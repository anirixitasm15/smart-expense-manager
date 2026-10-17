import streamlit as st
import pandas as pd
import os
import json
from datetime import date, timedelta

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Expense Tracker",
    page_icon="💰",
    layout="wide"
)

FILE_NAME = "expenses.csv"
COLUMNS = ["date", "amount", "category", "description"]

# ---------------- LOAD DATA ----------------
def load_expenses():
    if not os.path.exists(FILE_NAME):
        return pd.DataFrame(columns=COLUMNS)

    try:
        df = pd.read_csv(FILE_NAME)

        # Recover JSON records stored in a single column
        if len(df.columns) == 1 and len(df) > 0:
            records = []
            for value in df.iloc[:, 0]:
                try:
                    item = json.loads(value)
                    if isinstance(item, dict):
                        records.append(item)
                except (json.JSONDecodeError, TypeError):
                    continue
            df = pd.DataFrame(records)

        # Handle alternate old column names
        if "date" not in df.columns and "Date" in df.columns:
            df.rename(columns={"Date": "date"}, inplace=True)
        if "amount" not in df.columns and "Amount" in df.columns:
            df.rename(columns={"Amount": "amount"}, inplace=True)
        if "category" not in df.columns and "Category" in df.columns:
            df.rename(columns={"Category": "category"}, inplace=True)
        if "description" not in df.columns and "Description" in df.columns:
            df.rename(columns={"Description": "description"}, inplace=True)

        for col in COLUMNS:
            if col not in df.columns:
                df[col] = None

        df = df[COLUMNS]
        df["amount"] = pd.to_numeric(
            df["amount"], errors="coerce"
        ).fillna(0)

        return df

    except (pd.errors.ParserError, pd.errors.EmptyDataError):
        return pd.DataFrame(columns=COLUMNS)


def save_expenses(df):
    df[COLUMNS].to_csv(FILE_NAME, index=False)


# ---------------- INITIALIZE ----------------
if "expenses_df" not in st.session_state:
    st.session_state.expenses_df = load_expenses()

df = st.session_state.expenses_df.copy()

st.title("💰 Smart Expense Tracker")
st.write(
    "Add expenses, combine spending, and find out exactly "
    "where your money goes."
)

# ---------------- ADD EXPENSE ----------------
st.sidebar.header("➕ Add Expense")

with st.sidebar.form("add_expense", clear_on_submit=True):
    expense_date = st.date_input("Expense Date", value=date.today())

    amount = st.number_input(
        "Amount (₹)",
        min_value=0.0,
        step=10.0,
        format="%.2f"
    )

    category = st.selectbox(
        "Category",
        [
            "Food",
            "Transport",
            "Shopping",
            "Education",
            "Bills",
            "Entertainment",
            "Health",
            "Travel",
            "Other"
        ]
    )

    description = st.text_input(
        "Description",
        placeholder="e.g. Lunch, bus ticket, notebook"
    )

    add_button = st.form_submit_button("Add Expense")

    if add_button:
        if amount <= 0:
            st.error("Enter an amount greater than zero.")
        else:
            new_row = pd.DataFrame([{
                "date": str(expense_date),
                "amount": amount,
                "category": category,
                "description": description
            }])

            updated_df = pd.concat(
                [st.session_state.expenses_df, new_row],
                ignore_index=True
            )

            st.session_state.expenses_df = updated_df
            save_expenses(updated_df)

            st.success("Expense added!")
            st.rerun()

# Refresh data after any changes
df = st.session_state.expenses_df.copy()

for col in COLUMNS:
    if col not in df.columns:
        df[col] = None

df["amount"] = pd.to_numeric(
    df["amount"], errors="coerce"
).fillna(0)

df["date"] = pd.to_datetime(df["date"], errors="coerce")

# ---------------- OVERALL SUMMARY ----------------
st.header("📊 Overall Summary")

total_spending = df["amount"].sum()
total_count = len(df)
average_spending = (
    total_spending / total_count if total_count else 0
)

c1, c2, c3 = st.columns(3)

c1.metric("💸 Total Spending", f"₹{total_spending:,.2f}")
c2.metric("🧾 Total Expenses", total_count)
c3.metric("📍 Average Expense", f"₹{average_spending:,.2f}")

st.divider()

# ---------------- CATEGORY-WISE COMBINATION ----------------
st.header("🛍️ Category-wise Combined Spending")

if not df.empty:
    category_summary = (
        df.groupby("category", dropna=False)
        .agg(
            Total_Spent=("amount", "sum"),
            Number_of_Expenses=("amount", "count")
        )
        .reset_index()
    )

    category_summary["category"] = (
        category_summary["category"].fillna("Other")
    )

    category_summary = category_summary.sort_values(
        "Total_Spent", ascending=False
    )

    category_summary.columns = [
        "Category", "Total Spent (₹)", "Number of Expenses"
    ]

    st.dataframe(
        category_summary,
        use_container_width=True,
        hide_index=True
    )

    st.bar_chart(
        category_summary.set_index("Category")["Total Spent (₹)"]
    )

    # ---------------- CATEGORY DETAILS ----------------
    st.subheader("🔍 See Combined Expenses for One Category")

    available_categories = sorted(
        df["category"].dropna().astype(str).unique().tolist()
    )

    if available_categories:
        chosen_category = st.selectbox(
            "Choose a category",
            available_categories
        )

        selected_df = df[
            df["category"].astype(str) == chosen_category
        ].copy()

        st.write(f"**All {chosen_category} expenses:**")

        st.dataframe(
            selected_df[["date", "description", "amount"]]
            .rename(columns={
                "date": "Date",
                "description": "Description",
                "amount": "Amount (₹)"
            }),
            use_container_width=True,
            hide_index=True
        )

        st.metric(
            f"Total spent on {chosen_category}",
            f"₹{selected_df['amount'].sum():,.2f}"
        )

        st.caption(
            f"Combined {len(selected_df)} expense(s) "
            f"in {chosen_category}."
        )

    # ---------------- DAILY SPENDING ----------------
    st.divider()
    st.header("📅 Daily Spending")

    daily_data = df.dropna(subset=["date"]).copy()

    if not daily_data.empty:
        daily_data["Day"] = daily_data["date"].dt.date

        daily_summary = (
            daily_data.groupby("Day")["amount"]
            .sum()
            .reset_index()
        )

        daily_summary.columns = ["Date", "Total Spent (₹)"]

        st.dataframe(
            daily_summary.sort_values("Date", ascending=False),
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            daily_summary.set_index("Date")["Total Spent (₹)"]
        )
    else:
        st.info("No valid expense dates found.")

    # ---------------- MONTHLY SPENDING ----------------
    st.divider()
    st.header("🗓️ Monthly Spending")

    monthly_data = df.dropna(subset=["date"]).copy()

    if not monthly_data.empty:
        monthly_data["Month"] = (
            monthly_data["date"].dt.to_period("M").astype(str)
        )

        monthly_summary = (
            monthly_data.groupby("Month")["amount"]
            .sum()
            .reset_index()
        )

        monthly_summary.columns = ["Month", "Total Spent (₹)"]

        st.dataframe(
            monthly_summary.sort_values("Month", ascending=False),
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            monthly_summary.set_index("Month")["Total Spent (₹)"]
        )
    else:
        st.info("No monthly data available.")

    # ---------------- DATE FILTER ----------------
    st.divider()
    st.header("🗂️ Filter Expenses by Date")

    valid_dates = df["date"].dropna()

    if not valid_dates.empty:
        min_date = valid_dates.min().date()
        max_date = valid_dates.max().date()

        start_date = st.date_input(
            "From date",
            value=min_date,
            min_value=min_date,
            max_value=max_date,
            key="start_date"
        )

        end_date = st.date_input(
            "To date",
            value=max_date,
            min_value=min_date,
            max_value=max_date,
            key="end_date"
        )

        if start_date <= end_date:
            filtered_df = df[
                df["date"].dt.date.between(start_date, end_date)
            ]

            st.metric(
                "Total spent in selected period",
                f"₹{filtered_df['amount'].sum():,.2f}"
            )

            st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.warning("The start date must be before the end date.")

    # ---------------- DELETE EXPENSE ----------------
    st.divider()
    st.header("🗑️ Delete an Expense")

    expense_indices = df.index.tolist()

    if expense_indices:
        selected_index = st.selectbox(
            "Select an expense",
            expense_indices,
            format_func=lambda i: (
                f"{df.loc[i, 'date'].strftime('%d-%m-%Y') if pd.notna(df.loc[i, 'date']) else 'No date'} | "
                f"{df.loc[i, 'category']} | "
                f"₹{df.loc[i, 'amount']:,.2f} | "
                f"{df.loc[i, 'description'] or ''}"
            )
        )

        if st.button("Delete Selected Expense"):
            updated_df = df.drop(index=selected_index).copy()
            updated_df["date"] = updated_df["date"].apply(
                lambda d: d.strftime("%Y-%m-%d")
                if pd.notna(d) else None
            )

            st.session_state.expenses_df = updated_df.reset_index(drop=True)
            save_expenses(st.session_state.expenses_df)

            st.success("Expense deleted.")
            st.rerun()

    # ---------------- DOWNLOAD ----------------
    st.divider()
    st.header("📥 Download Your Data")

    download_df = df.copy()
    download_df["date"] = download_df["date"].apply(
        lambda d: d.strftime("%Y-%m-%d") if pd.notna(d) else ""
    )

    st.download_button(
        "Download All Expenses (CSV)",
        data=download_df.to_csv(index=False).encode("utf-8"),
        file_name="my_expenses.csv",
        mime="text/csv"
    )

else:
    st.info(
        "No expenses added yet. Use the sidebar to add your first expense."
    )

st.divider()
st.caption("Smart Expense Tracker | Built with Python + Streamlit")

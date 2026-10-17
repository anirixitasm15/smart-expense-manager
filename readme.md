# AVORA – RLSI College Assistant 🤖

**Voice-Enabled College Information & Computer Assistant**

AVORA is a web-based chatbot developed to help students get information about college-related queries, computer science, programming, and general technology. It combines college FAQ support with AI-powered responses to make information easier to access through a simple and interactive interface.

## 📌 Project Overview

AVORA is designed to act as a virtual assistant for students. Users can ask questions related to admissions, library information, examinations, fees, attendance, placements, internships, programming, and other computer-related topics.

The project also provides a conversational interface with voice interaction and customization features.

## ✨ Features

- 💬 **AI Chatbot:** Ask questions and receive responses.
- 🎓 **College Information:** Get answers to common college-related queries.
- 💻 **Programming Assistance:** Ask questions about programming and computer science.
- 🎙️ **Voice Interaction:** Interact with the chatbot using voice input, where supported.
- 📝 **Chat History:** Access saved conversations, where implemented.
- 🌙 **Dark and Light Mode:** Switch between available themes.
- 🌐 **Translation:** Use the available language translation feature.
- 🎨 **Interface Customization:** Customize supported font and color settings.
- 📚 **Academic Support:** Ask about admissions, library timings, examinations, attendance, and other academic topics.

## 🛠️ Technologies Used

- **Frontend:** React.js, JavaScript, HTML, CSS
- **Backend:** Node.js, Express.js
- **AI Integration:** Google Gemini API
- **Development Tools:** Visual Studio Code, npm, Git, GitHub

## 🏗️ Project Structure

```text
AVORA/
├── backend/
│   ├── controllers/
│   │   └── chatController.js
│   ├── routes/
│   │   └── chatRoutes.js
│   ├── .env
│   ├── package.json
│   └── server.js
├── frontend/
│   ├── public/
│   ├── src/
│   └── package.json
└── README.md
```

*Note: Adjust the folder structure above to match your actual project files.*

## ⚙️ Installation and Setup

### Prerequisites

Install the following before running the project:

- Node.js
- npm
- Visual Studio Code or another code editor
- A Google Gemini API key

### 1. Clone the Repository

```bash
git clone https://github.com/prachi-022/chatbot-name.git
```

### 2. Open the Project

```bash
cd chatbot-name
```

Open the project folder in Visual Studio Code.

### 3. Install Dependencies

Install the frontend and backend dependencies separately, depending on your folder structure.

For the backend:

```bash
cd backend
npm install
```

For the frontend:

```bash
cd ../frontend
npm install
```

### 4. Configure Environment Variables

Create a `.env` file in the backend directory and add your Gemini API key using the variable name expected by your backend code.

Example:

```env
GEMINI_API_KEY=your_gemini_api_key
```

**Important:** Replace the placeholder with your own API key. Never upload your actual API key or other secrets to GitHub.

### 5. Start the Backend

From the backend directory, run the start command configured in your `package.json`.

For example, if a start script is configured:

```bash
npm start
```

### 6. Start the Frontend

Open another terminal, navigate to the frontend directory, and run:

```bash
npm run dev
```

Use the local URL displayed in the terminal to open AVORA in your browser. The exact commands may vary depending on your project configuration.

## 💡 Example Questions

Users can ask questions such as:

- What courses are available at the college?
- What are the library timings?
- Which documents are required for admission?
- What is the importance of attendance?
- Explain the difference between C and C++.
- What is a database?
- Explain object-oriented programming.
- How does a chatbot work?

The accuracy and availability of answers depend on the configured AI service and the college information provided to the application.

## 🔐 Security

- Keep API keys in environment variables.
- Do not commit `.env` files containing secrets.
- Add sensitive configuration files to `.gitignore`.
- Avoid sharing private credentials in public repositories.

## 🎯 Project Objectives

1. Provide an easy-to-use virtual assistant for students.
2. Simplify access to frequently requested college information.
3. Support programming and computer science learning.
4. Explore the integration of AI APIs into web applications.
5. Provide an interactive interface with voice and customization features.

## 🚀 Future Enhancements

- Expand the college FAQ database.
- Improve voice recognition and response handling.
- Add more language options.
- Improve chatbot response accuracy.
- Introduce additional student-support features.

## 👩‍💻 Developer

**Name:** Prachi Bhoite  
**Course:** Bachelor of Computer Applications (BCA)  
**College:** RLSI BCA College, Belagavi, Karnataka, India

## 📄 License

This project was developed for academic and educational purposes. Add a formal open-source license if you intend to distribute the project under specific reuse terms.

---

⭐ **AVORA – Making college information and computer assistance more accessible through conversation.**

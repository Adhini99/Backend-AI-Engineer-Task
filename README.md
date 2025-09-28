# 📘 LinkedIn Post Generator API (Gemini + Tavily + FastAPI)

## 🚀 Overview
This project is built as part of the **Backend + AI Developer Assignment** for **Demanual AI**.  
It provides an **AI-powered API service** that:  
- Fetches **recent news articles** about a given topic using **Tavily API**.  
- Generates a **professional LinkedIn-style post** using **Google Gemini API** + LangChain.  
- Returns results via a **FastAPI backend** with Swagger documentation.  

🔗 **Live Swagger API**: [https://backend-ai-engineer-task.onrender.com/docs](https://backend-ai-engineer-task.onrender.com/docs)  

---

## 🛠️ Tech Stack
- **FastAPI** – Backend framework  
- **LangChain** – LLM orchestration  
- **Google Gemini API** – Content generation  
- **Tavily API** – News search  
- **Render** – Deployment platform  

---

## 📂 Project Structure
├── api/
│ ├── app.py # FastAPI backend
│ ├── client.py # Streamlit client (for local testing)
├── requirements.txt
├── README.md
└── .env (not committed to repo)


Deployment

Deployed using Render.

API base URL: https://backend-ai-engineer-task.onrender.com

Swagger docs: https://backend-ai-engineer-task.onrender.com/docs

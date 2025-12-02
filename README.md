# 🏡 Real Estate AI Assistant  
### Built by **Vinaykumar Yadav**  
GitHub Repository: https://github.com/yadavvinay77/real_estate_chatbot  

---

# 🚀 Overview  

The **Real Estate AI Assistant** is a production-ready, intelligent chatbot built for rental property search, repair/service management, and real‑estate support using:

- **FastAPI** backend  
- **WebSockets** for real‑time chat  
- **RAG (Retrieval-Augmented Generation)** for verified answers  
- **Local LLM (Ollama, Qwen2.5, etc.)**  
- **PostgreSQL/SQLModel** for database operations  
- **TailwindCSS UI**  
- **CI/CD with GitHub Actions + Railway deployment**

This project is engineered to mimic a professional property management assistant capable of:

- Understanding queries  
- Completing multi-step workflows  
- Suggesting service providers  
- Scoring rental listings  
- Avoiding hallucinations through RAG  
- Maintaining conversational state  

Perfect for your **AI engineer portfolio**, demonstrating full‑stack ML + backend + deployment skills.

---

# ✨ Features  

### 🧠 AI-Powered Chatbot  
- Multi-step guided conversations  
- Personalized responses using session memory  
- RAG + LLM hybrid answering  
- No hallucination rules  
- Intelligent fallback logic  

### 🛠 Repair & Property Service Engine  
Supports 25+ repair categories including:
- Boiler/Heating  
- Leaks  
- Electrical  
- Locks/Doors  
- Windows  
- Flooring  
- Exterior/Garden  
- Fire & Safety Issues  
- Internet issues  
And more.

Includes:
- Issue categorization  
- Address collection  
- Provider matching  
- “Done / thanks” graceful flow  
- Automatic DB logging  

### 🏠 Rental Search Engine  
User can filter by:
- Location  
- Property type (house, flat, studio…)  
- Bedrooms  
- Budget  
- Furnished/unfurnished  
- Garden  
- Parking  

Returns:
- Matched properties  
- Automatic scoring  
- Beautiful card-style UI  

### 💬 General Questions  
LLM answers with RAG grounding from:
- Boiler FAQ  
- Leak FAQ  
- Safety documents  
- Property management docs  

### ⚡ Backend Architecture  
- Modular services  
- SQLModel ORM  
- Central Conversation Engine  
- WebSocket connection  
- Static frontend hosted by FastAPI  

### 🎨 Modern Frontend  
- TailwindCSS  
- Responsive chat interface  
- Service cards  
- Provider cards  
- Animated typing indicator  
- WebSocket live updates  

### 🚀 Deployment  
- Dockerfile production‑optimized  
- Railway hosting  
- GitHub Actions CI/CD pipeline  
- Auto-deploy on push to `main`  

---

# 📁 Project Structure  

```
real_estate_ai/
│
├── app/
│   ├── main.py                    # FastAPI entrypoint
│   ├── router.py                  # REST endpoints
│   ├── database.py                # SQLModel database engine
│   │
│   ├── models/
│   │   ├── user_models.py
│   │   ├── rental_models.py
│   │   ├── repair_models.py
│   │   ├── provider_models.py
│   │   └── chat_models.py
│   │
│   ├── services/
│   │   ├── conversation_engine.py # Brain of the chatbot
│   │   ├── rental_engine.py
│   │   ├── repair_engine.py
│   │   ├── provider_engine.py
│   │   ├── rag_engine.py
│   │   └── ollama_client.py
│   │
│   ├── templates/
│   │   ├── index.html
│   │   └── admin.html
│   │
│   ├── static/
│   │   ├── css/styles.css
│   │   ├── js/chat.js
│   │   └── img/
│   │
│   └── data/
│       ├── properties.json
│       ├── service_providers.json
│       └── rag_docs/*.txt
│
├── Dockerfile
├── requirements.txt
├── README.md
└── start.sh
```

---

# 🧠 Retrieval-Augmented Generation (RAG)

The system uses:
- Sentence Transformers  
- Chunked text documents  
- Cosine similarity search  
- Context injection into prompts  

This ensures:
✔ Factual accuracy  
✔ No hallucinations  
✔ Property‑domain‑aware replies  

---

# 🔧 Running the Project Locally  

### 1️⃣ Create virtual environment  
```
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scriptsctivate           # Windows
```

### 2️⃣ Install dependencies  
```
pip install -r requirements.txt
```

### 3️⃣ Start FastAPI backend  
```
uvicorn app.main:app --reload --port 8000
```

### 4️⃣ Open UI  
Visit:

```
http://127.0.0.1:8000/
```

---

# 🐳 Docker Deployment  

### Build image  
```
docker build -t real-estate-ai .
```

### Run container  
```
docker run -p 8000:8000 real-estate-ai
```

---

# 🚀 CI/CD — GitHub Actions + Railway Deployment  

### Workflow file  
```
.github/workflows/deploy.yml
```

Pipeline:
1. Checkout code  
2. Build Docker image  
3. Authenticate to Railway  
4. Deploy automatically  

### Required GitHub Secrets  
| Secret | Description |
|--------|-------------|
| `RAILWAY_API_TOKEN` | Railway API token |
| `RAILWAY_SERVICE_ID` | Railway service ID |

Push to `main` → App auto-deploys.  

---

# 🌍 Live URL (after deployment)

Add here once deployed:

```
https://<your-app>.up.railway.app
```

---

# 📈 Future Enhancements  
- User login system  
- Tenant dashboard  
- PDF repair tickets  
- AI intent classification  
- WhatsApp / SMS integration  
- Multi-language support (Gujarati, Hindi, English)  
- Voice-based chat  

---

# 🤝 Contributing  
Pull requests are welcome.  
Create an issue for feature requests or bugs.

---

# 👨‍💻 Author  
**Vinaykumar Yadav**  
AI Engineer | ML Researcher | Full‑Stack Developer  
📧 Email: yadavvinay77@gmail.com  
🔗 GitHub: https://github.com/yadavvinay77  

---

# 📜 License  
MIT License — free to use, modify, and distribute.

---

# 🎉 Thank You!  
This AI assistant is a fully modular, production‑grade project ideal for real estate automation, showcasing your end‑to‑end AI engineering capabilities.


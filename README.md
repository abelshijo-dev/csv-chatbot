# 🤖 AI CSV Chatbot

Upload any CSV file and ask questions about your data in plain English. No SQL or coding required.

Built with **Python**, **Streamlit**, and **Groq (LLaMA 3.3)**.

---

## 🖥️ Demo

![AI CSV Chatbot](https://i.imgur.com/placeholder.png)

---

## ✨ Features

- 📂 Upload any CSV file
- 💬 Ask questions in plain English
- 📊 Auto data preview and summary
- 🧠 Powered by LLaMA 3.3 via Groq (free)
- 🔁 Multi-turn conversation — ask follow-up questions

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/YOURUSERNAME/csv-chatbot.git
cd csv-chatbot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get a free Groq API key
Sign up at [console.groq.com](https://console.groq.com) and create an API key.

### 4. Set your API key

**Windows (PowerShell):**
```bash
$env:GROQ_API_KEY="your-key-here"
```

**Mac/Linux:**
```bash
export GROQ_API_KEY="your-key-here"
```

### 5. Run the app
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 🗂️ Project Structure

```
csv-chatbot/
├── app.py            # Main application
├── requirements.txt  # Dependencies
└── README.md         # This file
```

---

## 💡 Example Questions You Can Ask

- *What are the top 5 values in column X?*
- *What is the average of column Y?*
- *Are there any missing values?*
- *What trends do you see in this data?*
- *Which rows have the highest or lowest values?*

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Streamlit | Web UI |
| Pandas | Data loading and processing |
| Groq API | AI model (LLaMA 3.3) |

---

## 📚 What I Learned Building This

- File handling with pandas
- Prompt engineering — injecting data context into AI prompts
- Making API calls to an LLM
- Building a chat interface with session state
- Multi-turn conversation history

---

## 📄 License

MIT License — free to use and modify.



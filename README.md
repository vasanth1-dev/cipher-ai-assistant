

# 📁 Project Structure

```
cipher-ai-assistant/
│
├── core/
│   ├── assistant.py
│   ├── listener.py
│   ├── router.py
│   ├── speaker.py
│   ├── registry.py
│   └── ...
│
├── gui/
│   ├── app.py
│   ├── main_window.py
│   ├── pages/
│   ├── widgets/
│   └── ...
│
├── services/
│   ├── ai_service.py
│   ├── conversation_service.py
│   ├── memory_service.py
│   ├── reminder_service.py
│   ├── todo_service.py
│   └── ...
│
├── skills/
│   ├── ai.py
│   ├── apps.py
│   ├── browser.py
│   ├── memory.py
│   ├── system.py
│   └── ...
│
├── plugins/
│
├── data/
│
├── config.py
├── requirements.txt
├── run.py
└── run_gui.py
```

---

# ⚙ Requirements

- Ubuntu 24.04 LTS
- Python 3.12+
- Ollama
- FFmpeg
- Git

---

# 📦 Installation

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/Cipher.git

cd Cipher
```

---

## Create Virtual Environment

```bash
python3 -m venv venv
```

Activate it

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🤖 Install Ollama

Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Download the default model

```bash
ollama pull qwen2.5:1.5b
```

Start Ollama

```bash
ollama serve
```

---

# ▶ Running Cipher

GUI Version

```bash
python run_gui.py
```

Console Version

```bash
python run.py
```

---

# 🎤 Example Commands

## Applications

```
Open Firefox

Open Terminal

Close Firefox
```

---

## Browser

```
Open Google

Search Google Python decorators

Search YouTube AI news
```

---

## Memory

```
Remember my bike is Duke 390

What is my bike?

Forget my bike
```

---

## Todo

```
Add task Complete project

Show tasks

Complete task 1
```

---

## Reminder

```
Remind me to call mom in 30 minutes

Show reminders
```

---

## Calendar

```
Add event Project Meeting tomorrow 10:00

Show calendar
```

---

# 🧩 Technologies Stack

| Category           | Technologies                |
| ------------------ | --------------------------- |
| Programming        | Python                      |
| GUI                | PyQt6                       |
| AI / LLM           | Ollama                      |
| Speech Recognition | Faster-Whisper              |
| Voice              | SpeechRecognition, Edge TTS |
| Wake Word          | OpenWakeWord                |
| Data Processing    | NumPy                       |
| Computer Vision    | OpenCV                      |
| HTTP / APIs        | Requests, REST APIs         |
| OS                 | Ubuntu Linux                |
| Version Control    | Git, GitHub                 |


---

# 🔮 Future Roadmap

### v2.1

- Better Memory
- Local Document Search
- RAG Support
- Plugin Marketplace
- Settings UI

### v3.0

- Windows Support
- Multi-Agent System
- Vision Improvements
- Automation Engine

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Vasanth K**

Computer Science Engineering

Cipher v2 Developer

---

# ⭐ Support

If you like this project,

please consider giving it a ⭐ on GitHub.

---

# 🚀 Cipher v2

**Professional Offline AI Assistant for Ubuntu**

# 🚀 Cipher v2

> A professional offline-first AI voice assistant for Ubuntu built with Python, Whisper, Ollama, and PyQt6.

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Ubuntu%2024.04-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Version](https://img.shields.io/badge/Version-v2.0.0-blue.svg)

---

# 📖 Overview

Cipher v2 is a modular AI voice assistant designed for Ubuntu.

It combines offline AI, speech recognition, text-to-speech, plugin support, and a modern desktop interface into a single application.

The project follows a service-oriented architecture with a plugin framework, making it easy to extend and maintain.

---

# ✨ Features

## 🤖 AI

- Offline AI using Ollama
- Local LLM support
- AI conversation mode
- Context-aware responses

---

## 🎤 Voice

- Wake word support
- Google Speech Recognition
- Faster-Whisper fallback
- Edge TTS voice synthesis
- Natural voice responses

---

## 🖥 GUI

- Modern PyQt6 interface
- Chat window
- Status indicators
- Microphone controls
- System tray integration

---

## 🧠 Memory

- Remember information
- Recall saved information
- Forget stored memories
- Persistent memory storage

---

## 📅 Productivity

- Todo List
- Reminder System
- Calendar Events
- Contacts

---

## 💻 Ubuntu Integration

- Launch applications
- Close applications
- Open folders
- Browser control
- Notifications

---

## 🔌 Plugin System

- Dynamic plugin discovery
- Plugin lifecycle management
- Plugin manifests
- Extensible architecture

---

## 🛠 Architecture

- Modular design
- Service Layer
- Runtime Container
- Command Pipeline
- Intent Routing
- Event Bus

---

# 📁 Project Structure

```
Cipher/
│
├── core/
├── gui/
├── services/
├── skills/
├── plugins/
├── data/
├── logs/
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

# 🧩 Technologies Used

- Python
- PyQt6
- Ollama
- Faster Whisper
- SpeechRecognition
- Edge TTS
- OpenWakeWord
- NumPy
- OpenCV
- Requests

---

# 🏗 Architecture

```
Wake Word
      │
      ▼
Speech Recognition
      │
      ▼
Intent Detection
      │
      ▼
Skill Router
      │
      ▼
AI / Local Skill
      │
      ▼
Text To Speech
      │
      ▼
GUI
```

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
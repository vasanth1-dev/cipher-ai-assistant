# ==========================================
# CIPHER v2 CONFIGURATION
# ==========================================

# Assistant
ASSISTANT_NAME = "Cipher"
USER_NAME = "Vasanth"

# ------------------------------------------
# Wake Word
# ------------------------------------------

WAKE_WORDS = [
    "hey cipher",
    "cipher",
    "hey cypher",
    "cypher",
    "hey safer",
    "safer",
    "hey stop",
]
# ========================
WAKEWORD_MODEL = None
WAKEWORD_THRESHOLD = 0.5

# ------------------------------------------
# Whisper
# ------------------------------------------

WHISPER_MODEL = "medium.en"
DEVICE = "cpu"
COMPUTE_TYPE = "int8"

# ------------------------------------------
# Audio
# ------------------------------------------

SAMPLE_RATE = 16000
CHANNELS = 1
LISTEN_SECONDS = 5

# ------------------------------------------
# Speech
# ------------------------------------------
VOICE = "en-IN-PrabhatNeural"
SPEECH_RATE = 170
SPEECH_VOLUME = 1.0

# ------------------------------------------
# Ollama
# ------------------------------------------

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:1.5b"

# ------------------------------------------
# Browser
# ------------------------------------------

GOOGLE_URL = "https://www.google.com"
YOUTUBE_URL = "https://www.youtube.com"
GITHUB_URL = "https://github.com"

GOOGLE_SEARCH = "https://www.google.com/search?q={}"
YOUTUBE_SEARCH = "https://www.youtube.com/results?search_query={}"

# ------------------------------------------
# Applications
# ------------------------------------------

APPLICATIONS = {
    "firefox": "firefox",
    "chrome": "google-chrome",
    "terminal": "gnome-terminal",
    "files": "nautilus",
    "calculator": "gnome-calculator",
    "settings": "gnome-control-center",
    "text editor": "gedit",
    "vscode": "code",
    "vs code": "code",
}

# ------------------------------------------
# Session
# ------------------------------------------

SESSION_TIMEOUT = 300
REQUEST_TIMEOUT =300
MIC_TIMEOUT = 5
PHRASE_TIMEOUT = 6

# ------------------------------------------
# Logging
# ------------------------------------------

LOG_FILE = "logs/cipher.log"
LOG_LEVEL = "INFO"

# ==========================
# AI Personality
# ==========================

AI_NAME = "Cipher"

AI_PERSONALITY = """
You are Cipher, an intelligent personal voice assistant.

Rules:

- Speak naturally like a human assistant.
- Keep answers short by default (1–2 sentences).
- If the user asks "explain", give a medium explanation.
- If the user asks "explain in detail", provide a detailed answer.
- Never write article-style responses unless explicitly requested.
- For app commands, simply confirm the action.
- Be friendly, confident and professional.
- Answer in the same language as the user.
- If the user mixes Tamil and English, reply in Tamil-English naturally.
- Don't repeat the user's question.
- Don't use unnecessary greetings in every reply.
- Don't say "As an AI language model...".
- If you don't know something, say it honestly.
"""


EXIT_COMMANDS = [
    "exit",
    "quit",
    "goodbye",
    "stop",
    ]
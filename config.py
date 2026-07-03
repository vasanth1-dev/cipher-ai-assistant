# ==========================================
# CIPHER v2 CONFIGURATION
# ==========================================

# Assistant
ASSISTANT_NAME = "Cipher"
USER_NAME = "Vasanth"

# ------------------------------------------
# Wake Word
# ------------------------------------------

WAKE_WORD = "hey cipher"

# ------------------------------------------
# Whisper
# ------------------------------------------

WHISPER_MODEL = "small.en"
DEVICE = "cpu"
COMPUTE_TYPE = "int8"

# ------------------------------------------
# Audio
# ------------------------------------------

SAMPLE_RATE = 44100
CHANNELS = 2
LISTEN_SECONDS = 5

# ------------------------------------------
# Speech
# ------------------------------------------

SPEECH_RATE = 170
SPEECH_VOLUME = 1.0

# ------------------------------------------
# Ollama
# ------------------------------------------

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "phi3:latest"

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

# ------------------------------------------
# Logging
# ------------------------------------------

LOG_FILE = "logs/cipher.log"
LOG_LEVEL = "INFO"
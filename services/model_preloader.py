import requests

from config import OLLAMA_URL, MODEL_NAME


def preload():

    try:

        requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": "hi",
                "stream": False,
                "keep_alive": "30m",
            },
            timeout=30,
        )

        print("✅ Ollama model preloaded.")

    except Exception as e:

        print("Preload Error:", e)
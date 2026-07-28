import requests

from core.logger import logger
from config import OLLAMA_URL, MODEL_NAME


def preload():

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": "hi",
                "stream": False,
                "keep_alive": "30m",
            },
            timeout=30,
        )

        response.raise_for_status()

        logger.info("✅ Ollama model preloaded.")

    except Exception as e:

        logger.exception(e)
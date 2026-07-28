import json
from pathlib import Path

from core.logger import logger


class SettingsService:

    def __init__(
       self,
    ) -> None:

        self.file = Path("data/settings.json")

        self.defaults = {
            "assistant_name": "Cipher",

            "model": "phi3",
            "temperature": "0.2",

            "voice": True,
            "startup": False,
            "tray": True,
            "theme": "Dark",
            "accent": "Blue",
            "font-size": "14",
            "ui_scale": "100%",
            "animation_speed": "Normal",
            "high_contrast": False,
            "reduced_motion": False,
            "large_click_targets": False,

            "speech_rate": 170,
            "speech_volume": 1.0,

            "ollama_model": "phi3:latest",
            "gemini_enabled": True,

            "wake_words": [
                "hey cipher",
                "cipher",
            ],
        }

        self.file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not self.file.exists():
            self.save(self.defaults.copy())

    # ------------------------------------------------ #
    # Internal
    # ------------------------------------------------ #

    def load(self):

        try:

            with open(
                self.file,
                "r",
                encoding="utf-8",
            ) as f:

                data = json.load(f)

            if not isinstance(data, dict):
                raise ValueError("Invalid settings format")

            updated = False

            for key, value in self.defaults.items():

                if key not in data:

                    data[key] = value
                    updated = True

            if updated:
                self.save(data)

            return data

        except Exception as e:

            logger.exception(
                f"[SETTINGS] Failed to load settings: {e}"
            )

            defaults = self.defaults.copy()

            self.save(defaults)

            return defaults

    def save(self, settings):

        try:

            with open(
                self.file,
                "w",
                encoding="utf-8",
            ) as f:

                json.dump(
                    settings,
                    f,
                    indent=4,
                    ensure_ascii=False,
                    sort_keys=True,
                )

            logger.info("[SETTINGS] Saved.")

        except Exception as e:

            logger.exception(
                f"[SETTINGS] Failed to save settings: {e}"
            )

    # ------------------------------------------------ #
    # Public API
    # ------------------------------------------------ #

    def get(self, key, default=None):

        return self.load().get(
            key,
            default,
        )

    def get_int(self, key, default=0):

        try:
            return int(self.get(key, default))
        except Exception:
            return default

    def get_float(self, key, default=0.0):

        try:
            return float(self.get(key, default))
        except Exception:
            return default

    def get_bool(self, key, default=False):

        value = self.get(key, default)

        if isinstance(value, bool):
            return value

        return str(value).lower() in (
            "1",
            "true",
            "yes",
            "on",
        )

    def set(self, key, value):

        key = str(key).strip()

        if not key:
            return "Invalid setting name."

        settings = self.load()

        settings[key] = value

        self.save(settings)

        logger.info(
            f"[SETTINGS] Updated: {key}"
        )

        return "Settings updated."

    def update(self, **kwargs):

        settings = self.load()

        settings.update(kwargs)

        self.save(settings)

        logger.info(
            f"[SETTINGS] Updated keys: {', '.join(kwargs.keys())}"
        )

    def save_profile(self, name: str) -> None:
        """
        Save the current settings as a named profile.
        """

        settings = self.load()

        profiles = settings.get("profiles", {})
        profiles[name] = settings.copy()

        settings["profiles"] = profiles

        self.update(**settings)

    def load_profile(self, name: str):

        settings = self.load()

        profile = settings.get(
            "profiles",
            {}
        ).get(name)

        if profile:

            self.update(**profile)

            return profile

        return None

    def exists(self, key):

        if not key:
            return False

        return key in self.load()

    def remove(self, key):

        if not key:
            return False
        
        key = str(key).strip()

        settings = self.load()

        if key in settings:

            del settings[key]

            self.save(settings)

            return True

        return False

    def all(self):

        return self.load()

    def reset(self):

        defaults = self.defaults.copy()

        self.save(defaults)

        logger.info(
            "[SETTINGS] Reset to defaults."
        )

        return self.load()


settings_service = SettingsService()
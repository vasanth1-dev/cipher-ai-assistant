"""
Cipher v2
Password Generator Plugin

Generate cryptographically secure passwords.

Features
--------
- Configurable password length
- Uppercase letters
- Lowercase letters
- Digits
- Symbols
- Password strength estimation
"""

from __future__ import annotations

import secrets
import string

from core.logger import logger
from plugins.base_plugin import Plugin


class PasswordGeneratorPlugin(Plugin):
    """
    Secure password generation plugin.
    """

    name = "password_generator"
    version = "1.0.0"
    description = "Generate secure random passwords."

    SYMBOLS = "!@#$%^&*()-_=+[]{}<>?/"

    def can_handle(self, text: str) -> bool:
        text = text.lower()

        keywords = (
            "generate password",
            "create password",
            "random password",
            "secure password",
            "strong password",
        )

        return any(keyword in text for keyword in keywords)

    def handle(self, text: str):
        """
        Password requests are intended to be routed through
        Cipher's structured intent pipeline.
        """

        return {
            "success": True,
            "message": (
                "Password Generator plugin is available. "
                "Waiting for structured password generation commands."
            ),
        }

    # --------------------------------------------------
    # Password Generation
    # --------------------------------------------------

    def generate(
        self,
        length: int = 16,
        uppercase: bool = True,
        lowercase: bool = True,
        digits: bool = True,
        symbols: bool = True,
    ) -> str:
        """
        Generate a cryptographically secure password.
        """
        length = max(4, length)

        pools = []

        if uppercase:
            pools.append(string.ascii_uppercase)

        if lowercase:
            pools.append(string.ascii_lowercase)

        if digits:
            pools.append(string.digits)

        if symbols:
            pools.append(self.SYMBOLS)

        if not pools:
            raise ValueError("At least one character set must be enabled.")

        # Ensure every selected pool contributes at least one character.
        password = [
            secrets.choice(pool)
            for pool in pools
        ]

        alphabet = "".join(pools)

        while len(password) < length:
            password.append(secrets.choice(alphabet))

        secrets.SystemRandom().shuffle(password)

        return "".join(password)

    # --------------------------------------------------
    # Password Strength
    # --------------------------------------------------

    def strength(self, password: str) -> dict:
        score = 0

        if len(password) >= 8:
            score += 1

        if len(password) >= 12:
            score += 1

        if any(ch.islower() for ch in password):
            score += 1

        if any(ch.isupper() for ch in password):
            score += 1

        if any(ch.isdigit() for ch in password):
            score += 1

        if any(ch in self.SYMBOLS for ch in password):
            score += 1

        labels = {
            0: "Very Weak",
            1: "Weak",
            2: "Fair",
            3: "Good",
            4: "Strong",
            5: "Very Strong",
            6: "Excellent",
        }

        return {
            "score": score,
            "max_score": 6,
            "rating": labels.get(score, "Unknown"),
            "length": len(password),
        }

    # --------------------------------------------------
    # Logging
    # --------------------------------------------------

    @staticmethod
    def log_error(exc: Exception):
        logger.exception(exc)
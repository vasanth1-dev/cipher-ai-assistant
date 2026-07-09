from html import escape

import re


class MarkdownRenderer:

    @staticmethod
    def render(text: str) -> str:

        if not text:
            return ""

        html = escape(text)

        # ---------------------------------
        # Code Blocks
        # ---------------------------------

        html = re.sub(
            r"```(.*?)```",
            lambda m: (
                "<pre style='"
                "background:#0F172A;"
                "padding:12px;"
                "border-radius:10px;"
                "overflow:auto;"
                "color:#E5E7EB;"
                "'><code>"
                + m.group(1)
                + "</code></pre>"
            ),
            html,
            flags=re.S,
        )

        # ---------------------------------
        # Bold
        # ---------------------------------

        html = re.sub(
            r"\*\*(.*?)\*\*",
            r"<b>\1</b>",
            html,
        )

        # ---------------------------------
        # Italic
        # ---------------------------------

        html = re.sub(
            r"\*(.*?)\*",
            r"<i>\1</i>",
            html,
        )

        # ---------------------------------
        # Inline Code
        # ---------------------------------

        html = re.sub(
            r"`(.*?)`",
            r"<code style='"
            "background:#1E293B;"
            "padding:2px 4px;"
            "border-radius:4px;"
            "'>\1</code>",
            html,
        )

        html = html.replace("\n", "<br>")

        return html
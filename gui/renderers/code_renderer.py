"""
Cipher Code Renderer

Responsible for rendering fenced code blocks
using Qt RichText compatible HTML.
"""

import html


class CodeRenderer:

    def render(
        self,
        language: str,
        code: str,
    ) -> str:

        if not code:
            return ""

        language = (
            language or ""
        ).strip()

        code = html.escape(code)

        if language:

            title = (
                f"<b>{language}</b><br>"
            )

        else:

            title = ""

        return (
            "<pre>"
            + title
            + code
            + "</pre>"
        )


code_renderer = CodeRenderer()
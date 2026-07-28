"""
Cipher Markdown Renderer

Uses CodeRenderer for fenced code blocks.
"""

import html
import re

from gui.renderers.code_renderer import (
    code_renderer,
)


class MarkdownRenderer:

    def render(
        self,
        text: str,
    ) -> str:

        if not text:
            return ""

        text = self._normalize(text)

        text, code_block = self._render_code_blocks(text)

        text = html.escape(text)

        text = self._render_headings(text)

        text = self._render_lists(text)

        text = self._render_bold(text)

        text = self._render_italic(text)

        text = self._render_inline_code(text)

        text = text.replace(
            "\n",
            "<br>",
        )

        for index, block in enumerate(code_block):
            text = text.replace(
                f"__CODE_BLOCK_{index}__",
                block,
            )

        return text

    # --------------------------------------------------

    def _normalize(
        self,
        text: str,
    ) -> str:

        text = text.replace(
            "\r\n",
            "\n",
        )

        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text,
        )

        return text.strip()

    # --------------------------------------------------
    # Code Blocks
    # --------------------------------------------------

    def _render_code_blocks(
        self, 
        text: str,
    ) -> tuple[str, list[str]]:

        pattern = re.compile(
            r"```(\w+)?\n?(.*?)```",
            re.DOTALL,
        )

        code_blocks = []

        def replace(match):

            language = match.group(1) or ""
            code = match.group(2) or ""

            rendered = code_renderer.render(
                language,
                code,
            )

            placeholder = f"__CODE_BLOCK_{len(code_blocks)}__"

            code_blocks.append(rendered)

            return placeholder

        text = pattern.sub(replace, text)

        return text, code_blocks

    # --------------------------------------------------
    # Headings
    # --------------------------------------------------

    def _render_headings(
        self,
        text: str,
    ) -> str:

        for level in range(6, 0, -1):

            pattern = (
                rf"^{'#'*level}\s+(.+)$"
            )

            text = re.sub(
                pattern,
                r"<b>\1</b>",
                text,
                flags=re.MULTILINE,
            )

        return text

    # --------------------------------------------------
    # Lists
    # --------------------------------------------------

    def _render_lists(
        self,
        text: str,
    ) -> str:

        text = re.sub(
            r"^\-\s+",
            "• ",
            text,
            flags=re.MULTILINE,
        )

        text = re.sub(
            r"^\*\s+",
            "• ",
            text,
            flags=re.MULTILINE,
        )

        return text

    # --------------------------------------------------
    # Bold
    # --------------------------------------------------

    def _render_bold(
        self,
        text: str,
    ) -> str:

        return re.sub(
            r"\*\*(.+?)\*\*",
            r"<b>\1</b>",
            text,
        )

    # --------------------------------------------------
    # Italic
    # --------------------------------------------------

    def _render_italic(
        self,
        text: str,
    ) -> str:

        return re.sub(
            r"\*(.+?)\*",
            r"<i>\1</i>",
            text,
        )

    # --------------------------------------------------
    # Inline Code
    # --------------------------------------------------

    def _render_inline_code(
        self,
        text: str,
    ) -> str:

        return re.sub(
            r"`(.+?)`",
            r"<code>\1</code>",
            text,
        )


markdown_renderer = MarkdownRenderer()
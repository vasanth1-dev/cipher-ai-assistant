from html import escape

import re


class MarkdownRenderer:

    @staticmethod
    def _render_code_block(match):

        language = match.group(1)

        code = escape(match.group(2).strip())

        if language:
            language = language.upper()
        else:
            language = "CODE"

        return f"""
    <table width="100%" cellspacing="0" cellpadding="0">
    <tr>
    <td style="
    background:#0F172A;
    border:1px solid #334155;
    border-radius:10px;
    padding:0;
    ">

    <div style="
    padding:8px 12px;
    border-bottom:1px solid #334155;
    font-size:9pt;
    font-weight:bold;
    color:#94A3B8;
    ">
    {language}
    </div>

    <pre style="
    margin:0;
    padding:14px;
    overflow:auto;
    white-space:pre;
    color:#E2E8F0;
    font-family:Consolas, monospace;
    font-size:13px;
    "><code>{code}</code></pre>

    </td>
    </tr>
    </table>
    """

    @staticmethod
    def render(text: str) -> str:

        if not text:
            return ""

        html = escape(text)

        # ---------------------------------
        # Triple Backtick Code Blocks
        # ---------------------------------

        html = re.sub(
            r"```(\w+)?\n?(.*?)```",
            MarkdownRenderer._render_code_block,
            html,
            flags=re.S,
        )

        # ---------------------------------
        # Bold
        # ---------------------------------

        html = re.sub(
            r"\*\*(.+?)\*\*",
            r"<b>\1</b>",
            html,
        )

        # ---------------------------------
        # Italic
        # ---------------------------------

        html = re.sub(
            r"\*(.+?)\*",
            r"<i>\1</i>",
            html,
        )

        # ---------------------------------
        # Inline Code
        # ---------------------------------

        html = re.sub(
            r"`([^`\n]+?)`",
            r"<code style='"
            "background:#1E293B;"
            "padding:2px 6px;"
            "border-radius:4px;"
            "font-family:Consolas, monospace;"
            "'>\1</code>",
            html,
        )

        # ---------------------------------
        # Bullet Lists
        # ---------------------------------

        html = re.sub(
            r"^- (.+)$",
            r"• \1",
            html,
            flags=re.M,
        )

        html = html.replace("\n", "<br>")

        return html
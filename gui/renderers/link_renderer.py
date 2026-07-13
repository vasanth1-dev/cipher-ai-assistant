"""
Cipher Link Renderer

Converts plain URLs into clickable HTML links.
"""

import html
import re


class LinkRenderer:

    URL_PATTERN = re.compile(
        r"(https?://[^\s<]+)"
    )

    def render(
        self,
        text: str,
    ):

        if not text:
            return ""

        def replace(match):

            url = match.group(1)

            safe = html.escape(url)

            return (
                f'<a href="{safe}">{safe}</a>'
            )

        return self.URL_PATTERN.sub(
            replace,
            text,
        )


link_renderer = LinkRenderer()
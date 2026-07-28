"""
Cipher Renderer Manager

Routes text through all renderers.
"""

from gui.renderers.markdown_renderer import (
    markdown_renderer,
)
from gui.renderers.link_renderer import (
    link_renderer,
)
from gui.renderers.code_renderer import (
    code_renderer,
)


class RendererManager:

     def __init__(
       self,
    ) -> None:

        self.markdown = markdown_renderer
        self.link = link_renderer
        self.code = code_renderer

    # --------------------------------------------------

    def render(
        self,
        text: str,
    ) -> str:

        if not text:
            return ""

        text = self.markdown.render(
            text,
        )

        text = self.link.render(
            text,
        )

        return text

    # --------------------------------------------------

    def render_code(
        self,
        language: str,
        code: str,
    ) -> str:

        return self.code.render(
            language,
            code,
        )


renderer_manager = RendererManager()
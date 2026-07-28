import importlib

from pathlib import Path
from core.logger import logger

class PluginManager:

    def __init__(
       self,
    ) -> None:

        self.plugins = {}

    def load(
        self,
    ) -> None:

        folder = Path("plugins")

        if not folder.exists():
            return

        for file in sorted(folder.iterdir()):

            if file.suffix != ".py":
                continue

            module_name = file.stem

            if module_name.startswith("_"):
                continue

            try:

                module = importlib.import_module(
                    f"plugins.{module_name}"
                )

                if hasattr(module, "register"):

                    module.register()

                    self.plugins[module_name] = module

                    logger.info(
                        f"Loaded plugin: {module_name}"
                    )

            except Exception:

                logger.exception(
                    f"Plugin Error ({module_name})"
                )

    def loaded(
        self,
    ) -> tuple[str, ...]:

        return tuple(sorted(self.plugins))


plugin_manager = PluginManager()

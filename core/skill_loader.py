import importlib

from pathlib import Path
from core.logger import logger
from core.action_engine import action_engine


class SkillLoader:

    def __init__(
       self,
    ) -> None:

        self.skills: dict[str, object] = {}

    def load(
        self,
    ) -> None:

        folder = Path("skills")

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
                    f"skills.{module_name}"
                )

                if hasattr(module, "INTENT") and hasattr(module, "handle"):

                    action_engine.register(
                        module.INTENT,
                        module.handle,
                    )

                    self.skills[module.INTENT] = module

                    logger.info(
                        f"Loaded Skill : {module.INTENT}"
                    )

            except Exception:

                logger.exception(
                    f"Skill Error ({module_name})"
                )

    def loaded(
        self,
    ) -> tuple[str, ...]:

        return tuple(sorted(self.skills))


skill_loader = SkillLoader()

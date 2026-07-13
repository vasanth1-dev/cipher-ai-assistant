import importlib
import os

from core.action_engine import action_engine


class SkillLoader:

    def __init__(self):

        self.skills = {}

    def load(self):

        folder = "skills"

        if not os.path.exists(folder):
            return

        for file in os.listdir(folder):

            if not file.endswith(".py"):
                continue

            if file.startswith("_"):
                continue

            module_name = file[:-3]

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

                    print(
                        f"Loaded Skill : {module.INTENT}"
                    )

            except Exception as e:

                print(
                    f"Skill Error ({module_name}) : {e}"
                )

    def loaded(self):

        return list(self.skills.keys())


skill_loader = SkillLoader()

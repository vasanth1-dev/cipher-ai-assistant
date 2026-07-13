import importlib
import os


class PluginManager:

    def __init__(self):

        self.plugins = {}

    def load(self):

        folder = "plugins"

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
                    f"plugins.{module_name}"
                )

                if hasattr(module, "register"):

                    module.register()

                    self.plugins[module_name] = module

                    print(f"Loaded Plugin : {module_name}")

            except Exception as e:

                print(
                    f"Plugin Error ({module_name}) : {e}"
                )

    def loaded(self):

        return list(self.plugins.keys())


plugin_manager = PluginManager()

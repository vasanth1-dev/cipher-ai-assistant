import traceback

from gui.app import CipherApp

from services.startup_service import startup_service
from services.scheduler_service import scheduler_service
from services.model_preloader import preload
from core.plugin_manager import plugin_manager
from core.skill_loader import skill_loader


def startup_check():

    print("\n========== Cipher Startup Check ==========\n")

    for name, status in startup_service.check():

        icon = "✅" if status else "❌"

        print(f"{icon} {name}")

    print("\n==========================================\n")


def initialize():

    startup_check()

    scheduler_service.start()

    plugin_manager.load()

    skill_loader.load()

    print("Loading AI model...")

    preload()

    print("AI Ready.")


def main():

    try:

        initialize()

        app = CipherApp()

        app.run()

    except KeyboardInterrupt:

        print("\nShutting down Cipher...")

    except Exception:

        print("\nFatal Error!\n")

        traceback.print_exc()


if __name__ == "__main__":

    main()
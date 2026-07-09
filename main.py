import traceback

from gui.app import CipherApp

from services.application_bootstrap import ApplicationBootstrap
from services.health_monitor import HealthMonitor
from services.performance_monitor import PerformanceMonitor

from services.startup_service import startup_service
from services.scheduler_service import scheduler_service

from services.model_preloader import preload

from core.plugin_manager import plugin_manager
from core.skill_loader import skill_loader


# --------------------------------------------------
# Startup Checks
# --------------------------------------------------

def startup_check():

    print("\n========== Cipher Startup Check ==========\n")

    for name, status in startup_service.check():

        icon = "✅" if status else "❌"

        print(f"{icon} {name}")

    print("\n==========================================\n")


# --------------------------------------------------
# Initialization
# --------------------------------------------------

def initialize():

    startup_check()

    # Existing services
    scheduler_service.start()

    plugin_manager.load()

    try:
        from plugins import plugin_manager as new_plugin_manager
        new_plugin_manager.start()
    except Exception as e:
        print(f"Plugin Framework Error: {e}")

    skill_loader.load()

    print("Loading AI model...")

    preload()

    print("AI Ready.")

    # --------------------------------------------------
    # New Runtime Bootstrap
    # --------------------------------------------------

    bootstrap = ApplicationBootstrap()

    if bootstrap.initialize():

        runtime = bootstrap.runtime()

        print(
            f"Runtime initialized with "
            f"{len(runtime['plugin_manager'].names())} plugins."
        )

    else:

        print("Warning: Runtime bootstrap failed.")

    return bootstrap


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    bootstrap = None

    health_monitor = HealthMonitor()

    performance_monitor = PerformanceMonitor()

    try:

        with performance_monitor.measure():

            bootstrap = initialize()

            health_monitor.heartbeat()

            app = CipherApp()

            app.run()

    except KeyboardInterrupt:

        print("\nShutting down Cipher...")

        try:
            scheduler_service.stop()
        except Exception:
            traceback.print_exc()

        if bootstrap is not None:

            try:
                bootstrap.shutdown()

            except Exception:
                traceback.print_exc()

    except Exception:

        print("\nFatal Error!\n")

        traceback.print_exc()

    finally:

        try:
            scheduler_service.stop()
        except Exception:
            traceback.print_exc()

        if bootstrap is not None:

            try:

                bootstrap.shutdown()

            except Exception:

                traceback.print_exc()

        print("\nCipher stopped.")


if __name__ == "__main__":

    main()
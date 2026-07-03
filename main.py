import traceback

from core.assistant import Cipher


def main():
    assistant = Cipher()

    try:
        assistant.run()

    except KeyboardInterrupt:
        print("\n\nCipher stopped by user.")

    except Exception:
        print("\n===== FATAL ERROR =====")
        traceback.print_exc()


if __name__ == "__main__":
    main()
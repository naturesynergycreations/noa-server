import sys
from PySide6.QtWidgets import QApplication

from gui import VoiceAssistant


def main():
    app = QApplication(sys.argv)

    window = VoiceAssistant()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
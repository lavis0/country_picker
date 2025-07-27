"""Establish the event loop and shows the main window of the application."""

import sys
from PyQt6.QtWidgets import QApplication
from gui import MainWindow


def run_app() -> int:
    """Run the country picker application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()

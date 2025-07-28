"""Establish the event loop and shows the main window of the application."""

import sys
from PyQt6.QtWidgets import QApplication
from .cli import parse_args
from .gui import MainWindow


def run_app(preselected_country=parse_args()) -> int:
    """Run the country picker application."""
    app = QApplication(sys.argv)
    window = MainWindow(preselected_country=preselected_country)
    window.show()
    return app.exec()

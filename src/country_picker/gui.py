"""GUI logic for the application."""

from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    """Main window of the country picker application."""

    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        ui_path = Path(__file__).parent / "resources" / "MainWindow.ui"
        uic.loadUi(ui_path, self)

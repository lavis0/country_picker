"""GUI logic for the application."""

import json
from pathlib import Path
from PyQt6 import uic
from PyQt6.QtCore import QByteArray, QUrl
from PyQt6.QtGui import QShowEvent
from PyQt6.QtNetwork import (QNetworkAccessManager,
                             QNetworkReply,
                             QNetworkRequest)
from PyQt6.QtWidgets import QMainWindow, QComboBox, QLabel, QMessageBox

_api_url = "https://www.apicountries.com/countries"


class MainWindow(QMainWindow):
    """Main window of the country picker application."""

    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        ui_path = Path(__file__).parent / "resources" / "MainWindow.ui"
        uic.loadUi(ui_path, self)

        self._combo: QComboBox = self.findChild(QComboBox, "countryComboBox")
        self._label: QLabel = self.findChild(QLabel, "selectionLabel")

        self._combo.setEnabled(False)  # Disabled until data is fetched
        self._combo.currentTextChanged.connect(
            lambda text: self._label.setText(
                f"Selected: {text}" if text else "")
        )

        self._qnam = QNetworkAccessManager()
        self._qnam.finished.connect(self._handle_response)

        # set a flag so the network request occurs after the window is shown
        self._has_fetched = False

    def showEvent(self, event: QShowEvent) -> None:
        """Network request on show event."""
        super().showEvent(event)
        if not self._has_fetched:
            self._has_fetched = True
            self._fetch_countries()

    def _fetch_countries(self) -> None:
        """Fetch country data from the API."""
        url = QUrl(_api_url)
        request = QNetworkRequest(url)
        self._qnam.get(request)

    def _handle_response(self, reply: QNetworkReply) -> None:
        """Handle the network response."""
        if reply.error() != QNetworkReply.NetworkError.NoError:
            QMessageBox.critical(self,
                                 "Error",
                                 f"Network error: {reply.errorString()}")
            reply.deleteLater()
            return

        try:
            # Capture raw data from the reply to parse later
            countries_data = reply.readAll()
            self._handle_data(countries_data)
        except Exception as e:
            QMessageBox.critical(self,
                                 "Error",
                                 f"Unexpected error: {e}")

        reply.deleteLater()

    def _handle_data(self, countries_data: QByteArray) -> None:
        """Handle raw data from the network reply."""
        try:
            countries_json = json.loads(countries_data.data().decode('utf-8'))

            names = []
            for c in countries_json:
                n = c.get("name")
                if isinstance(n, dict):
                    cn = n.get("common")
                    if isinstance(cn, str):
                        names.append(cn)
                elif isinstance(n, str):
                    names.append(n)
            countries_sorted = sorted(names)

            self._populate(countries_sorted)
        except json.JSONDecodeError as e:
            QMessageBox.critical(self, "Error", f"JSON parsing error: {e}")

    def _populate(self, countries: list[str]) -> None:
        """Populate the combo box with country names."""
        # self._combo.clear()
        self._combo.addItem("")
        self._combo.addItems(countries)
        self._combo.setEnabled(True)

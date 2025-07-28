"""GUI logic for the application."""

import json
from pathlib import Path
from PyQt6 import uic
from PyQt6.QtCore import QByteArray, QObject, QThread, QUrl, pyqtSignal, \
    pyqtSlot
from PyQt6.QtGui import QShowEvent
from PyQt6.QtNetwork import (QNetworkAccessManager,
                             QNetworkReply,
                             QNetworkRequest)
from PyQt6.QtWidgets import QMainWindow, QComboBox, QLabel, QMessageBox

_api_url = "https://www.apicountries.com/countries"


class DataWorker(QObject):
    """Worker class for downloading and handling data."""

    resultReady = pyqtSignal(list)
    errorOccurred = pyqtSignal(str)

    def __init__(self):
        """Initialize the data worker."""
        super().__init__()
        self._qnam = QNetworkAccessManager(self)
        self._qnam.finished.connect(self._handle_response)

    @pyqtSlot()
    def fetch_countries(self):
        """Fetch country data from the API."""
        url = QUrl(_api_url)
        request = QNetworkRequest(url)
        self._qnam.get(request)

    @pyqtSlot(QNetworkReply)
    def _handle_response(self, reply: QNetworkReply) -> None:
        """Handle the network response."""
        if reply.error() != QNetworkReply.NetworkError.NoError:
            self.errorOccurred.emit(reply.errorString())
            reply.deleteLater()
            return

        try:
            # Capture raw data from the reply to parse later
            countries_data = reply.readAll()
            self._handle_data(countries_data)
        except Exception as e:
            self.errorOccurred.emit(str(e))

        reply.deleteLater()

    def _handle_data(self, countries_data: QByteArray) -> None:
        """Handle raw data from the network reply."""
        try:
            countries_json = json.loads(countries_data.data().decode('utf-8'))

            # Extract country names from the JSON data
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
            self.resultReady.emit(countries_sorted)
        except json.JSONDecodeError as e:
            self.errorOccurred.emit(str(e))


class MainWindow(QMainWindow):
    """Main window of the country picker application."""

    def __init__(self, preselected_country: str):
        """Initialize the main window."""
        super().__init__()
        ui_path = Path(__file__).parent / "resources" / "MainWindow.ui"
        uic.loadUi(ui_path, self)

        self._combo: QComboBox = self.findChild(QComboBox, "countryComboBox")
        self._label: QLabel = self.findChild(QLabel, "selectionLabel")

        self._preselected_country = preselected_country

        self._combo.setEnabled(False)  # Disabled until data is fetched
        self._combo.currentTextChanged.connect(
            lambda text: self._label.setText(
                f"Selected: {text}" if text else "")
        )

        # set a flag so the network request occurs after the window is shown
        self._has_fetched = False

    def showEvent(self, event: QShowEvent) -> None:
        """Network request on show event."""
        super().showEvent(event)
        if not self._has_fetched:
            self._has_fetched = True
            self._start_worker()

    def _start_worker(self) -> None:
        """Start the data worker to fetch and parse country data."""
        self._thread = QThread(parent=self)
        self._worker = DataWorker()
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.fetch_countries)

        self._worker.resultReady.connect(self._populate)
        self._worker.errorOccurred.connect(self._handle_error)

        self._thread.finished.connect(self._thread.deleteLater)
        self._worker.resultReady.connect(self._worker.deleteLater)
        self._worker.errorOccurred.connect(self._worker.deleteLater)

        self._thread.start()

    def _populate(self, countries: list[str]) -> None:
        """Populate the combo box with country names."""
        # self._combo.clear()
        if self._thread:
            self._thread.quit()
        self._combo.addItem("")
        self._combo.addItems(countries)
        self._combo.setEnabled(True)

        self._preselect_country()

    def _preselect_country(self) -> None:
        """Preselect a country if specified (case-insensitive, startswith)."""
        if not self._preselected_country:
            return

        target = self._preselected_country.lower()
        found_index = -1

        # Find the index of the preselected country (case-insensitive)
        for i in range(self._combo.count()):
            item_text = self._combo.itemText(i).lower()
            if item_text == target:
                found_index = i
                break

        if found_index >= 0:
            self._combo.setCurrentIndex(found_index)

    def _handle_error(self, error_message: str) -> None:
        """Handle errors by showing a message box."""
        if self._thread:
            self._thread.quit()
        QMessageBox.critical(self, "Error", f"Error: {error_message}")

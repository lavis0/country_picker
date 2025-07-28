# Country Picker

A PyQt6-based GUI application for selecting countries from a dropdown list.

## Installation

Install from TestPyPI:
```bash
pip install --index-url https://test.pypi.org/simple/ --no-deps country-picker==0.1.0
```

Or install from source:
```bash
git clone https://www.github.com/lavis0/country-picker.git
cd country-picker
pip install .
```

## Usage

Get dependencies (perhaps, in a virtual environment):
```bash
pip install PyQt6
```

Run the application:
```bash
python -m country_picker
```

Or with a preselected country:
```bash
python -m country_picker --country "Switzerland"
```

## Requirements

- Python 3.9+
- PyQt6

import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QComboBox, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtGui import QDoubleValidator
from locale import setlocale, atof, LC_ALL
from google_currency import convert


class Window(QWidget):

    currencies = [
        "USD",
        "EUR",
        "GBP",
        "CAD",
        "JPY",
        "CHF",
        "AUD",
        "INR",
        "NZD",
        "ZAR",
        "RMB",
        "SGD",
        "HKD"
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Currency Converter")
        self.vbox = QVBoxLayout()
        self.grid = QGridLayout()

        self.from_options = QComboBox()
        self.from_options.addItems(self.currencies)
        self.from_options.currentIndexChanged.connect(self.convert_currency)
        self.to_options = QComboBox()
        self.to_options.addItems(self.currencies)
        self.to_options.currentIndexChanged.connect(self.convert_currency)
        self.grid.addWidget(self.from_options, 1, 1)
        self.grid.addWidget(self.to_options, 3, 1)

        self.input = QLineEdit()
        self.input.setValidator(QDoubleValidator())
        self.input.setMaxLength(14)
        self.input.returnPressed.connect(self.convert_currency)
        self.output = QLineEdit()
        self.output.setValidator(QDoubleValidator())
        self.output.setReadOnly(True)
        self.grid.addWidget(self.input, 1, 2)
        self.grid.addWidget(self.output, 3, 2)

        self.switch = QPushButton("⇅")
        self.switch.clicked.connect(self.swap_currency)
        self.grid.addWidget(self.switch, 2, 1)

        self.vbox.addLayout(self.grid)
        self.vbox.addStretch()

        self.btn = QPushButton("Convert")
        self.btn.setAutoDefault(True)
        self.btn.clicked.connect(self.convert_currency)
        self.vbox.addWidget(self.btn)

        self.setLayout(self.vbox)

    def swap_currency(self):
        temp = self.from_options.currentIndex()
        self.from_options.setCurrentIndex(self.to_options.currentIndex())
        self.to_options.setCurrentIndex(temp)

    def convert_currency(self):
        if self.input.text():
            currency_json = json.loads(convert(self.from_options.currentText(
            ), self.to_options.currentText(), atof(self.input.text())))
            self.output.setText(f"{float(currency_json['amount']):.2f}")
        else:
            self.output.setText("")


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    try:
        setlocale(LC_ALL, "en_US.utf8")
    except Exception:
        try:
            setlocale(LC_ALL, "en_US.UTF-8")
        except Exception as e:
            print(f"{e}\nErr#000: locale error.")

    main()

import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit
from PySide6.QtGui import QCloseEvent

from password_generator.ui.ui_main import Ui_MainWindow
import password_generator.ui.resource

import buttons
import password


class PasswordGenerator(QMainWindow):
    def __init__(self):
        super(PasswordGenerator, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        for btn in buttons.GENERATE_PASSWORD:
            getattr(self.ui, btn).clicked.connect(self.set_password)

        self.update_slider()
        self.set_password()
        self.copy_to_clipboard()

    def update_slider(self) -> None:
        self.ui.slider_length.valueChanged.connect(self.ui.spinbox_length.setValue)
        self.ui.spinbox_length.valueChanged.connect(self.ui.slider_length.setValue)
        self.ui.spinbox_length.valueChanged.connect(self.set_password)

    def get_chars(self) -> str:
        chars = ''
        for btn in buttons.Characters:
            if getattr(self.ui, btn.name).isChecked():
                chars += btn.value
        return chars

    def set_password(self) -> None:
        try:
            self.ui.line_password.setText(
                password.new_password(length=self.ui.slider_length.value(), chars=self.get_chars())
            )
        except IndexError:
            self.ui.line_password.clear()

        self.set_entropy()
        self.set_strength()
            
    def get_char_num(self) -> int:
        num = 0
        for btn in buttons.CHARACTERS_NUMBER.items():
            if getattr(self.ui, btn[0]).isChecked():
                num += btn[1]
        return num

    def set_entropy(self) -> None:
        length = len(self.ui.line_password.text())
        char_num = self.get_char_num()

        self.ui.label_entropy.setText(
            f'Entropy: {password.get_entropy(length, char_num)} bit'
        )

    def set_strength(self):
        length = len(self.ui.line_password.text())
        char_num = self.get_char_num()

        for complexity in password.PasswordComplexity:
            if password.get_entropy(length, char_num) >= complexity.value:
                self.ui.label_strength.setText(f'Strength: {complexity.name}')

    def copy_to_clipboard(self) -> None:
        QApplication.clipboard().setText(self.ui.line_password.text())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = PasswordGenerator()
    window.show()

    sys.exit(app.exec())

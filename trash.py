from PyQt6.QtWidgets import *
import sys

class CustomDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Dialog")

        buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        button = QPushButton('Click Me')
        button.clicked.connect(CustomDialog.button_clicked)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Do you want to proceed?"))
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

 
    def button_clicked():
        print('Button was clicked!')

app = QApplication([])
app.setStyleSheet("""
    QPushButton{
        background-color: #0078d7;
        color: write;
        border-radius: 4px;
        padding: 6px;
    }
    QPushButton:hover{
        background-color: #0053a6;
    }
""")

# button.show()
window = CustomDialog()
window.show()

sys.exit(app.exec())

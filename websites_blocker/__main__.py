import sys
from PyQt6.QtWidgets import QApplication
from websites_blocker.main_window import MainWindow


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

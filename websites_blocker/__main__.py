import ctypes, sys
from PyQt6.QtWidgets import QApplication
from websites_blocker.main_window import MainWindow


if ctypes.windll.shell32.IsUserAnAdmin():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
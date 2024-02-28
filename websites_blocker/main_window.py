from sys import platform

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QTextEdit, QPushButton, QHBoxLayout, QWidget, QVBoxLayout, QMessageBox


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setMinimumSize(900, 850)
        self.setWindowTitle("Blokowanie stron internetowych")

        if platform == "linux":
            self.hosts_file = "/etc/hosts"
        elif platform == "win32":
            self.hosts_file = "C:\\Windows\\System32\\drivers\\etc\\hosts"
        else:
            self.hosts_file = "/etc/hosts"

        self.websites_are_blocked_str = "Następujące strony internetowe są zablokowane:"
        self.redirect_page = "127.0.0.1"
        self.blocked_websites = self.read_blocked_websites()

        self.central_widget = QWidget()
        self.websites = QTextEdit()
        self.block_button = QPushButton("Zablokuj")
        self.block_button.clicked.connect(self.block)
        self.unblock_button = QPushButton("Odblokuj")
        self.unblock_button.clicked.connect(self.unblock)
        self.update_button = QPushButton("Aktualizuj okno")
        self.update_button.clicked.connect(self.update)
        self.edit_widgets()

        self.central_layout = QVBoxLayout()
        self.control_bottom_panel = QHBoxLayout()
        self.edit_layouts()

        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)

    def edit_widgets(self):
        self.websites.setMinimumSize(450, 650)
        self.websites.setStyleSheet("font-size : 12pt")
        self.websites.setText(self.blocked_websites)
        self.block_button.setMinimumSize(140, 40)
        self.block_button.setMaximumSize(140, 40)
        self.block_button.setStyleSheet("border-radius : 9; border : 1px solid black; font-size : 11pt")
        self.unblock_button.setMinimumSize(140, 40)
        self.unblock_button.setMaximumSize(140, 40)
        self.unblock_button.setStyleSheet("border-radius : 9; border : 1px solid black; font-size : 11pt")
        self.update_button.setMinimumSize(140, 40)
        self.update_button.setMaximumSize(140, 40)
        self.update_button.setStyleSheet("border-radius : 9; border : 1px solid black; font-size : 11pt")

    def edit_layouts(self):
        self.control_bottom_panel.addWidget(self.block_button)
        self.control_bottom_panel.addWidget(self.unblock_button)
        self.control_bottom_panel.addWidget(self.update_button)
        self.central_layout.addSpacing(45)
        self.central_layout.addWidget(self.websites, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.central_layout.addLayout(self.control_bottom_panel)
        self.central_layout.addSpacing(43)

    def read_blocked_websites(self):
        with open(self.hosts_file, 'r') as file:
            content_of_hosts_file = file.readlines()

        blocked_websites = self.websites_are_blocked_str + "\n"
        for line in content_of_hosts_file:
            if line.startswith(self.redirect_page):
                blocked_websites += line
        blocked_websites = blocked_websites.replace(f"{self.redirect_page} ", "")
        return blocked_websites

    def read_from_qtextedit_and_edit(self):
        websites = self.websites.toPlainText()
        websites = websites.replace(self.websites_are_blocked_str, "")
        websites_list = websites.split()
        websites_list = [website.replace("https://", "").replace(",", "") for website in websites_list]

        return websites_list

    def block(self):
        websites_list = self.read_from_qtextedit_and_edit()
        with open(self.hosts_file, 'r+') as file:
            content_of_hosts_file = file.read()
            for website in websites_list:
                if website not in content_of_hosts_file:
                    file.write(self.redirect_page + " " + website + "\n")

        QMessageBox.information(self, "Strony zablokowane",
                                "Strony internetowe podane w oknie aplikacji zostały zablokowane",
                                buttons=QMessageBox.StandardButton.Ok)

    def unblock(self):
        website_list = self.read_from_qtextedit_and_edit()
        with open(self.hosts_file, 'r+') as file:
            content_of_hosts_file = file.readlines()
            file.seek(0)
            for line in content_of_hosts_file:
                if not any(website in line for website in website_list):
                    file.write(line)

            file.truncate()
            QMessageBox.information(self, "Strony odblokowane",
                                    "Strony internetowe podane w oknie aplikacji zostały odblokowane",
                                    buttons=QMessageBox.StandardButton.Ok)

    def update(self):
        self.blocked_websites = self.read_blocked_websites()
        self.websites.setText(self.blocked_websites)
        QMessageBox.information(self, "Okno aplikacji uaktualnione", "Okno aplikacji zostało uaktualnione",
                                buttons=QMessageBox.StandardButton.Ok)

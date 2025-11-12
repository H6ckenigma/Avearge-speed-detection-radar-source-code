#The GUI

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

class RadarGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Radar System")
        self.setGeometry(100, 100, 900, 700)

        #Dark BG
        self.setStyleSheet("background-color: #1a1a1a; color: #00ff00;")

        #widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        #title
        title = QLabel("Radar SyS")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)

        #Test
        test = QLabel("GUI loading...")
        test.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(test)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RadarGUI()
    window.show()
    sys.exit(app.exec())


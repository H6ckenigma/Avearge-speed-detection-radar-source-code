#The GUI

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt

class RadarGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Radar System")
        self.setGeometry(100, 100, 900, 700)

        #Dark BG
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0a0a0a,
                    stop:1 #1a1a1a
                );        
            }
        """)

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

        from radar_conf import Distance, Speed_limit

        info_layout = QHBoxLayout()
        self.distance_label = QLabel(f"Distance : {Distance} km")
        self.speedlimit_label = QLabel(f"Speed Limit: {Speed_limit}")
        info_layout.addWidget(self.distance_label)
        info_layout.addWidget(self.speedlimit_label)
        layout.addLayout(info_layout)

        #Buttons
        button_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start sim")
        self.stop_btn = QPushButton("Stop Sim")

        self.stop_btn.setEnabled(False)
        # Styling the button
        btn_style = """
            QPushButton {
                background-color: #2d2d2d;
                color: #00ff00
                border: 2px solid #00ff00;
                padding: 12px;
                font-size: 14px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #00ff00
                color: #1a1a1a;
            }
            QPushButton:disabled {
                color: #555555;
                border-color: #555555;
            }
        """
        self.start_btn.setStyleSheet(btn_style)
        self.stop_btn.setStyleSheet(btn_style)
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.stop_btn)
        layout.addLayout(button_layout)

        # Status Message
        self.status = QLabel("Ready")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status.setStyleSheet("margin-top: 20px; font-style: italic")
        layout.addWidget(self.status)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RadarGUI()
    window.show()
    sys.exit(app.exec())
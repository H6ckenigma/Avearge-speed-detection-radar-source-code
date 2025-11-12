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
        main_widget.setStyleSheet("background: transparent;")
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)
        layout.setSpacing(25)
        layout.setContentsMargins(40, 30, 40, 30)

        #title
        title = QLabel("Radar Sys")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #00ff00;
            letter-spacing: 4px;
            margin: 20px;
            padding: 15px;
            background: rgba(0, 255, 0, 0.05);
            border: 2px solid #00ff00;
            border-radius: 12px;
            """)
        layout.addWidget(title)

        from radar_conf import Distance, Speed_limit

        info_layout = QHBoxLayout()
        info_layout.setSpacing(20)

        self.distance_label = QLabel(f"Distance : {Distance} km")
        self.speedlimit_label = QLabel(f"Speed Limit: {Speed_limit}")
        info_style= """
            QLabel {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(0, 255, 0, 0.1),
                    stop:1 rgba(0, 255, 0, 0.05)
                );
                color: #00ff00;
                font-size: 16px;
                font-weight: 600;
                padding: 20px 30px;
                border: 2px solid rgba(0, 255, 0, 0.3);
                border-left: 4px solid #00ff00;
                border-radius: 20px;
                letter-spacing: 1px;
            }
        """
        self.distance_label.setStyleSheet(info_style)
        self.speedlimit_label.setStyleSheet(info_style)
        info_layout.addWidget(self.distance_label)
        info_layout.addWidget(self.speedlimit_label)
        layout.addLayout(info_layout)

        layout.addSpacing(20)
        #Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(30)
        self.start_btn = QPushButton("Start sim")
        self.stop_btn = QPushButton("Stop Sim")

        self.stop_btn.setEnabled(False)
        # Style the button with animation
        btn_style = """
        QPushButton {
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #2d2d2d,
                stop:1 #1a1a1a
            );
            color: #00ff00;
            border: 2px solid #00ff00;
            padding: 18px 40px;
            font-size: 15px;
            font-weight: bold;
            letter-spacing: 2px;
            border-radius: 12px;
        }
        QPushButton:hover {
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #00ff00,
                stop:1 #00cc00
            );
            color: #000000;
            border: 2px solid #00ff00;
        }
        QPushButton:pressed {
            background: #00cc00;
            padding: 20px 40px 16px 40px;
        }
        QPushButton:disabled {
            background: #1a1a1a;
            color: #333333;
            border: 2px solid #333333;
        }

"""
        self.start_btn.setStyleSheet(btn_style)
        self.stop_btn.setStyleSheet(btn_style)
        self.start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.stop_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.stop_btn)
        layout.addLayout(button_layout)

        layout.addSpacing(20)
        
        # Status Message
        self.status = QLabel("Ready")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status.setStyleSheet("""
            QLabel {
                background: rgba(0, 255, 0, 0.08);
                color: #00ff00;
                font-size: 14px;
                font-style: italic;
                font-weight:500;
                padding: 15px;
                border: 1px solid rgba(0, 255, 0, 0.2);
                border-radius: 8px;
                letter-spacing:1px;
            }
        """)
        layout.addWidget(self.status)
        layout.addStretch()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RadarGUI()
    window.show()
    sys.exit(app.exec())
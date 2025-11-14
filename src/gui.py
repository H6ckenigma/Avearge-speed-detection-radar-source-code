#The GUI

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QTextEdit
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
                    stop:0 #0d1b2a,
                    stop:1 #1b263b
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
            color: #e0e1dd;
            letter-spacing: 4px;
            margin: 20px;
            padding: 15px;
            background: rgba(58, 134, 255, 0.08);
            border: 2px solid #3a86ff;
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
                    stop:0 rgba(255, 183, 3, 0.18),
                    stop:1 rgba(255, 183, 3, 0.1)
                );
                color: #e0e1dd;
                font-size: 16px;
                font-weight: 600;
                padding: 20px 30px;
                border: 2px solid rgba(58, 134, 255, 0.4);
                border-left: 4px solid #3a86ff;
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
                stop:0 #3a86ff,
                stop:1 #1d5fcf
            );
            color: #e0e1dd;
            border: 2px solid #3a86ff;
            padding: 18px 40px;
            font-size: 15px;
            font-weight: bold;
            letter-spacing: 2px;
            border-radius: 12px;
        }
        QPushButton:hover {
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #ffb703,
                stop:1 #e09a03
            );
            color: #000000;
            border: 2px solid #ffb703;
        }
        QPushButton:pressed {
            background: #e09a03;
            padding: 20px 40px 16px 40px;
        }
        QPushButton:disabled {
            background: #415a77;
            color: #8d99ae;
            border: 2px solid #778da9;
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
                background: rgba(255, 183, 3, 0.12);
                color: #e0e1dd;
                font-size: 14px;
                font-style: italic;
                font-weight:500;
                padding: 15px;
                border: 1px solid rgba(58, 134, 255, 0.3);
                border-radius: 8px;
                letter-spacing:1px;
            }
        """)
        layout.addWidget(self.status)
        log_label = QLabel("Live Detections")
        log_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        log_label.setStyleSheet("""
            QLabel {
                color: #e0e1dd;
                font-size: 18px;
                font-weight: bold;
                margin: 15px 0 10px 0;
                letter-spacing:3px;
                }
        """)
        layout.addWidget(log_label)

        self.live_log = QTextEdit()
        self.live_log.setReadOnly(True)
        self.live_log.setMaximumHeight(180)
        self.live_log.setStyleSheet("""
            QTextEdit{
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0f0f0f,
                    stop:1 #0a0a0a);                    
                color: #00ff00;
                border: 2px solid #00ff00;
                border-radius: 12px;
                padding: 15px;
                font-family: Consolas, monospace;
                font-size: 12px;
                letter-spacing: 0.5px;
                }

        """)
        self.live_log.append("Waiting for the simulation to start...")
        layout.addWidget(self.live_log)
        
        layout.addStretch()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RadarGUI()
    window.show()
    sys.exit(app.exec())
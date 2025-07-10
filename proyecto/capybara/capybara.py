
import sys
import os
import time
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

class CapybaraMascot(QLabel):
    def __init__(self):
        super().__init__()

        base_path = os.path.dirname(os.path.abspath(__file__))

        self.happy_pix = QPixmap(os.path.join(base_path, "happy.png"))
        self.sleep_pix = QPixmap(os.path.join(base_path, "sleep.png"))
        self.sad_pix = QPixmap(os.path.join(base_path, "sad.png"))
        self.surprise_pix = QPixmap(os.path.join(base_path, "surprise.png"))

        for name, pix in [("happy", self.happy_pix), ("sleep", self.sleep_pix), ("sad", self.sad_pix), ("surprise", self.surprise_pix)]:
            if pix.isNull():
                print(f"Error: imagen '{name}.png' no pudo cargarse. Revisa el archivo y la ruta.")
                sys.exit(1)

        self.setPixmap(self.sleep_pix)  # Empieza durmiendo
        self.setFixedSize(self.sleep_pix.size())
        self.move(100, 100)
        self.show()

        self.last_activity_time = time.time()
        self.surprise_start_time = None
        self.surprise_duration = 5
        self.drag_position = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_state)
        self.timer.start(100)

        # Label para mostrar texto que "dice"
        self.dialog_label = QLabel(self)
        self.dialog_label.setStyleSheet(
            "background-color: white; border-radius: 10px; padding: 5px; font-size: 12pt;")
        self.dialog_label.setWordWrap(True)
        self.dialog_label.move(0, -50)
        self.dialog_label.resize(200, 50)
        self.dialog_label.hide()

    def say(self, text):
        self.dialog_label.setText(text)
        self.dialog_label.show()
        self.wake_up()

    def stop_saying(self):
        self.dialog_label.hide()

    def reset_timer(self):
        self.last_activity_time = time.time()

    def wake_up(self):
        # Cambia a feliz cuando está activo
        self.setPixmap(self.happy_pix)
        self.last_activity_time = time.time()

    def sleep(self):
        self.setPixmap(self.sleep_pix)

    def mousePressEvent(self, event):
        self.reset_timer()
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.reset_timer()
        if event.buttons() == Qt.LeftButton and self.drag_position is not None:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.reset_timer()
        if event.button() == Qt.LeftButton:
            if self.drag_position is not None:
                moved = event.globalPos() != (self.frameGeometry().topLeft() + self.drag_position)
                if not moved:
                    self.show_surprise()
            self.drag_position = None
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        self.reset_timer()
        super().keyPressEvent(event)

    def show_surprise(self):
        self.setPixmap(self.surprise_pix)
        self.surprise_start_time = time.time()

    def update_state(self):
        current_time = time.time()

        if self.surprise_start_time is not None:
            if current_time - self.surprise_start_time < self.surprise_duration:
                return
            else:
                self.surprise_start_time = None

        elapsed = current_time - self.last_activity_time

        if elapsed < 30:
            pix = self.happy_pix
        elif elapsed < 120:
            pix = self.sleep_pix
        else:
            pix = self.sad_pix

        if self.pixmap() != pix:
            self.setPixmap(pix)

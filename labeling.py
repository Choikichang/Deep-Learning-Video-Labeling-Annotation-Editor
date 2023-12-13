import sys
import cv2
import json
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog, QLineEdit, QHBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)

    def set_video_path(self, video_path):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(self.video_path)
        self.frame_number = 0

    def run(self):
        self.next_frame()

    def next_frame(self):
        if self.cap.isOpened():
            ret, cv_img = self.cap.read()
            if ret:
                self.frame_number += 1
                qt_img = self.convert_cv_qt(cv_img)
                self.change_pixmap_signal.emit(qt_img)

    @staticmethod
    def convert_cv_qt(cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        return convert_to_Qt_format.scaled(640, 480, Qt.KeepAspectRatio)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Labeler")
        self.disply_width = 640
        self.display_height = 480

        # Create widgets
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)

        self.btn_select = QPushButton('Select Video', self)
        self.btn_select.clicked.connect(self.select_video)

        self.btn_next_frame = QPushButton('Next Frame', self)
        self.btn_next_frame.clicked.connect(self.next_frame)

        self.start_frame_input = QLineEdit(self)
        self.end_frame_input = QLineEdit(self)
        self.label_input = QLineEdit(self)

        self.btn_label = QPushButton('Label', self)
        self.btn_label.clicked.connect(self.label_video)

        # Set layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.btn_select)

        hbox = QHBoxLayout()
        hbox.addWidget(self.btn_next_frame)
        vbox.addLayout(hbox)

        label_box = QHBoxLayout()
        label_box.addWidget(QLabel('Start Frame:'))
        label_box.addWidget(self.start_frame_input)
        label_box.addWidget(QLabel('End Frame:'))
        label_box.addWidget(self.end_frame_input)
        label_box.addWidget(QLabel('Label:'))
        label_box.addWidget(self.label_input)
        vbox.addLayout(label_box)

        vbox.addWidget(self.btn_label)
        self.setLayout(vbox)

        # Create a thread
        self.thread = VideoThread()

    @pyqtSlot()
    def select_video(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Video")
        if filename != '':
            self.thread.set_video_path(filename)
            self.thread.change_pixmap_signal.connect(self.update_image)
            self.thread.start()

    @pyqtSlot(QImage)
    def update_image(self, qt_img):
        self.image_label.setPixmap(QPixmap.fromImage(qt_img))

    @pyqtSlot()
    def next_frame(self):
        self.thread.next_frame()

    @pyqtSlot()
    def label_video(self):
        start_frame = self.start_frame_input.text()
        end_frame = self.end_frame_input.text()
        label = self.label_input.text()
        # Save the labels to a file or process them as needed
        QMessageBox.information(self, "Info", f"Labeled from frame {start_frame} to {end_frame} with label {label}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
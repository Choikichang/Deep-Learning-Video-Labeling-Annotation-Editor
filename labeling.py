import sys
import cv2
import json
import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel,\
     QFileDialog, QLineEdit, QHBoxLayout, QMessageBox, QShortcut
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap, QKeySequence

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)
    video_total_frames_signal = pyqtSignal(int)
    video_current_frame_signal = pyqtSignal(int)
    video_height_signal = pyqtSignal(int)
    video_width_signal = pyqtSignal(int)

    def set_video_path(self, video_path):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            print("Error: Unable to open video file.")
            return
        self.frame_number = 0
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.video_total_frames_signal.emit(self.total_frames)
        self.video_height_signal.emit(self.frame_height)
        self.video_width_signal.emit(self.frame_width)


# When Operate start show first frame!
    def run(self):
        self.next_frame()

    def next_frame(self):
        if self.cap.isOpened():
            ret, cv_img = self.cap.read()
            if ret:
                self.frame_number += 1
                qt_img = self.convert_cv_qt(cv_img)
                self.change_pixmap_signal.emit(qt_img)
                frame_number = self.frame_number
                self.video_current_frame_signal.emit(frame_number)
                # self.video_total_frames_signal.emit(self.total_frames)
                # self.video_height_signal.emit(self.frame_height)
                # self.video_width_signal.emit(self.frame_width)

    def before_frame(self):
        if self.cap.isOpened() and self.frame_number > 1:
            self.frame_number -= 2
            # self.cap.read() going front so I need to set frame number once
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.frame_number)
            ret, cv_img = self.cap.read()
            if ret:
                self.frame_number += 1
                qt_img = self.convert_cv_qt(cv_img)
                self.change_pixmap_signal.emit(qt_img)
                # frame_number = self.frame_number
                self.video_current_frame_signal.emit(self.frame_number)
        
    def stop(self):
        self.cap.release()
        self.quit()
        self.wait()

    @staticmethod
    def convert_cv_qt(cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        return convert_to_Qt_format.scaled(1280, 960, Qt.KeepAspectRatio)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Labeler")
        self.display_width = 1280
        self.display_height = 600

        self.video_paths = []
        self.current_video_index = 0

        # Create widgets
        self.btn_select_video = QPushButton('Select Video', self)
        self.btn_select_video.clicked.connect(self.select_video)

        self.video_info_label = QLabel('Video Information: None', self)
        self.image_label = QLabel(self)
        # self.image_label.setFixedSize(self.display_width, self.display_height)

        self.btn_prev_video = QPushButton('Previous Video', self)
        self.btn_prev_video.clicked.connect(self.prev_video)

        self.btn_next_video = QPushButton('Next Video', self)
        self.btn_next_video.clicked.connect(self.next_video)

        self.btn_before_frame = QPushButton('Before frame', self)
        self.btn_before_frame.clicked.connect(self.before_frame)

        self.btn_next_frame = QPushButton('Next Frame', self)
        self.btn_next_frame.clicked.connect(self.next_frame)

        self.start_frame_input = QLineEdit(self)
        self.label_frame_count = QLineEdit(self)
        self.label_frame_count.setText('60')

        self.btn_label = QPushButton('Label', self)
        self.btn_label.clicked.connect(self.label_video)


        # Add Short cut key Q E I P O
        
        self.shortcut_before_frame = QShortcut(QKeySequence("Q"), self)
        self.shortcut_before_frame.activated.connect(self.before_frame)

        self.shortcut_next_frame = QShortcut(QKeySequence("E"), self)
        self.shortcut_next_frame.activated.connect(self.next_frame)

        self.shortcut_prev_video = QShortcut(QKeySequence("I"), self)
        self.shortcut_prev_video.activated.connect(self.prev_video)

        self.shortcut_next_video = QShortcut(QKeySequence("P"), self)
        self.shortcut_next_video.activated.connect(self.next_video)

        self.shortcut_label_video = QShortcut(QKeySequence("O"), self)
        self.shortcut_label_video.activated.connect(self.label_video)

        # Set layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.video_info_label)

        hbox = QHBoxLayout()
        hbox.addWidget(self.btn_select_video)
        hbox.addWidget(self.btn_prev_video)
        hbox.addWidget(self.btn_next_video)
        vbox.addLayout(hbox)

        hbox = QHBoxLayout()
        hbox.addWidget(self.btn_before_frame)
        hbox.addWidget(self.btn_next_frame)
        vbox.addLayout(hbox)

        label_box = QHBoxLayout()
        label_box.addWidget(QLabel('Start Frame:'))
        label_box.addWidget(self.start_frame_input)
        label_box.addWidget(QLabel('Label Frame Count:'))
        label_box.addWidget(self.label_frame_count)
        vbox.addLayout(label_box)

        vbox.addWidget(self.btn_label)
        self.setLayout(vbox)

        # Create a thread
        self.thread = VideoThread()
        # Video info connect with update_video_info
        self.thread.video_total_frames_signal.connect(self.update_total_frames)
        self.thread.video_current_frame_signal.connect(self.update_current_frame)
        self.thread.video_height_signal.connect(self.update_frame_height)
        self.thread.video_width_signal.connect(self.update_frame_width)
        # print(self.thread.video_current_frame_signal)


    def select_video(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select First Video")
        if filename:
            # 선택된 파일의 절대 경로를 얻음
            abs_filename = os.path.abspath(filename)
            folder_path = os.path.dirname(abs_filename)  # 파일의 디렉토리 경로 추출
            self.video_paths = [os.path.abspath(os.path.join(folder_path, f)) for f in os.listdir(folder_path) if f.endswith(('.mp4', '.avi', '.mov'))]
            
            if abs_filename in self.video_paths:
                self.current_video_index = self.video_paths.index(abs_filename)
                self.load_video()

                # for video info file name update
                video_path = self.video_paths[self.current_video_index]
                self.video_filename = os.path.basename(video_path)

            else:
                QMessageBox.warning(self, "Warning", "Selected video file is not in the list!")
        else:
            QMessageBox.warning(self, "Warning", "No video file selected!")

    def load_video(self):
        if 0 <= self.current_video_index < len(self.video_paths):
        # Stop and release the previous thread if it exists
            if hasattr(self, 'thread') and self.thread.isRunning():
                self.thread.stop()
                self.thread.wait()

            self.thread = VideoThread()
            
            self.thread.change_pixmap_signal.connect(self.update_image)
            self.thread.video_total_frames_signal.connect(self.update_total_frames)
            self.thread.video_current_frame_signal.connect(self.update_current_frame)
            self.thread.video_height_signal.connect(self.update_frame_height)
            self.thread.video_width_signal.connect(self.update_frame_width)
            self.thread.set_video_path(self.video_paths[self.current_video_index])
            self.thread.start()

            video_path = self.video_paths[self.current_video_index]
            self.video_path = video_path
            self.video_filename = os.path.basename(video_path)
        else:
            QMessageBox.warning(self, "Warning", "Video file not found in the list!")

    def update_total_frames(self, total_frames):
        self.total_frames = total_frames
        print(f"Total frames updated: {total_frames}")
        self.video_info_display()

    def update_current_frame(self, frame_number):
        self.frame_number = frame_number
        print(f"Total frames updated: {frame_number}")
        self.video_info_display()

    def update_frame_height(self, frame_height):
        self.frame_height = frame_height
        print(f"Total frames updated: {frame_height}")
        self.video_info_display()

    def update_frame_width(self, frame_width):
        self.frame_width = frame_width
        print(f"Total frames updated: {frame_width}")
        self.video_info_display()

    def video_info_display(self):
        # 'self.video_filename'과 같은 다른 정보를 추가하기 전에 존재하는지 확인합니다.
        video_info = f"Video name : {getattr(self, 'video_filename', 'Unknown')}\
 Total frame : {getattr(self, 'total_frames', 'Unknown')} \n Current frame : {getattr(self, 'frame_number', 'Unknown')}\
 Frame width : {getattr(self, 'frame_width', 'Unknown')} Frame height : {getattr(self, 'frame_height', 'Unknown')}"
        self.video_info_label.setText(video_info)

    @pyqtSlot(QImage)
    def update_image(self, qt_img):
        self.image_label.setPixmap(QPixmap.fromImage(qt_img))

    @pyqtSlot()
    def before_frame(self):
        self.thread.before_frame()
        
    @pyqtSlot()
    def next_frame(self):
        self.thread.next_frame()
        
    @pyqtSlot()
    def label_video(self):


        # If start_frame is blank then insert current frame number to start frame        
        try:
            start_frame = int(self.start_frame_input.text())
        except ValueError:
            start_frame = self.frame_number

        frame_count = int(self.label_frame_count.text())
        
        labels = []
        for frame in range(start_frame-1):
            labels.append({"frame_number": frame+1, "label": 0})

        for frame in range(start_frame, start_frame + frame_count):
            labels.append({"frame_number": frame, "label": 1})
        total_frames = self.total_frames
        for frame in range(start_frame + frame_count ,total_frames):
            labels.append({"frame_number": frame, "label": 0})

        # JSON 파일로 저장
        label_data = {"video_name": self.video_filename, "labels": labels}
        with open(f'{self.video_path}.json', 'w') as file:
            json.dump(label_data, file, indent=4)

        QMessageBox.information(self, "Info", f"Labeled {frame_count} frames starting from frame {start_frame}")
    

    @pyqtSlot()
    def prev_video(self):

        if self.current_video_index > 0:
            self.current_video_index -= 1
            self.load_video()

    @pyqtSlot()
    def next_video(self):

        if self.current_video_index < len(self.video_paths) - 1:
            self.current_video_index += 1
            self.load_video()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
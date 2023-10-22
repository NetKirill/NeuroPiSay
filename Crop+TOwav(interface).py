import sys
from moviepy.editor import VideoFileClip
import librosa
import soundfile as sf
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QTabWidget, QGroupBox, QHBoxLayout


class ConvertTab(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Select MP4 file:", self)
        self.label.setGeometry(20, 20, 100, 20)

        self.file_line_edit = QLineEdit(self)
        self.file_line_edit.setGeometry(20, 50, 250, 20)

        self.browse_button = QPushButton("Browse", self)
        self.browse_button.setGeometry(280, 50, 75, 25)
        self.browse_button.clicked.connect(self.browse_file)

        self.label_output = QLabel("Output WAV file:", self)
        self.label_output.setGeometry(20, 80, 100, 20)

        self.output_line_edit = QLineEdit(self)
        self.output_line_edit.setGeometry(20, 110, 250, 20)

        self.convert_button = QPushButton("Convert", self)
        self.convert_button.setGeometry(150, 150, 100, 30)
        self.convert_button.clicked.connect(self.convert_file)

    def browse_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select MP4 file")
        self.file_line_edit.setText(file_path)

    def convert_file(self):
        mp4_path = self.file_line_edit.text()
        wav_path = self.output_line_edit.text()
        if mp4_path and wav_path:
            try:
                convert_mp4_to_wav(mp4_path, wav_path)
                QMessageBox.information(self, "Conversion Successful", "MP4 to WAV conversion completed successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Conversion Error", f"An error occurred during conversion:\n{str(e)}")
        else:
            QMessageBox.warning(self, "Fields Not Filled", "Please select an MP4 file and provide an output WAV file.")

def convert_mp4_to_wav(mp4_file, wav_file):
    video = VideoFileClip(mp4_file)
    audio = video.audio
    audio.write_audiofile(wav_file)
    audio.close()
    video.close()

class CropTab(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Select WAV file:", self)
        self.label.setGeometry(20, 20, 100, 20)

        self.file_line_edit = QLineEdit(self)
        self.file_line_edit.setGeometry(20, 50, 250, 20)

        self.browse_button = QPushButton("Browse", self)
        self.browse_button.setGeometry(280, 50, 75, 25)
        self.browse_button.clicked.connect(self.browse_file)

        self.label_start = QLabel("Start Time (seconds):", self)
        self.label_start.setGeometry(20, 80, 150, 20)

        self.start_line_edit = QLineEdit(self)
        self.start_line_edit.setGeometry(20, 110, 100, 20)

        self.label_end = QLabel("End Time (seconds):", self)
        self.label_end.setGeometry(150, 80, 150, 20)

        self.end_line_edit = QLineEdit(self)
        self.end_line_edit.setGeometry(150, 110, 100, 20)

        self.label_output = QLabel("Output WAV file:", self)
        self.label_output.setGeometry(20, 140, 100, 20)

        self.output_line_edit = QLineEdit(self)
        self.output_line_edit.setGeometry(20, 170, 250, 20)

        self.crop_button = QPushButton("Crop", self)
        self.crop_button.setGeometry(150, 210, 100, 30)
        self.crop_button.clicked.connect(self.crop_file)

    def browse_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select WAV file")
        self.file_line_edit.setText(file_path)

    def crop_file(self):
        wav_path = self.file_line_edit.text()
        start_time = float(self.start_line_edit.text())
        end_time = float(self.end_line_edit.text())
        output_path = self.output_line_edit.text()
        if wav_path and output_path:
            try:
                crop_video(wav_path, start_time, end_time, output_path)
                QMessageBox.information(self, "Crop Successful", "Video cropping completed successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Crop Error", f"An error occurred during cropping:\n{str(e)}")
        else:
            QMessageBox.warning(self, "Fields Not Filled", "Please select a WAV file, specify start and end times, and provide an output WAV file.")

def crop_video(input_file, start_time, end_time, output_file):
    # Загрузка аудиофайла
    audio, sr = librosa.load(input_file)

    # Определение начальной и конечной позиций отсчетов аудио для обрезки
    start_sample = int(start_time * sr)
    end_sample = int(end_time * sr)

    # Обрезка аудио
    trimmed_audio = audio[start_sample:end_sample]

    # Сохранение обрезанного аудио в новый файл
    sf.write(output_file, trimmed_audio, sr)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Toolbox")
        self.setGeometry(100, 100, 400, 300)

        self.tab_widget = QTabWidget(self)

        self.convert_tab = ConvertTab()
        self.crop_tab = CropTab()

        self.tab_widget.addTab(self.convert_tab, "Convert MP4 to WAV")
        self.tab_widget.addTab(self.crop_tab, "Crop Video")

        self.setCentralWidget(self.tab_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
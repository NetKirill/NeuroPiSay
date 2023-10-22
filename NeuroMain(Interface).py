import sys
import wave
import json
import vosk
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog
from PyQt5.QtWidgets import QMessageBox

class SpeechRecognitionWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.model_path = r"C:\AtomicHackBase\vosk-model-ru-0.42"
        self.audio_file = ""
        self.result_file = ""

        self.label_path = QLabel("Audio File:", self)
        self.label_path.setGeometry(20, 20, 80, 20)

        self.path_lineedit = QLineEdit(self)
        self.path_lineedit.setGeometry(110, 20, 250, 20)

        self.browse_button = QPushButton("Browse", self)
        self.browse_button.setGeometry(370, 20, 75, 25)
        self.browse_button.clicked.connect(self.browse_file)

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(20, 60, 425, 200)

        self.recognize_button = QPushButton("Recognize", self)
        self.recognize_button.setGeometry(185, 280, 100, 30)
        self.recognize_button.clicked.connect(self.start_recognition)

    def browse_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Audio File")
        self.path_lineedit.setText(file_path)

    def start_recognition(self):
        self.audio_file = self.path_lineedit.text()
        if self.audio_file:
            self.result_file = self.audio_file.replace(".wav", "_result.txt")
            self.path_lineedit.setReadOnly(True)
            self.browse_button.setEnabled(False)
            self.recognize_button.setEnabled(False)
            self.text_edit.clear()
            self.text_edit.setPlainText("Initializing speech recognition...\n")

            self.recognize_speech()
        else:
            self.show_message_box("Audio File Not Selected", "Please select an audio file.")

    def recognize_speech(self):
        model = vosk.Model(self.model_path)

        wf = wave.open(self.audio_file, "rb")
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            self.show_message_box("Invalid Audio File", "Audio file must be mono and have PCM 16-bit format")
            self.reset_ui()
            return

        rec = vosk.KaldiRecognizer(model, wf.getframerate())

        with open(self.result_file, mode='w') as txtfile:
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    result = rec.Result()
                    result_dict = json.loads(result)
                    text = result_dict['text']
                    self.text_edit.append(text)

            result = rec.FinalResult()
            result_dict = json.loads(result)
            text = result_dict['text']
            self.text_edit.append(text)

        self.show_message_box("Speech Recognition Completed", f"Result saved to:\n{self.result_file}")
        self.reset_ui()

    def reset_ui(self):
        self.path_lineedit.clear()
        self.path_lineedit.setReadOnly(False)
        self.browse_button.setEnabled(True)
        self.recognize_button.setEnabled(True)

    def show_message_box(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()

    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Speech Recognition")
        self.setGeometry(100, 100, 465, 330)

        self.central_widget = QWidget(self)

        self.layout = QVBoxLayout()
        self.speech_recognition_widget = SpeechRecognitionWindow()
        self.layout.addWidget(self.speech_recognition_widget)

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
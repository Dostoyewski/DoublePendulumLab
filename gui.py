import mimetypes
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QMessageBox

from main import ARUCODetector

mimetypes.init()


def isMediaFile(fileName):
    """
    Check if file is video
    :param fileName: path to file
    :return:
    """
    mimestart = mimetypes.guess_type(fileName)[0]
    if mimestart != None:
        mimestart = mimestart.split('/')[0]
        if mimestart in ['video']:
            return True
    return False


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        # Time axis
        self.left = 10
        self.top = 50
        self.title = 'Lab4 v1.2.0'
        # bar with buttons and checkbox
        self.filepath = ''
        self.btnStart = QPushButton('Start', self)
        self.btnLoad = QPushButton('Загрузить видео', self)

        self.infoLabel = QLabel('©Dostoyewski & Amgaran, THEORHECH INC.\n'
                                'All output files will be saved to\napp launch directory', self)
        self.statusLabel = QLabel('', self)

        self.widthp = 384
        self.heightp = 240

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.widthp, self.heightp)
        self.btnLoad.move(100, 20)
        self.btnLoad.clicked.connect(self.openFileNameDialog)
        self.statusLabel.move(100, 100)

        self.btnStart.move(100, 70)

        self.infoLabel.resize(250, 40)
        self.infoLabel.move(100, 180)

        self.btnStart.clicked.connect(self.start)

        self.show()

    def start(self):
        detector = ARUCODetector(self.filepath)
        self.statusLabel.setText('Обрабатываю...')
        detector.run()
        self.statusLabel.setText('Готово!')

    def openFileNameDialog(self):
        """
        Select scenario file
        :return:
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileNames(self, "Загрузить видео", "", "", options=options)
        if filename and isMediaFile(filename[0]):
            self.filepath = filename[0]
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Вы уверены, что это видео?")
            msg.setInformativeText('Хм. По-моему, это какая-то ботва, а не видео. Перепроверьте то, что вы '
                                   'скармливаете программе. Лучше всего *.mp4.')
            msg.setWindowTitle("Эй, помедленнее!")
            msg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

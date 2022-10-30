from PyQt5.QtWidgets import (QWidget, QApplication, QProgressBar, QMainWindow)
from PyQt5.QtCore import (Qt, QObject, pyqtSignal, pyqtSlot, QRunnable, QThreadPool)
import time


class WorkerSignals(QObject):

    progress = pyqtSignal(int)



class JobRunner(QRunnable):

    signals = WorkerSignals()

    def __init__(self):
        super().__init__()

    @pyqtSlot()
    def run(self):
        for n in range(100):
            self.signals.progress.emit(n + 1)
            time.sleep(0.1)



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Create a statusbar.
        self.status = self.statusBar()
        self.progress = QProgressBar()
        self.status.addPermanentWidget(self.progress)

        # Thread runner
        self.threadpool = QThreadPool()

        # Create a runner
        self.runner = JobRunner()
        self.runner.signals.progress.connect(self.update_progress)
        self.threadpool.start(self.runner)

        self.show()

    def update_progress(self, n):
        self.progress.setValue(n)

app = QApplication([])
w = MainWindow()
app.exec_()
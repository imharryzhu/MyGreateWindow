import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
import resources.app_rc ## !! do not delete this line!!!


if __name__ == "__main__":
    app = QApplication(sys.argv)

    view = MainWindow()
    view.show()

    retcode = app.exec()
    sys.exit(retcode)

import sys

def main():
    from PySide6.QtWidgets import QApplication
    from .gui import MainWindow
    app = QApplication.instance() or QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
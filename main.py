import subprocess
import sys

import qpageview
from PyQt5.QtWidgets import QApplication, QGridLayout, QMainWindow, QWidget, QLabel, QPushButton, QFileDialog, \
    QMessageBox
from os.path import expanduser
import os.path
from pathlib import Path

config_filename = 'welcome-pages.desktop'


class pageView(qpageview.View):

    def __init__(self, parent=None):
        super().__init__(parent)

    def wheelEvent(self, ev):
        pass


class MainWindow(QMainWindow):

    def next_page(self):
        if self.current_page < self.numpages - 1:
            self.v.gotoNextPage()
            self.current_page += 1
            self.pagenumberlabel.setText(f'Страница {self.current_page + 1} из {self.numpages}')

    def prev_page(self):
        if self.current_page > 0:
            self.v.gotoPreviousPage()
            self.current_page -= 1
            self.pagenumberlabel.setText(f'Страница {self.current_page + 1} из {self.numpages}')

    def remove_link(self):
        if os.path.isfile(f'{expanduser("~")}/.config/autostart/{config_filename}'):
            subprocess.run(f'rm -rf {expanduser("~")}/.config/autostart/{config_filename}')
        else:
            print('No config file found.')

    # def open_file_dialog(self):
    #     filename, ok = QFileDialog.getOpenFileName(
    #         self, "Выберите файл", '/', "PDF Files (*.pdf)"
    #     )
    #     if ok:
    #         fname = str(Path(filename))
    #         doc = qpageview.loadPdf(fname)
    #         self.v.setDocument(doc)
    #         self.pages = self.v.pages()
    #         self.numpages = len(self.pages)
    #         self.current_page = 0
    #         self.pagenumberlabel.setText(f'Страница {self.current_page + 1} из {self.numpages}')

    def __init__(self):
        error_message = False
        if len(sys.argv) < 2:
            error_message = 'Не задан PDF-файл для открытия'
        elif not os.path.isfile(sys.argv[1].strip()):
            error_message = 'Указанный файл не существует'
        elif not sys.argv[1].strip().endswith('pdf'):
            error_message = 'Файл не является PDF-файлом'
        if error_message:
            dlg = QMessageBox(QMessageBox.Warning, 'Внимание', error_message)
            dlg.exec_()
            sys.exit()

        QMainWindow.__init__(self)

        self.setWindowTitle("welcome-pages")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        grid_layout = QGridLayout()

        self.v = pageView()
        doc = qpageview.loadPdf("/home/user/Загрузки/manual.pdf")
        self.v.setDocument(doc)
        self.v.setViewMode(qpageview.FitBoth)
        self.v.setContinuousMode(False)
        self.v.kineticPagingEnabled = False
        self.v.kineticScrollingEnabled = True

        self.v.wheelZoomingEnabled = False
        self.pages = self.v.pages()
        self.numpages = len(self.pages)
        self.current_page = 0

        # open_file_button = QPushButton("Выберите файл")
        # open_file_button.clicked.connect(self.open_file_dialog)
        # grid_layout.addWidget(open_file_button, 0, 0, 1, 3)
        grid_layout.addWidget(self.v, 0, 0, 1, 3)
        back = QPushButton('Назад')
        nomoreshow = QPushButton('Больше не показывать')
        fwd = QPushButton('Вперёд')
        back.clicked.connect(self.prev_page)
        fwd.clicked.connect(self.next_page)
        nomoreshow.clicked.connect(self.remove_link)
        grid_layout.addWidget(back, 1, 0)
        grid_layout.addWidget(fwd, 1, 2)
        grid_layout.addWidget(nomoreshow, 1, 1)
        self.pagenumberlabel = QLabel(f'Страница 1 из {self.numpages}')
        grid_layout.addWidget(self.pagenumberlabel, 2, 0, 1, 2)
        central_widget.setLayout(grid_layout)
        self.showMaximized()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

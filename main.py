#!/usr/bin/python3

import os.path
import subprocess
import sys
from os.path import expanduser

import qpageview
from PyQt5.QtWidgets import QApplication, QGridLayout, QMainWindow, QWidget, QLabel, QPushButton, QMessageBox

config_filename = 'welcome-pages.desktop'


class pageView(qpageview.View):

    def __init__(self, parent=None):
        super().__init__(parent)

    def wheelEvent(self, ev):
        pass


class MainWindow(QMainWindow):

    def show_send_statistics_window(self):
        dlg = QMessageBox.question(self, 'Внимание!', 'Вы соглашаетесь на отправку анонимной статистики.',
                                   QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if dlg == QMessageBox.Yes:
            print('Yes')
            sys.exit()
        elif dlg == QMessageBox.No:
            print('No')
            sys.exit()
        else:
            print('Cancel')

    def next_page(self):
        self.back_btn.setEnabled(True)
        if self.current_page < self.numpages - 1:
            self.v.gotoNextPage()
            self.current_page += 1
            self.pagenumberlabel.setText(f'Страница {self.current_page + 1} из {self.numpages}')
            if self.current_page == self.numpages - 1:
                self.fwd.clicked.disconnect()
                self.fwd.clicked.connect(self.show_send_statistics_window)
                self.fwd.setText('Хочу помочь сбору статистики')
                return

    def prev_page(self):
        self.fwd.setEnabled(True)
        if self.current_page > 0:
            self.v.gotoPreviousPage()
            self.current_page -= 1
            self.pagenumberlabel.setText(f'Страница {self.current_page + 1} из {self.numpages}')
            if self.current_page == self.numpages - 2:
                self.fwd.clicked.disconnect()
                self.fwd.clicked.connect(self.next_page)
                self.fwd.setText('Вперёд')
        if self.current_page == 0:
            self.back_btn.setDisabled(True)

    def remove_link(self):
        if os.path.isfile(f'{expanduser("~")}/.config/autostart/{config_filename}'):
            subprocess.run(f'rm -rf {expanduser("~")}/.config/autostart/{config_filename}')
        else:
            print('No config file found.')
        sys.exit()

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
        doc = qpageview.loadPdf(sys.argv[1])
        self.v.setDocument(doc)
        self.v.setViewMode(qpageview.FitBoth)
        self.v.setContinuousMode(False)
        self.v.kineticPagingEnabled = False
        self.v.kineticScrollingEnabled = True

        self.v.wheelZoomingEnabled = False
        self.pages = self.v.pages()
        self.numpages = len(self.pages)
        self.current_page = 0

        grid_layout.addWidget(self.v, 0, 0, 1, 3)

        self.back_btn = QPushButton('Назад')
        nomoreshow = QPushButton('Больше не показывать')
        self.fwd = QPushButton('Вперёд')
        self.back_btn.clicked.connect(self.prev_page)
        self.fwd.clicked.connect(self.next_page)
        nomoreshow.clicked.connect(self.remove_link)
        grid_layout.addWidget(self.back_btn, 1, 0)
        grid_layout.addWidget(self.fwd, 1, 2)
        self.back_btn.setDisabled(True)
        grid_layout.addWidget(nomoreshow, 1, 1)
        self.pagenumberlabel = QLabel(f'Страница 1 из {self.numpages}')
        grid_layout.addWidget(self.pagenumberlabel, 2, 0, 1, 2)
        central_widget.setLayout(grid_layout)
        self.showFullScreen()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

import sys

import qpageview
from PyQt5.QtWidgets import QApplication, QGridLayout, QMainWindow, QWidget, QLabel, QPushButton


class MainWindow(QMainWindow):

    def next_page(self):
        if self.current_page < self.numpages - 1:
            self.current_page += 1
            with self.v.modifyPages() as mod_pages:
                mod_pages[:] = [self.pages[self.current_page]]
            self.pagenumberlabel.setText(f'Страница {self.current_page + 1} из {self.numpages}')
    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            with self.v.modifyPages() as mod_pages:
                mod_pages[:] = [self.pages[self.current_page]]
            self.pagenumberlabel.setText(f'Страница {self.current_page + 1} из {self.numpages}')

    def __init__(self):
        QMainWindow.__init__(self)

        self.setWindowTitle("Просмотр PDF")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        grid_layout = QGridLayout()

        self.v = qpageview.View()
        doc = qpageview.loadPdf("/home/user/Data/cco/st/2022-23/diagn/20230425/20230425.pdf")
        self.v.setDocument(doc)
        self.pages = self.v.pages()
        self.numpages = len(self.pages)
        self.current_page = 0
        with self.v.modifyPages() as mod_pages:
            mod_pages[:] = [self.pages[0]]

        grid_layout.addWidget(self.v, 0, 0, 1, 2)
        back = QPushButton('Назад')
        fwd = QPushButton('Вперёд')
        back.clicked.connect(self.prev_page)
        fwd.clicked.connect(self.next_page)
        grid_layout.addWidget(back, 1, 0)
        grid_layout.addWidget(fwd, 1, 1)
        self.pagenumberlabel = QLabel(f'Страница 1 из {self.numpages}')
        grid_layout.addWidget(self.pagenumberlabel, 2, 0, 1, 2)
        central_widget.setLayout(grid_layout)
        self.resize(600, 800)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

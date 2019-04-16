import requests
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QTableWidgetItem, QMainWindow, QWidget, QGridLayout, QApplication, QTableWidget
from bs4 import BeautifulSoup


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(800, 500))
        self.setWindowTitle("Pikabu")
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        grid_layout = QGridLayout()
        central_widget.setLayout(grid_layout)

        table = QTableWidget(self)
        table.setColumnCount(6)
        table.setRowCount(1)

        table.setHorizontalHeaderLabels(["Author", "Time", "Title", "Rating", "Comments", "href"])

        page = requests.get('https://pikabu.ru/best')
        soup = BeautifulSoup(page.text, 'html.parser')
        articles = soup.find_all('article')

        for i in range(len(articles)-1):
            article = articles[i]

            author = article.find(class_="user__nick")
            href = article.find(class_="story__title").find('a').get("href")
            time = article.find(class_="story__datetime")
            title = article.find(class_="story__title-link")
            rating = article.find(class_="story__rating-block")
            comments = article.find(class_="story__comments-count").find_all('span')[1]

            table.setRowCount(i + 1)

            table.setItem(i, 0, QTableWidgetItem(author.get_text()))
            table.setItem(i, 1, QTableWidgetItem(time.get_text()))
            table.setItem(i, 2, QTableWidgetItem(title.get_text()))
            table.setItem(i, 3, QTableWidgetItem(rating.get_text()))
            table.setItem(i, 4, QTableWidgetItem(comments.get_text()))
            table.setItem(i, 5, QTableWidgetItem(href))

        table.resizeColumnsToContents()
        grid_layout.addWidget(table, 0, 0)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())

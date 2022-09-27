
from fileinput import filename
from ui import Ui_MainWindow
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWidgets import QMainWindow,QApplication, QFileDialog, QTableWidgetItem, QHeaderView, QPushButton

class main_ui(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(main_ui,self).__init__()
        self.setupUi(self)
        self.count = 0
        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        

        
        self.add_file_bttn.clicked.connect(self.add_pdf_file)

    def add_pdf_file(self):
        filename, _ = QFileDialog.getOpenFileName(None, filter="PDF (*.pdf)")
        if not filename:
            print("please select the .pdf file")
        # print(len(file_name), " ", str(filename))
        print(filename.split("/"))
        file_name = filename.split("/")
        # file_name = len(file_name)-1
        file_name = file_name[len(file_name)-1]
        print(file_name)
        
        self.create_bttns()    
        self.tableWidget.insertRow(self.count)
        self.tableWidget.setItem(self.count, 0, QTableWidgetItem(str(filename)))
        self.tableWidget.setCellWidget(self.count, 1, self.view_bttn)
        self.tableWidget.setCellWidget(self.count, 2, self.delete_bttn)
        self.create_webview(filename)
        self.count = +1

    def create_webview(self,filename):
        # view = QWebEngineView()
        view = QWebEngineView()
        settings = view.settings()
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        url = QUrl.fromLocalFile(filename)
        view.load(url)
        self.gridLayout_4.addWidget(view)
        
    def create_bttns(self):
        self.view_bttn = QPushButton()
        self.view_bttn.setIcon(QIcon('icons/visual.png'))
        self.delete_bttn = QPushButton()
        self.delete_bttn.setIcon(QIcon('icons/delete.png'))
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    four_pdf = main_ui()
    four_pdf.show()
    sys.exit(app.exec_())

from fileinput import filename
from ui import Ui_MainWindow
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWidgets import QMainWindow,QApplication, QFileDialog, QTableWidgetItem, QHeaderView, QPushButton
from PyPDF2 import PdfFileMerger, PdfMerger
import qpageview

class main_ui(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(main_ui,self).__init__()
        self.setupUi(self)
        self.showMaximized()
        self.count = 0
        self.pdfs = []
        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        

        self.view = QWebEngineView()
        settings = self.view.settings()
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
        self.create_webview(filename)
        
        self.add_file_bttn.clicked.connect(self.add_pdf_file)
        self.merge_bttn.clicked.connect(self.on_merge_bttn)
        self.start_bttn.clicked.connect(self.on_merge_start)
        self.home_bttn.clicked.connect(self.go_home)
        # self.view_bttn.clicked.connect(self.on_view_bttn_clicked)

    def add_pdf_file(self):
        filename, _ = QFileDialog.getOpenFileName(None, filter="PDF (*.pdf)")
        if not filename:
            print("please select the .pdf file")

        print(filename.split("/"))
        file_name = filename.split("/")
        file_name = file_name[len(file_name)-1]
        print(file_name)
        
        self.create_bttns()    
        self.tableWidget.insertRow(self.count)
        self.tableWidget.setItem(self.count, 0, QTableWidgetItem(str(file_name)))
        self.tableWidget.setCellWidget(self.count, 1, self.view_bttn)
        self.tableWidget.setCellWidget(self.count, 2, self.delete_bttn)
        
        self.count = +1
        self.pdfs.append(filename)
        print(self.pdfs)

    def create_webview(self,filename):
        # view = QWebEngineView()
        # url = QUrl.fromLocalFile(filename)
        # view.load(url)
        # view.setGeometry(100, 50, 400, 300)

        # self.view.load(QUrl.fromUserInput(filename))
        self.gridLayout_6.addWidget(self.view)

        # v = qpageview()
        # v = qpageview.View()
        # self.gridLayout_4.addWidget(v)
        # v.loadPdf("../osi.pdf")
        # v.show()
        
    def create_bttns(self):
        self.view_bttn = QPushButton()
        self.view_bttn.setIcon(QIcon('icons/eye.png'))
        self.view_bttn.clicked.connect(self.on_view_bttn_clicked)
        self.delete_bttn = QPushButton()
        self.delete_bttn.setIcon(QIcon('icons/delete.png'))
        self.delete_bttn.clicked.connect(self.on_delete_bttn_clicked)
    
    def on_merge_start(self):       
        merger = PdfFileMerger()
        for pdf in self.pdfs:
            merger.append(pdf)
        #     merger.write("result.pdf")
        #     merger.close()
        name = QFileDialog.getSaveFileName(self, 'Save File',"","PDF Files(*.pdf);;")
            # writing combined pdf to output pdf file
        with open(name, 'wb') as f:
            merger.write(f)
            merger.close()
        # file = open(name,'wb')
        # file.write()
        # # merger(PdfFileMerger(open(name,"w")).write(k))
        # file.close()
        
        # merger.write("result.pdf")
        # merger.close()
    def on_merge_bttn(self):
        self.stackedWidget.setCurrentIndex(0)
    def go_home(self):
        self.stackedWidget.setCurrentIndex(1)
    
    def on_view_bttn_clicked(self):
        button = self.sender()
        if button:
            row = self.tableWidget.indexAt(button.pos()).row()
            self.view.load(QUrl.fromUserInput(str(self.pdfs[row])))
            # del_row = row + 1
            # print("row value" ,del_row)
            # self.webView2.page().runJavaScript("rowValue('"+str(del_row)+"');", self.ready)
            
            # self.tableWidget.removeRow(row)
            # self.count -= 1

    def on_delete_bttn_clicked(self):
        try:
            button = self.sender()
            if button:
                row = self.tableWidget.indexAt(button.pos()).row()
                # del_row = row + 1
                # print("row value" ,del_row)
                # self.webView2.page().runJavaScript("rowValue('"+str(del_row)+"');", self.ready)
                
                self.tableWidget.removeRow(row)
                self.pdfs.pop(row)
                self.count -= 1
        except:
            print("Deletion failed !")
        # def save_file(self):

    def file_save(self):
        name = QFileDialog.getSaveFileName(self, 'Save File')
        file = open(name,'w')
        text = self.textEdit.toPlainText()
        file.write(text)
        file.close()
        pass

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    four_pdf = main_ui()
    four_pdf.show()
    sys.exit(app.exec_())
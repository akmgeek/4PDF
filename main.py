from ui import Ui_MainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow,QApplication, QFileDialog, QTableWidgetItem,QPushButton, QMessageBox
from PyPDF2 import PdfFileMerger, PdfFileWriter, PdfFileReader
import os
import qdarktheme

class main_ui(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(main_ui,self).__init__()
        self.setupUi(self)
        self.showMaximized()
        self.count = 0
        self.pdfs = []

        self.add_file_bttn.clicked.connect(self.add_pdf_file)
        self.merge_bttn.clicked.connect(self.merge_pdf_file_th)
        self.lightMode_rb.toggled.connect(self.change_theme)
        self.darkMode_rb.toggled.connect(self.change_theme)
        self.browserFile_bttn.clicked.connect(self.select_pdf_file)
        self.split_bttn.clicked.connect(self.do_split)
        self.split_page_gb.toggled.connect(self.uncheck_range)
        self.split_range_gb.toggled.connect(self.uncheck_page)

    def add_pdf_file(self):
        filename, _ = QFileDialog.getOpenFileName(None, filter="PDF (*.pdf)")
        if not filename:
            print("please select the .pdf file")
        else:
            file_name = filename.split("/")
            file_name = file_name[len(file_name)-1]
            file_size = self.getsize(filename)
            page_num = self.getpages(filename)
            
            self.create_bttns()    
            self.tableWidget.insertRow(self.count)
            self.tableWidget.setItem(self.count, 0, QTableWidgetItem(str(file_name)))
            self.tableWidget.setItem(self.count, 1, QTableWidgetItem(str(file_size)))
            self.tableWidget.setItem(self.count, 2, QTableWidgetItem(str(page_num)))
            self.tableWidget.setItem(self.count, 3, QTableWidgetItem(str('All')))
            self.tableWidget.setCellWidget(self.count, 4, self.delete_bttn)
            
            self.count = +1
            self.pdfs.append(filename)
            print(self.pdfs)

    def select_pdf_file(self):
        filename, _ = QFileDialog.getOpenFileName(None, filter="PDF (*.pdf)")
        if not filename:
            print("please select the .pdf file")
        else:
            self.pdf_path_split.setText(filename)
            self.split_inputFile = filename
            page_nums = self.getpages(filename)
            file_size = self.getsize(filename)
            self.label_3.setText(f'Total number of pages: {page_nums}. File size:{file_size}')
    
    def uncheck_page(self):
            self.split_page_gb.setChecked(False)
    def uncheck_range(self):
            self.split_range_gb.setChecked(False)

    def do_split(self):
        reader = PdfFileReader(self.split_inputFile)
        writer = PdfFileWriter()
        if self.split_page_gb.isChecked()==True:
            writer.addPage(reader.getPage(int(self.page_no.text())))
        
        elif self.split_range_gb.isChecked()==True:
            pageFrom = int(self.page_from.text())
            pageTo = int(self.page_to.text())

            for page in range(pageFrom-1,pageTo):
                writer.addPage(reader.getPage(page))

        filename = QFileDialog.getSaveFileName(self, 'Save File',"","PDF Files(*.pdf);;")
        with open(filename[0], 'wb') as output:
            writer.write(output)
        # self.statusBar.showMessage("File Splitted and Saved Successfully !")

    # pdf INFO
    def getsize(self, filename):
        size = os.path.getsize(filename)*0.0001      # byte to kb
        if size>999:
            size = str(round(size*0.0001,1))+'mb'     
        else:
            size = str(round(size,1))+'kb'           # change kilobyte(kb) to megabyte(mb)
        return size

    def getpages(self, filename):
        reader = PdfFileReader(filename)
        return reader.getNumPages()

    # create remove button in table for each pdf

    def create_bttns(self):
        self.delete_bttn = QPushButton()
        self.delete_bttn.setIcon(QIcon('icons/delete.png'))
        self.delete_bttn.clicked.connect(self.on_delete_bttn_clicked)

    def merge_pdf_file_th(self):
        if self.count==0:
            QMessageBox.information(self, 'Merge Info', 'Please add files before merge.')
        else:
            import threading
            merge_th = threading.Thread(target=self.merge_pdf_file)
            merge_th.start()
        # self.merge_pdf_file()

    # start merging pdf file.
    def merge_pdf_file(self):
        merger = PdfFileMerger()
        for pdf in self.pdfs:
            merger.append(pdf)
        filename = QFileDialog.getSaveFileName(self, 'Save File',"","PDF Files(*.pdf);;")
        print(filename[0])
        output = open(filename[0],'wb')
        merger.write(output)
        merger.close()
        output.close()

    # remove pdf from table
    def on_delete_bttn_clicked(self):
        try:
            button = self.sender()
            if button:
                row = self.tableWidget.indexAt(button.pos()).row()
                self.tableWidget.removeRow(row)
                self.pdfs.pop(row)
                self.count -= 1
        except:
            print("Deletion failed !")

    # SETTING

    # Change theme
    def change_theme(self):
        if self.lightMode_rb.isChecked()==True:
            app.setStyleSheet(qdarktheme.load_stylesheet("light"))
            self.darkMode_rb.setChecked(False)

        elif self.darkMode_rb.isChecked()==True:
            app.setStyleSheet(qdarktheme.load_stylesheet("dark"))
            self.lightMode_rb.setChecked(False)

    
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet("light"))
    four_pdf = main_ui()
    four_pdf.show()
    sys.exit(app.exec_())
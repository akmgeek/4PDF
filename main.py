from ui import Ui_MainWindow
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMainWindow,QApplication, QFileDialog, QTableWidgetItem,QPushButton, QMessageBox, QProgressDialog
from PyPDF2 import PdfWriter, PdfMerger, PdfReader
import os
import qdarktheme

class Worker(QThread):
    def __init__(self, session, order):
        super.__init__()
        self.session = session
        self.order = order

    def run(self):
        self.session.delete(self.order)
        self.session.commit()

class main_ui(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(main_ui,self).__init__()
        self.setupUi(self)
        self.showMaximized()
        self.count = 0
        self.pdfs = []
        
        self.encryptionFlag = False
        self.mergeEncryptPass.hide()
        self.splitEncryptPass.hide()

        self.mergeEncryptCheck.toggled.connect(self.mergeAddPass)
        self.splitEncryptCheck.toggled.connect(self.splitAddPass)

        self.add_file_bttn.clicked.connect(self.add_pdf_file)
        self.merge_bttn.clicked.connect(self.merge_pdf_file_th)
        self.lightMode_rb.toggled.connect(self.change_theme)
        self.darkMode_rb.toggled.connect(self.change_theme)
        self.browserFile_bttn.clicked.connect(self.select_pdf_file)
        self.browserFile_bttn_2.clicked.connect(self.select_pdf_file_extract)
        self.browserFile_bttn_3.clicked.connect(self.extractText)
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
            # self.tableWidget.setItem(self.count, 3, QTableWidgetItem(str('All')))
            self.tableWidget.setCellWidget(self.count, 3, self.delete_bttn)
            
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

    def select_pdf_file_extract(self):
        filename, _ = QFileDialog.getOpenFileName(None, filter="PDF (*.pdf)")
        if not filename:
            print("please select the .pdf file")

        else:
            self.pdf_path_extract.setText(filename)
            # self.split_inputFile = filename
            page_nums = self.getpages(filename)
            file_size = self.getsize(filename)
            self.label_6.setText(f'Total number of pages: {page_nums}. File size:{file_size}')

    def extractText(self):
        try:
            if self.pdf_path_extract.text()=="" or self.pdf_path_extract.text()==" ":
                QMessageBox.information(self, "Extract Info", "Add valid pdf file path.")
            else:
                reader = PdfReader(self.pdf_path_extract.text())
                page = reader.pages[int(self.extractPageNo.text())-1]
                self.textEdit.setPlainText(page.extract_text())
                
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "Extract", "Text extraction failed.")

    
    def uncheck_page(self):
            self.split_page_gb.setChecked(False)
    def uncheck_range(self):
            self.split_range_gb.setChecked(False)

    def do_split(self):
        try:
            if self.label_3.text()=="" or self.label_3.text()==" ":
                QMessageBox.information(self, "Split Info", "Add valid pdf file path.")
            else:
                reader = PdfReader(self.split_inputFile)
                writer = PdfWriter()
                if self.split_page_gb.isChecked()==True:
                    writer.add_page(reader.pages[int(self.page_no.text())-1])
                
                elif self.split_range_gb.isChecked()==True:
                    pageFrom = int(self.page_from.text())
                    pageTo = int(self.page_to.text())

                    for page in range(pageFrom-1,pageTo):
                        writer.add_page(reader.pages[page])
                    
                    if self.encryptionFlag:
                        writer.encrypt(self.splitEncryptPass.text())

                filename = QFileDialog.getSaveFileName(self, 'Save File',"","PDF Files(*.pdf);;")
                # self.progress = QProgressDialog("Running Script", None, 0, 0, self)
                with open(filename[0], 'wb') as output:
                    writer.write(output)
                # self.progress.close()

                QMessageBox.information(self, "Success", f'Your file saved to location: {filename[0]}')
 
        except:
            QMessageBox.warning(self, "Split Warning ", "Split Failed!")
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
        reader = PdfReader(filename)
        return len(reader.pages)

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
        try:
            merger = PdfWriter()
            for pdf in self.pdfs:
                merger.append(pdf)
            filename = QFileDialog.getSaveFileName(self, 'Save File',"","PDF Files(*.pdf);;")
            print(filename[0])
            if self.encryptionFlag:
                merger.encrypt(self.mergeEncryptPass.text())
            with open(filename[0], 'wb') as output:
                merger.write(output)
            QMessageBox.information(self, "Success", f'Your file saved to location: {filename[0]}')
        except:
            QMessageBox.warning(self, "Merge Warning", "Merging Failed")

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

    # Encyption & Decryption
    def mergeAddPass(self):
        if self.mergeEncryptCheck.isChecked():
            self.mergeEncryptPass.show()
            self.encryptionFlag = True
        else:
            self.mergeEncryptPass.hide()
            self.encryptionFlag = False
            
    def splitAddPass(self):
        if self.splitEncryptCheck.isChecked():
            self.splitEncryptPass.show()
            self.encryptionFlag = True
        else:
            self.splitEncryptPass.hide()
            self.encryptionFlag = False

        
    def runEncryption(self, file, key):
        reader = PdfReader(file)
        writer = PdfWriter()

        # Add all pages to the writer
        for page in reader.pages:
            writer.add_page(page)

        # Add a password to the new PDF
        writer.encrypt(key)
        
    def runDecryption(self, file, key):
        reader = PdfReader(file)
        writer = PdfWriter()

        if reader.is_encrypted:
            reader.decrypt(key)

        # Add all pages to the writer
        for page in reader.pages:
            writer.add_page(page)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet("light"))
    four_pdf = main_ui()
    four_pdf.show()
    sys.exit(app.exec_())
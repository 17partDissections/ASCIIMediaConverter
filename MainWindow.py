from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QFileDialog, QMessageBox, QLabel
from PyQt5.QtGui import *
from PIL import Image


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        #self.setWindowTitle("ASCII Media Converter (Mode: None)")
        self.setWindowTitle("ASCII Media Converter")
        self.setWindowIcon(QIcon("_internal/ico/icon.ico"))
        self.setGeometry(100, 100, 1000, 800)

        self.textEdit = QTextEdit()
        self.textEdit.setFontFamily("Courier")
        self.textEdit.setFontPointSize(7)
        self.textEdit.setTabStopDistance(30)
        self.setCentralWidget(self.textEdit)

        self.CreateMenu()

        self.statusBar().showMessage("Row: 1, Column: 1")
        self.statusBar = self.statusBar()
        self.rightLabel = QLabel("ASCIIMediaConverter version 1.0 by Q17pD")
        self.statusBar.addPermanentWidget(self.rightLabel)
        self.textEdit.cursorPositionChanged.connect(self.UpdateStatusBar)

        self.show()

    def CreateMenu(self):
        menubar = self.menuBar()

        fileMenu = menubar.addMenu("File")

        openAction = QAction("Open", self)
        openAction.triggered.connect(self.OpenFile)
        saveAction = QAction("Save as...", self)
        saveAction.triggered.connect(self.SaveFile)
        #optionsAction = QAction("Options", self)  #  иллюзия безопасности
        exitAction = QAction("Exit", self)
        exitAction.triggered.connect(self.close)
        #modeMenu = QMenu("Mode", self)
        #imageAction = QAction("Image", self)
        #imageAction.triggered.connect(self.SetImageMode)
        #modeMenu.addAction(imageAction)
        #videoAction = QAction("Video", self)
        #videoAction.triggered.connect(self.SetVideoMode)
        #modeMenu.addAction(videoAction)

        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        #fileMenu.addMenu(modeMenu)
        #fileMenu.addAction(optionsAction)
        fileMenu.addAction(exitAction)

        helpMenu = menubar.addMenu("Help")
        aboutAction = QAction("About", self)
        aboutAction.triggered.connect(self.About)
        helpMenu.addAction(aboutAction)

    def OpenFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Images (*.png *.xpm *.jpg *.bmp)")
        if fileName:
            try:
                #self.SetImageMode()
                ASCIIImage = self.ImageToASCII(fileName)
                self.textEdit.setText(ASCIIImage)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error loading image: {str(e)}")
                #self.SetNoneMode()

    def SaveFile(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save as...", "", "Text Files (*.txt)")
        if fileName:
            with open(fileName, "w", encoding="utf-8") as f:
                f.write(self.textEdit.toPlainText())

    def SetNoneMode(self):
        self.setWindowTitle("ASCII Media Converter (Mode: None)")
    def SetImageMode(self):
        self.setWindowTitle("ASCII Media Converter (Mode: Image)")
    def SetVideoMode(self):
        self.setWindowTitle("ASCII Media Converter (Mode: Video)")

    def About(self):
        aboutMessage = QMessageBox(self)
        aboutMessage.setIcon(QMessageBox.Information)
        aboutMessage.setWindowTitle("About program")
        aboutMessage.setWindowIcon(QIcon("_internal/ico/icon.ico"))
        aboutMessage.setText("<b>ASCII Media Converter</b><br>Version 1.0<br>Made by: Q17pD<a href='https://github.com/17partDissections'>(17partDissections)</a><br><a href='https://github.com/17partDissections/ASCIIMediaConverter'>(Github Repository Page)</a>")
        aboutMessage.exec_()

    def ImageToASCII(self, imagePath, newWidth=100):
        ASCIIChars = ["@", "#", "%", "?", "*", "+", "=", "-", "(", ")", "/", ";", ":", ",", "."]

        try:
            img = Image.open(imagePath).convert("L")
            width, height = img.size
            aspectRatio = height / width

            newHeight = int(newWidth * aspectRatio * 0.55)

            img = img.resize((newWidth, newHeight))

            pixels = img.getdata()

            ASCIIStr = ""
            for pixel in pixels:
                ASCIIStr += ASCIIChars[pixel // 25]

            ASCIIImg = ""
            for i in range(0, len(ASCIIStr), newWidth):
                ASCIIImg += ASCIIStr[i:i + newWidth] + "\n"

            return ASCIIImg
        except Exception as e:
            raise ValueError(f"Error processing image: {e}")

    def UpdateStatusBar(self):
        cursor = self.textEdit.textCursor()
        row = cursor.blockNumber() + 1
        column = cursor.columnNumber() + 1
        self.statusBar.showMessage(f"Row: {row}, Column: {column}")
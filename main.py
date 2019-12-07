# This file is part of PYDE.
#
# PYDE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PYDE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PYDE.  If not, see <https://www.gnu.org/licenses/>

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtRemoveInputHook, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QFileDialog, QPlainTextEdit, QPushButton, QMessageBox
from PyQt5 import uic

Ui_MainWindow, QtBaseClass = uic.loadUiType('MainWindowUI.ui')

class MyApp(QMainWindow):
    def __init__(self):

        # initialize its parent `QMainWindow`
        # and set `Ui_MainWindow` as `ui`
        super(MyApp, self).__init__(None)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow = self)

        # add event handling for file menu
        self.ui.actionNew.triggered.connect(self.actionNew)
        self.ui.actionOpen.triggered.connect(self.actionOpen)
        
        # global : `activefile` gives the full path to the current working document
        self.activeFile = None
        self.ui.actionSave.triggered.connect(self.actionSave)
        self.ui.actionSave_As.triggered.connect(self.actionSaveAs)

        self.ui.actionExit.triggered.connect(self.actionExit)

    def actionNew(self):
        # clear the workspace
        # if the current document is not already saved, ask if the user would like to save it

        if self.checkSaved():
            # if the document is saved or empty, clear the workspace
            self.ui.plainTextEdit.setPlainText(QtCore.QCoreApplication.translate('MainWindow', ''))
        else:
            # if the document is not saved or empty, ask if the user wants to save it
            # private msg : temporary window to ask if the user wants to overwrite the current document
            msg = self.overwriteWarning()
            if msg == QMessageBox.Yes:
                # save the current document and then clear the workspace
                self.actionSave()
                self.ui.plainTextEdit.setPlainText(QtCore.QCoreApplication.translate('MainWindow', ''))
            elif msg == QMessageBox.No:
                # clear the workspace if the user doesnt want to save
                self.ui.plainTextEdit.setPlainText(QtCore.QCoreApplication.translate('MainWindow', ''))
            if msg == QMessageBox.Cancel:
                # cancel clearing the workspace if the user doesnt want to skip nor continue saving
                pass
        

    def actionOpen(self):
        # TODO : clean this up, its really ugly
        # too many copy/pastes where there could be a common function
        
        if self.checkSaved():
            options = QFileDialog.Options()
            filename = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*)", options=options)
            with open(filename[0]) as f:
                self.ui.plainTextEdit.setPlainText(QtCore.QCoreApplication.translate('MainWindow', f.read()))
                self.activeFile = filename[0]
            if self.activeFile:
                self.setWindowTitle('{0} - PyEditor'.format(window.activeFile))
            elif self.activeFile == None:
                self.setWindowTitle('PyEditor')
        else:
            # if the document is not saved or empty, ask if the user wants to save it
            # private msg : temporary window to ask if the user wants to overwrite the current document
            msg = self.overwriteWarning()
            if msg == QMessageBox.Yes:
                # save the current document and then open the chosen document
                self.actionSave()
                options = QFileDialog.Options()
                filename = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*)", options=options)
                with open(filename[0]) as f:
                    self.ui.plainTextEdit.setPlainText(QtCore.QCoreApplication.translate('MainWindow', f.read()))
                    self.activeFile = filename[0]
                if self.activeFile:
                    self.setWindowTitle('{0} - PyEditor'.format(window.activeFile))
                elif self.activeFile == None:
                    self.setWindowTitle('PyEditor')
            elif msg == QMessageBox.No:
                # open the chosen document if the user doesnt want to save
                # save the current document and then open the chosen document
                self.actionSave()
                options = QFileDialog.Options()
                filename = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*)", options=options)
                with open(filename[0]) as f:
                    self.ui.plainTextEdit.setPlainText(QtCore.QCoreApplication.translate('MainWindow', f.read()))
                    self.activeFile = filename[0]
                if self.activeFile:
                    self.setWindowTitle('{0} - PyEditor'.format(window.activeFile))
                elif self.activeFile == None:
                    self.setWindowTitle('PyEditor')
            if msg == QMessageBox.Cancel:
                # cancel open the chosen document if the user doesnt want to skip nor continue saving
                pass
    
    def actionSave(self):
        if self.activeFile:
            with open(self.activeFile, 'w') as f:
                f.write(self.ui.plainTextEdit.document().toPlainText())
        elif self.activeFile == None:
            self.actionSaveAs()
        else:
            raise FileNotFoundError

    
    def actionSaveAs(self):
        options = QFileDialog.Options()
        filename = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()", "","All Files (*)", options=options)
        print(filename[0])
        with open(filename[0], 'w') as f:
            f.write(self.ui.plainTextEdit.document().toPlainText())

    def actionExit(self):
        if self.checkSaved():
            QApplication.quit()
        else:
            msg = self.overwriteWarning()
            if msg == QMessageBox.Yes:
                self.actionSave()
                QApplication.quit()
            elif msg == QMessageBox.No:
                QApplication.quit()
            elif msg == QMessageBox.Cancel:
                pass

    def overwriteWarning(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText('Would you like to save your changes before closing this document?')
        msg.setWindowTitle('Save Changes?')
        msg.setDetailedText('Unsaved changes in the following files: \n\n{0}'.format(self.activeFile))
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel | QMessageBox.No)
        return msg.exec_()

    def checkSaved(self):
        try:
            with open(self.activeFile) as f:
                return True if f.read() == self.ui.plainTextEdit.document().toPlainText() else False
        except TypeError:
            return True if self.ui.plainTextEdit.document().toPlainText() == '' else False
        
        

if __name__ == '__main__':
    import sys

    pyqtRemoveInputHook()
    app = QApplication(sys.argv)
    window = MyApp()

    window.setWindowTitle('PyEditor')
    #window.showMaximized()
    window.show()

    sys.exit(app.exec())
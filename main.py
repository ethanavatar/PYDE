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
from PyQt5.QtCore import pyqtRemoveInputHook
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QFileDialog, QPlainTextEdit
from PyQt5 import uic

Ui_MainWindow, QtBaseClass = uic.loadUiType('EditorUI.ui')

class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__(None)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow = self)

        self.ui.actionNew.triggered.connect(self.onNew)
        self.ui.actionOpen.triggered.connect(self.onOpen)

        self.ui.actionSave.triggered.connect(self.onSave)
        self.ui.actionSave_As.triggered.connect(self.onSaveAs)

        self.ui.actionExit.triggered.connect(QApplication.quit)
    
    def onNew(self):
        self.ui.plainTextEdit.setPlainText(QtCore.QCoreApplication.translate('MainWindow', ''))

    def onOpen(self):
        options = QFileDialog.Options()
        filename = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        with open(filename[0]) as f:
            self.ui.plainTextEdit.setPlainText(QtCore.QCoreApplication.translate('MainWindow', f.read()))
            self.activeFile = filename[0]
    
    def onSave(self):
        with open(self.activeFile, 'w') as f:
            f.write(self.ui.plainTextEdit.document().toPlainText())

    
    def onSaveAs(self):
        options = QFileDialog.Options()
        filename = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        print(filename[0])
        with open(filename[0], 'w') as f:
            f.write(self.ui.plainTextEdit.document().toPlainText())


if __name__ == '__main__':
    import sys

    pyqtRemoveInputHook()
    app = QApplication(sys.argv)
    window = MyApp()

    window.setWindowTitle('PyEditor')
    window.showMaximized()
    window.show()

    sys.exit(app.exec())
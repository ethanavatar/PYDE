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

from PyQt5.QtCore import pyqtRemoveInputHook
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction
from PyQt5 import uic

Ui_MainWindow, QtBaseClass = uic.loadUiType('EditorUI.ui')

class MyApp(QMainWindow):
    def __init__(self):
        self.newLines = 1
        super(MyApp, self).__init__(None)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == '__main__':
    import sys

    pyqtRemoveInputHook()
    app = QApplication(sys.argv)
    window = MyApp()

    window.setWindowTitle('PyEditor')
    window.showMaximized()
    window.show()

    sys.exit(app.exec())
from PyQt5.QtWidgets import QErrorMessage
from PyQt5.QtWidgets import QMessageBox


def handleError(error):
    em = QErrorMessage.qtHandler()
    em.showMessage(str(error))

def handleCompileMsg():
    msg_box = QMessageBox(QMessageBox.Question, 'Compile Code!', 'There are changes to your code that have not been compiled. \
                                                 If you do not compile your code before exporting you will lose those changes.')
    msg_box.exec_()
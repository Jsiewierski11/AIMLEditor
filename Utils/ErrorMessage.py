from PyQt5.QtWidgets import QErrorMessage
from PyQt5.QtWidgets import QMessageBox


def handleError(error):
    em = QErrorMessage.qtHandler()
    em.showMessage(str(error))

def handleCompileMsg():
    msg_box = QMessageBox(QMessageBox.Warning, 'Compile Code!', 'There are changes to your code that have not been compiled. \
                                                If you do not compile your code before exporting you will lose those changes. \
                                                Would you like to compile before you export?')
    msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    
    retval = msg_box.exec_()
    return retval
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QMessageBox
import xml.etree.ElementTree as ET
from Model.Data import *

class QLabelClickable(QLabel):

    # initializing signal for click or double click events
    catClicked = pyqtSignal()

    def __init__(self, parent=None):
        super(QLabelClickable, self).__init__(parent)
        self.templateText = ""
        self. patternText = ""
        self.patternFont = QFont("Ubuntu", 13, QFont.Bold)
        self.templateFont = QFont("Ubuntu", 13, True)

    def mousePressEvent(self, event):
        self.last = "Click"

    def mouseReleaseEvent(self, even):
        if self.last == "Click":
            QTimer.singleShot(QApplication.instance().doubleClickInterval(), self.performSingleClickAction)
        else:
            # emmit to Editor Widget, Editor Widget sends cat to Window then to Docker
            self.catClicked.emit()

    def mouseDoubleClickEvent(self, event):
        self.last = "Double Click"

    def performSingleClickAction(self):
        if self.last == "Click":
            # emmit to Editor Widget, Editor Widget sends cat to Window then to Docker
            self.catClicked.emit()

    def displayVisuals(self, category):
        self.clear()
        print("creating visuals for the label")
        root = ET.fromstring(str(category))
        self.template = Template()
        self.pattern = Pattern()
        self.condition = Condition()
        self.random = Random()

        self.template = self.parseTree(root)
        self.templateText = str(self.template)
        self.patternText = str(self.pattern)
        text_to_set = 'pattern: ' + self.patternText + '\ntemplate: ' + self.templateText
        self.setText(text_to_set)

    def parseTree(self, root):
        print("parsing through category tree to get desired text")
        for child in root:
            if child.tag == "template":
                if child.findall("*") is None:
                    if child.text is None:
                        print("child.text is None")
                        print("child.text for template: " + str(child.text))
                        self.template.append("")
                    else:
                        print("child.text for template: " + child.text)
                        self.template.append(child.text)
                else:
                    self.template.append(child.text)
                    self.parseTree(child)
            elif child.tag == "pattern":
                if child.text is None:
                    print("child.text is None")
                    print("child.text for pattern: " + str(child.text))
                    self.pattern.append("")
                else:
                    print("child.text for pattern: " + child.text)
                    self.pattern.append(child.text)
            elif child.tag == "condition":
                self.parseTree(child)
                self.condition.attrib['name'] = child.attrib['name']
                self.template.append(self.condition)
                self.template.append(child.tail)
            elif child.tag == "random":
                self.parseTree(child)
                self.template.append(self.random)
                self.template.append(child.tail)
            elif child.tag == "think":
                think = Think()
                think.append(child.text)
                self.template.append(think)
            elif child.tag == "li":
                if child.attrib is None:
                    conItem = ConditionItem()
                    conItem.append(child.text)
                    self.random.append(conItem)
                else:
                    conItem = ConditionItem()
                    conItem.append(child.text)
                    conItem.attrib = child.attrib
                    self.condition.append(conItem)
            else:
                print("do nothing")
        self.template.attrib = []
        self.pattern.attrib = []
        return self.template

class LabelClickable(QDialog):
    def __init__(self, parent=None):
        super(LabelClickable, self).__init__(parent)

        self.setWindowTitle("Category")
        self.setWindowIcon(QIcon("icon.png"))
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        self.setFixedSize(350, 350)

        self.initUI()

    def initUI(self):
        self.imageLabel = QLabelClickable(self)
        self.imageLabel.setGeometry(0, 0, 350, 350)
        self.imageLabel.setToolTip("Edit category")
        self.imageLabel.setCursor(Qt.PointingHandCursor)

        self.imageLabel.setStyleSheet("QLabel {background-color: white; color: black; border: 1px solid "
                                      "#01DFD7; border-radius: 5px;}")

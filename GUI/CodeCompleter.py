from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QCompleter

class CodeCompleter(QCompleter):
    insertText = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        QCompleter.__init__(self, parent)

        # AIML keywords
        self.keywords = [
            "category",
            "aiml",
            "topic",
            "category",
            "pattern",
            "template",
            "condition",
            "li",
            "random",
            "set",
            "think",
            "that",
            "oob",
            "robot",
            "options",
            "option",
            "image",
            "video",
            "filename",
            "get",
            "srai",
            "star"
        ]
        self.setCompletionMode(QCompleter.PopupCompletion)
        self.activated.connect(self.setHighlighted)

    def setHighlighted(self, text):
        print("IN SETHIGHLIGHTED!!")
        self.lastSelected = text

    def getSelected(self):
        return self.lastSelected
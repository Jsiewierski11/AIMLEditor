# from PyQt5 import QtGui, QtCore, QtWidgets
# from PyQt5.QtWidgets import QCompleter

# class CodeCompleter(QCompleter):
#     insertText = QtCore.pyqtSignal(str)

#     def __init__(self, parent=None):
#         # AIML keywords
#         self.keywords = [
#             "category",
#             "aiml",
#             "topic",
#             "category",
#             "pattern",
#             "template",
#             "condition",
#             "li",
#             "random",
#             "set",
#             "think",
#             "that",
#             "oob",
#             "robot",
#             "options",
#             "option",
#             "image",
#             "video",
#             "filename",
#             "get",
#             "srai",
#             "star"
#         ]
#         QCompleter.__init__(self, self.keywords, parent)
#         self.setCompletionMode(QCompleter.PopupCompletion)
#         self.insertText.connect(self.setHighlighted)
#         self.lastSelected = "hey"

#     def setHighlighted(self, text):
#         print("IN SET HIGHLIGHTED!!")
#         print(f"text: {text}")
#         self.lastSelected = text

#     def getSelected(self):
#         return self.lastSelected
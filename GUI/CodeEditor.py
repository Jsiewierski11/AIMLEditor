#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
Licensed under the terms of the MIT License
https://github.com/luchko/QCodeEditor
@author: Ivan Luchko (luchko.ivan@gmail.com)
This module contains the light QPlainTextEdit based QCodeEditor widget which
provides the line numbers bar and the syntax and the current line highlighting.
    class XMLHighlighter(QSyntaxHighlighter):
    class QCodeEditor(QPlainTextEdit):

testing and examples:
    def run_test():
Module is compatible with both pyQt4 and pyQt5
'''
try:
    import PyQt4 as PyQt

    pyQtVersion = "PyQt4"

except ImportError:
    try:
        import PyQt5 as PyQt

        pyQtVersion = "PyQt5"
    except ImportError:
        raise ImportError("neither PyQt4 or PyQt5 is found")

# imports requied PyQt modules
if pyQtVersion == "PyQt4":
    from PyQt4.QtCore import Qt, QRect, QRegExp
    from PyQt4.QtGui import (QWidget, QTextEdit, QPlainTextEdit, QColor,
                             QPainter, QFont, QSyntaxHighlighter,
                             QTextFormat, QTextCharFormat, QPalette)
else:
    from PyQt5 import QtWidgets
    from PyQt5.QtCore import Qt, QRect, QRegExp, pyqtSlot, QFileInfo, pyqtSignal, QFile, QStringListModel
    from PyQt5.QtWidgets import QWidget, QTextEdit, QPlainTextEdit, QErrorMessage, QCompleter, QApplication
    from PyQt5.QtGui import (QColor, QPainter, QFont, QSyntaxHighlighter, QCursor,
                             QTextFormat, QTextCharFormat, QPalette, QTextCursor)
    from Model.Data import *
    import Utils.AIMLHighlighter as HL
    import re


def handleError(error):
    em = QErrorMessage.qtHandler()
    em.showMessage(str(error))


DEBUG = False



class QCodeEditor(QPlainTextEdit):
    '''
    QCodeEditor inherited from QPlainTextEdit providing:

        numberBar - set by DISPLAY_LINE_NUMBERS flag equals True
        curent line highligthing - set by HIGHLIGHT_CURRENT_LINE flag equals True
        setting up QSyntaxHighlighter
    references:
        https://john.nachtimwald.com/2009/08/19/better-qplaintextedit-with-line-numbers/
        http://doc.qt.io/qt-5/qtwidgets-widgets-codeeditor-example.html
    '''
    # Adding signal
    catCreated = pyqtSignal(Tag)

    class NumberBar(QWidget):
        '''class that deifnes textEditor numberBar'''

        def __init__(self, editor):
            QWidget.__init__(self, editor)

            self.editor = editor
            self.editor.blockCountChanged.connect(self.updateWidth)
            self.editor.updateRequest.connect(self.updateContents)
            self.font = QFont()
            self.numberBarColor = QColor("#e8e8e8")

        def paintEvent(self, event):
            painter = QPainter(self)
            painter.fillRect(event.rect(), self.numberBarColor)

            block = self.editor.firstVisibleBlock()

            # Iterate over all visible text blocks in the document.
            while block.isValid():
                blockNumber = block.blockNumber()
                block_top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()

                # Check if the position of the block is outside of the visible area.
                if not block.isVisible() or block_top >= event.rect().bottom():
                    break

                # We want the line number for the selected line to be bold.
                if blockNumber == self.editor.textCursor().blockNumber():
                    self.font.setBold(True)
                    painter.setPen(QColor("#000000"))
                else:
                    self.font.setBold(False)
                    painter.setPen(QColor("#717171"))
                painter.setFont(self.font)

                # Draw the line number right justified at the position of the line.
                paint_rect = QRect(0, block_top, self.width(), self.editor.fontMetrics().height())
                painter.drawText(paint_rect, Qt.AlignRight, str(blockNumber + 1))

                block = block.next()

            painter.end()

            QWidget.paintEvent(self, event)

        def getWidth(self):
            count = self.editor.blockCount()
            width = self.fontMetrics().width(str(count)) + 10
            return width

        def updateWidth(self):
            width = self.getWidth()
            if self.width() != width:
                self.setFixedWidth(width)
                self.editor.setViewportMargins(width, 0, 0, 0)

        def updateContents(self, rect, scroll):
            if scroll:
                self.scroll(0, scroll)
            else:
                self.update(0, rect.y(), self.width(), rect.height())

            if rect.contains(self.editor.viewport().rect()):
                fontSize = self.editor.currentCharFormat().font().pointSize()
                self.font.setPointSize(fontSize)
                self.font.setStyle(QFont.StyleNormal)
                self.updateWidth()

    def __init__(self, tab_controller, DISPLAY_LINE_NUMBERS=True, HIGHLIGHT_CURRENT_LINE=True,
                 SyntaxHighlighter=None, theme_color='light', *args):
        '''
        Parameters
        ----------
        DISPLAY_LINE_NUMBERS : bool
            switch on/off the presence of the lines number bar
        HIGHLIGHT_CURRENT_LINE : bool
            switch on/off the current line highliting
        SyntaxHighlighter : QSyntaxHighlighter
            should be inherited from QSyntaxHighlighter
        theme_color : string
            gets set by TabController
        '''
        super(QCodeEditor, self).__init__()

        self.theme_color = theme_color

        # Code completer object, gets set by the TabController
        self._completer = None
        
        if self.theme_color == 'dark':
            # Setting background color to dark blue
            palette = self.palette()
            palette.setColor(QPalette.Active, QPalette.Base, QColor(0, 39, 97))
            palette.setColor(QPalette.Active, QPalette.Text, QColor(255, 255, 255))
            self.setPalette(palette)
            self.setBackgroundVisible(False)

        self.setFont(QFont("Ubuntu Mono", 11))
        self.setLineWrapMode(QPlainTextEdit.NoWrap)

        self.DISPLAY_LINE_NUMBERS = DISPLAY_LINE_NUMBERS

        # connecting slot for category creation
        self.aiml = AIML()
        self.make_connection(tab_controller)   
           

        self.setReadOnly(False)

        if DISPLAY_LINE_NUMBERS:
            self.number_bar = self.NumberBar(self)

        if HIGHLIGHT_CURRENT_LINE:
            self.currentLineNumber = None
            # self.currentLineColor = self.palette().alternateBase()
            if self.theme_color == 'light': self.currentLineColor = QColor("#f6f79e")
            if self.theme_color == 'dark': self.currentLineColor = QColor("#84852a")
            self.cursorPositionChanged.connect(self.highligtCurrentLine)

        if SyntaxHighlighter is None:  # add highlighter to textdocument
            self.highlighter = HL.AIMLHIghlighter(self.document(), styles=self.theme_color)
        
        self.setPlainText('\n\n\n\n\n\n\n\n\n\n')
        

    def setThemeColor(self, color):
        self.theme_color=color

        if self.theme_color == 'dark':
            # Setting background color to dark blue
            palette = self.palette()
            palette.setColor(QPalette.Active, QPalette.Base, QColor(0, 39, 97))
            palette.setColor(QPalette.Active, QPalette.Text, QColor(255, 255, 255))
            self.setPalette(palette)
            self.setBackgroundVisible(False)

        if self.theme_color == 'light':
            palette = self.palette()
            self.setPalette(palette)


    def resizeEvent(self, *e):
        '''overload resizeEvent handler'''
        if DEBUG: print("Resized called")
        if self.DISPLAY_LINE_NUMBERS:  # resize number_bar widget
            cr = self.contentsRect()
            rec = QRect(cr.left(), cr.top(), self.number_bar.getWidth(), cr.height())
            self.number_bar.setGeometry(rec)

        QPlainTextEdit.resizeEvent(self, *e)

    def highligtCurrentLine(self):
        newCurrentLineNumber = self.textCursor().blockNumber()
        if newCurrentLineNumber != self.currentLineNumber:
            self.currentLineNumber = newCurrentLineNumber
            hi_selection = QTextEdit.ExtraSelection()
            hi_selection.format.setBackground(self.currentLineColor)
            hi_selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            hi_selection.cursor = self.textCursor()
            hi_selection.cursor.clearSelection()
            self.setExtraSelections([hi_selection])

    # function to make connection with signal in TabController
    def make_connection(self, tab_controller):
        tab_controller.catCreated.connect(self.categoryCreated)
        tab_controller.catUpdated.connect(self.categoryUpdated)

    def setCompleter(self, completer):
        if self._completer is not None:
            self._completer.activated.disconnect()

        self._completer = completer

        completer.setWidget(self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.activated.connect(self.insertCompletion)

    def insertCompletion(self, completion):
        if self._completer.widget() is not self:
            return

        tc = self.textCursor()
        extra = len(completion) - len(self._completer.completionPrefix())-1
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)

    def textUnderCursor(self):
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def focusInEvent(self, e):
        if self._completer is not None:
            self._completer.setWidget(self)
        super().focusInEvent(e)

    def keyPressEvent(self, e):
        if self._completer is not None and self._completer.popup().isVisible():
            # The following keys are forwarded by the completer to the widget.
            if e.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab):
                e.ignore()
                # Let the completer do default behavior.
                return
        
        isShortcut = ((e.modifiers() & Qt.ControlModifier) != 0 and e.key() == Qt.Key_E)
        if self._completer is None or not isShortcut:
            # Do not process the shortcut when we have a completer.
            super().keyPressEvent(e)

        ctrlOrShift = e.modifiers() & (Qt.ControlModifier | Qt.ShiftModifier)
        if self._completer is None or (ctrlOrShift and len(e.text()) == 0):
            return

        eow = "~!@#$%^&*()_+{}|:\"?,.;'[]\\-="
        hasModifier = (e.modifiers() != Qt.NoModifier) and not ctrlOrShift
        completionPrefix = self.textUnderCursor()

        if not isShortcut and (hasModifier or len(e.text()) == 0 or len(completionPrefix) < 2 or e.text()[-1] in eow):
            self._completer.popup().hide()
            return

        if completionPrefix != self._completer.completionPrefix():
            self._completer.setCompletionPrefix(completionPrefix)
            self._completer.popup().setCurrentIndex(
                    self._completer.completionModel().index(0, 0))

        cr = self.cursorRect()
        cr.setWidth(self._completer.popup().sizeHintForColumn(0) + self._completer.popup().verticalScrollBar().sizeHint().width())
        try:
            self._completer.complete(cr)
        except Exception as ex:
            print(f"Error occured while showing completion popup: {ex}")

    # slot function for a category being created and displaying on editSpace
    @pyqtSlot(Tag)
    def categoryCreated(self, aiml):
        try:
            if DEBUG: print("In CodeEditor Slot - categoryCreated()")
            self.setPlainText(str(aiml))
        except Exception as ex:
            handleError(ex)
            print("Exception caught in CodeEditor - categoryCreated()")
            print(ex)

    # Slot function for updating categories.
    @pyqtSlot(Tag)
    def categoryUpdated(self, aiml):
        if DEBUG: print("In CodeEditor Slot - categoryUpdated()")
        if DEBUG: print(f"aiml object to set (CodeEditor):\n{aiml}")
        try:
            self.setPlainText(str(aiml))
            if DEBUG: print("Updated CodeEditor successfully")
        except Exception as ex:
            handleError(ex)
            print("Exception caught in CodeEditor - categoryUpdated()")
            print(ex)
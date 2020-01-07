import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Utils.ErrorMessage import handleError


DEBUG = True


class QDMGraphicsScene(QGraphicsScene):
    def __init__(self, scene, parent=None):
        try:
            if DEBUG: print("In __init__ of GraphicsScene")
            super().__init__(parent)

            self.scene = scene

            # settings
            self.gridSize = 20
            self.gridSquares = 5

            self._color_background = QColor("#393939")
            self._color_light = QColor("#2f2f2f")
            self._color_dark = QColor("#292929")

            self._pen_light = QPen(self._color_light)
            self._pen_light.setWidth(1)
            self._pen_dark = QPen(self._color_dark)
            self._pen_dark.setWidth(2)

            self.setBackgroundBrush(self._color_background)
        except Exception as ex:
            print("Exception caught in GraphicsScene - __init__()")
            print(ex)
            handleError(ex)

    def setGrScene(self, width, height):
        try:
            if DEBUG: print("Setting graphics scene")
            self.setSceneRect(-width // 2, -height // 2, width, height)
        except Exception as ex:
            print("Exception caught in GraphicsScene - setGrScene()")
            print(ex)
            handleError(ex)

    def drawBackground(self, painter, rect):
        try:
            if DEBUG: print("drawing background")
            super().drawBackground(painter, rect)

            # here we create our grid
            left = int(math.floor(rect.left()))
            right = int(math.ceil(rect.right()))
            top = int(math.floor(rect.top()))
            bottom = int(math.ceil(rect.bottom()))

            first_left = left - (left % self.gridSize)
            first_top = top - (top % self.gridSize)

            # compute all lines to be drawn
            lines_light, lines_dark = [], []
            for x in range(first_left, right, self.gridSize):
                if (x % (self.gridSize*self.gridSquares) != 0): lines_light.append(QLine(x, top, x, bottom))
                else: lines_dark.append(QLine(x, top, x, bottom))

            for y in range(first_top, bottom, self.gridSize):
                if (y % (self.gridSize*self.gridSquares) != 0): lines_light.append(QLine(left, y, right, y))
                else: lines_dark.append(QLine(left, y, right, y))

            # draw the lines
            painter.setPen(self._pen_light)
            painter.drawLines(*lines_light)

            painter.setPen(self._pen_dark)
            painter.drawLines(*lines_dark)
            if DEBUG: print("finished drawing backgroud")
        except Exception as ex:
            print("Exception caught in GraphicsScene - drawBackground()")
            print(ex)
            handleError(ex)
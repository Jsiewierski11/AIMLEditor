import unittest
import os, sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import * 
from pytestqt import *

sys.path.append(os.path.abspath('..'))
from GUI.EditorWindow import EditorWindow
from GUI.DockerWidget import DockerWidget


class TestFunctions(unittest.TestCase):

    def test_update_category(self):
        app = QApplication(sys.argv)
        wnd = EditorWindow()
        wnd.show()


if __name__ == '__main__':
    unittest.main()
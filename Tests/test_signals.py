import unittest
import os, sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import * 
from pytestqt import *

sys.path.append(os.path.abspath('..'))
import Utils.Storage as Storage
from Model.Data import *
from GUI.EditorWindow import EditorWindow
from GUI.DockerWidget import DockerWidget


class TestFunctions(unittest.TestCase):

    def test_import_jupiter(self):
        app = QApplication(sys.argv)
        wnd = EditorWindow()
        wnd.show()
        wnd.onFileImport()
        aiml = wnd.editSpace.aiml

        imported = Storage.importAIML('./test_aimls/jupiter')
        self.assertEqual(str(aiml), str(imported))


if __name__ == '__main__':
    unittest.main()
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



# HACK: Trying to implement example for the docs.
#       Not working though, throwing error on connect
'''
def test_long_computation(qtbot):
    # app = QApplication(sys.argv)

    wnd = EditorWindow()

    # Watch for the app.worker.finished signal, then start the worker.
    with qtbot.waitSignal(wnd.categoryCreated, timeout=10000) as blocker:
        blocker.connect(wnd.categoryCreated.failed)  # Can add other signals to blocker
        wnd.categoryCreated.start()
        # Test will block at this point until either the "finished" or the
        # "failed" signal is emitted. If 10 seconds passed without a signal,
        # TimeoutError will be raised.

    assert_application_results(app)
'''
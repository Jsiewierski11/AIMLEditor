from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget, QPushButton, QVBoxLayout
from GUI.CodeEditor import *
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, pyqtSlot, QFileInfo, pyqtSignal
from GUI.DockerWidget import DockerWidget
from Model.Data import *

class TabController(QWidget):

     # Adding signal
    catCreated = pyqtSignal(Tag)
    catClicked = pyqtSignal(Tag)
    catUpdated = pyqtSignal(Tag)
    childClicked = pyqtSignal(str)
    
    def __init__(self, parent, docker):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.editSpace = None # Used for displaying source code
        self.docker = docker
        self.aiml = AIML()
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300,200)
        
        # Add tabs
        self.tabs.addTab(self.tab1,"Text Display")
        self.tabs.addTab(self.tab2,"Graph Display")
        
        # Create first tab
        self.add_editspace(self.tab1, self.docker)
        
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        # Make Connection
        self.docker.catCreated.connect(self.categoryCreated)

    def add_editspace(self, tab, docker):
        tab.layout = QVBoxLayout(self)
        # Setting main editing area where Files will be displayed and can be edited
        self.editSpace = QCodeEditor(docker)
        self.tab1.layout.addWidget(self.editSpace)
        tab.setLayout(tab.layout)

    # slot function for a category being created and displaying on editSpace
    @pyqtSlot(Tag)
    def categoryCreated(self, cat):
        print("In TabController slot")
        try:
            self.aiml.append(cat)
        except Exception as ex:
            handleError(ex)
            print("exception caught!")
            print(ex)
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QGridLayout, \
                            QTabWidget, QPushButton, QVBoxLayout, QLabel
from GUI.CodeEditor import *
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, pyqtSlot, QFileInfo, pyqtSignal
from GUI.DockerWidget import DockerWidget
from GUI.EditorWidget import EditorWidget
from GUI.Node.Node import Node
from Model.Data import *

class TabController(QWidget):

     # Adding signal
    catCreated = pyqtSignal(Tag)
    catClicked = pyqtSignal(Tag)
    catUpdated = pyqtSignal(Tag)
    childClicked = pyqtSignal(str)
    
    def __init__(self, parent, docker, window):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.editSpace = None # Used for displaying source code
        self.graphview = None # Used for the graphical display
        self.aiml = None # THIS SHOULD BE THE ONLY MODEL IN THE SYSTEM
        self.docker = docker
        self.window = window
        self.up_to_date = True
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300,200)
        
        # Add tabs
        self.tabs.addTab(self.tab1,"Text Display")
        self.tabs.addTab(self.tab2,"Graph Display")
        
        # Create tabs
        self.add_editspace(self.tab1)
        self.add_graphview(self.tab2)
        
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        # Make Connection
        self.docker.catCreated.connect(self.categoryCreated)
        self.window.catCreated.connect(self.categoryCreated)
        self.docker.catUpdated.connect(self.categoryUpdated) # connecting signal from EditorWindow to update Node
        self.editSpace.textChanged.connect(self.editsMade)  

    def editsMade(self):
        self.tabs.setStyleSheet('QTabBar::tab {background-color: red;}')
        self.up_to_date = False
        print("Text has been changed!!")

    def add_editspace(self, tab):
        tab.layout = QVBoxLayout(self)
        # Setting main editing area where Files will be displayed and can be edited
        self.editSpace = QCodeEditor(self)
        self.tab1.layout.addWidget(self.editSpace)
        tab.setLayout(tab.layout)

    def add_graphview(self, tab):
        tab.layout = QGridLayout(self)
        # Setting of backdrop for view categories as nodes.
        self.graphview = EditorWidget(self)

        # Building legend and zoom buttons
        self.add_legend()        

        # Adding widgets to layout
        self.tab2.layout.addWidget(self.legendLabel, 0, 0)
        self.tab2.layout.addWidget(self.zoom_out, 0, 1)
        self.tab2.layout.addWidget(self.zoom_in, 0, 2)
        self.tab2.layout.addWidget(self.graphview, 1, 0, 1, 3)

        # Making button connections
        self.zoom_out.clicked.connect(self.zoom_out_clicked)
        self.zoom_in.clicked.connect(self.zoom_in_clicked)

        # Setting layout
        tab.setLayout(tab.layout)


    def add_legend(self):
        # Creating buttons to zoom in and out of the graph scene
        self.zoom_out = QPushButton("-")
        self.zoom_out.resize(50, 50)
        self.zoom_in = QPushButton("+")
        self.zoom_in.resize(50, 50)

        # Creating legend to clarify what fields in nodes mean
        self.legendLabel = QLabel()
        self.legendLabel.setFont(QFont("Sanserif", 10))
        self.legendLabel.setText("1st textbox represents the Pattern Tag\n"
                                 "2nd textbox represents the That Tag\n"
                                 "3rd textbox represents the Template Tag")
        self.legendLabel.setStyleSheet("QLabel {background-color: black; color: white; border: 1px solid "
                                       "#01DFD7; border-radius: 5px;}")


    def zoom_in_clicked(self):
        print("Zoom In Clicked")
        zoomFactor = self.graphview.view.zoomInFactor
        zoomFactor += self.graphview.view.zoomStep
        self.graphview.view.scale(zoomFactor, zoomFactor)


    def zoom_out_clicked(self):
        print("Zoom Out Clicked")
        zoomFactor = self.graphview.view.zoomInFactor
        zoomFactor -= (self.graphview.view.zoomStep * 0.5)
        self.graphview.view.scale(zoomFactor, zoomFactor)


    # slot function for a category being created and displaying on editSpace
    @pyqtSlot(Tag)
    def categoryCreated(self, cat):
        # This is for the CodeEditor
        try:
            print("In TabController Slot - categoryCreated()")
            if self.aiml is not None:
                print(f"Current aiml Model:\n{self.aiml}")
                print("Ok to add category")
                self.aiml.append(cat)
                print("appended category to AIML object")
                self.catCreated.emit(self.aiml)
            else:
                print("CodeEditor is equal to None")
                self.aiml = AIML()
                # self.clear()
                self.aiml.append(cat)
                print("appended category to AIML object")
                self.catCreated.emit(self.aiml)
        except Exception as ex:
            handleError(ex)
            print("Exception caught in TabController case 1 - categoryCreated()")
            print(ex)

        # This is for the EditorWidget
        try:
            if cat.type == "topic":
                # Iterate through topic and place categories
                for category in cat.tags:
                    thatToCheck = self.graphview.getLastSentence(category)
                    print("got last sentence of category")
                    title = "Category: " + category.id
                    aNode = Node(self.graphview.scene, title, category)
                    print("created node")
                    aNode.content.wdg_label.displayVisuals(category)
                    print("displayed contents on node")

                    if thatToCheck is not None:
                        for that in thatToCheck:
                            self.graphview.findChildNodes(aNode, that)
                    
                    # FIXME: Why aren't nodes getting placed?
                    self.graphview.findParentNodes(aNode)
                    self.graphview.placeNodes(self.graphview.scene.nodes)

                    for node in self.graphview.scene.nodes:
                        node.updateConnectedEdges()

                    aNode.content.catClicked.connect(self.graphview.categoryClicked) # connecting signals coming from Content Widget
                    print("trying to connect addChild button")
                    aNode.content.childClicked.connect(self.graphview.addChildClicked) # connecting signals coming from Content Widget
            else:
                thatToCheck = self.graphview.getLastSentence(cat)
                print("got last sentence of category")
                title = "Category: " + cat.id
                aNode = Node(self.graphview.scene, title, cat)
                print("created node")
                aNode.content.wdg_label.displayVisuals(cat)
                print("displayed contents on node")

                if thatToCheck is not None:
                    for that in thatToCheck:
                        self.graphview.findChildNodes(aNode, that)
                
                self.graphview.findParentNodes(aNode)
                self.graphview.placeNodes(self.graphview.scene.nodes)

                for node in self.graphview.scene.nodes:
                    node.updateConnectedEdges()

                aNode.content.catClicked.connect(self.graphview.categoryClicked) # connecting signals coming from Content Widget
                print("trying to connect addChild button")
                aNode.content.childClicked.connect(self.graphview.addChildClicked) # connecting signals coming from Content Widget
        except Exception as ex:
            print("Exception caught in TabController case 2 - categoryCreated()")
            print(ex)
            handleError(ex)

    # Slot function for updating categories.
    @pyqtSlot(Tag)
    def categoryUpdated(self, cat):
        print("slot in TabController - categoryUpdated()")
        try:
            updatedCat = self.aiml.update(cat)
            print(f'Updated aiml object:\n{self.aiml}')
            updatedNode = self.graphview.updateNode(cat)
            thatStr = self.graphview.getLastSentence(cat)
            self.graphview.findParentNodes(updatedNode)
            that = cat.findTag("that")
            if that is not None:
                self.graphview.findChildNodes(updatedNode, thatStr)
            print("display updated")
            print("updated category")
            print(str(updatedCat))
            self.catUpdated.emit(self.aiml) # Sending the updated aiml object to the CodeEditor.
        except Exception as ex:
            print("Exception caught trying to update Node in TabController")
            print(ex)

    # Slot function for when a category is clicked in the graphical view.
    @pyqtSlot(Tag)
    def categoryClicked(self, cat):
        print("slot in EditorWidget - categoryClicked()")
        try:
            cat = self.aiml.find(cat.id)
            print(cat)
            self.catClicked.emit(cat) # emitting signal to be sent to EditorWindow
        except Exception as ex:
            print("Exception caught when category is clicked.")
            print(ex)
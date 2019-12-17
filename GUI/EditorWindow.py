import os
import json
from PyQt5.QtWidgets import QMainWindow, QLabel, QAction, QMessageBox, QApplication, QFileDialog, QTextEdit, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, pyqtSlot, QFileInfo
from GUI.EditorWidget import EditorWidget
from GUI.DockerWidget import DockerWidget
from GUI.TabController import TabController
from GUI.Find import Find
from Model.Data import *
import Utils.Storage as Storage
import Utils.AIMLHighlighter as HL
from GUI.CodeEditor import *
from GUI.QLabel_Clickable import *
from GUI.Node.QDM.GraphicsScene import *
from Utils.ErrorMessage import handleError, handleCompileMsg


DEBUG = True


class EditorWindow(QMainWindow):

    # Adding signal
    catCreated = pyqtSignal(Tag)
    catClicked = pyqtSignal(Tag)
    catUpdated = pyqtSignal(Tag)
    childClicked = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.filename = None
        self.editSpace = None # Used for displaying source code
        self.display = None # Used for graphing out categories
        self.aiml = AIML()

        # create dockable widget to have as place to write content in categories
        # Creating docker that can create categories
        self.docker = DockerWidget(self)

        self.initUI()


    def createAct(self, name, shortcut, tooltip, callback):
        act = QAction(name, self)
        act.setShortcut(shortcut)
        act.setToolTip(tooltip)
        act.triggered.connect(callback)
        return act

    def initUI(self):
        menubar = self.menuBar()
        
        # initialize Menu
        fileMenu = menubar.addMenu('&File')
        
        #NOTE: These are unneeded menu options since we do not have the graph view
        # fileMenu.addAction(self.createAct('&New', 'Ctrl+N', "Create new graph", self.onFileNew))
        # fileMenu.addSeparator()
        # fileMenu.addAction(self.createAct('&Open', 'Ctrl+O', "Open file", self.onFileOpen))
        # fileMenu.addAction(self.createAct('&Save', 'Ctrl+S', "Save file", self.onFileSave))
        # fileMenu.addAction(self.createAct('Save &As...', 'Ctrl+Shift+S', "Save file as...", self.onFileSaveAs))
        fileMenu.addAction(self.createAct('&Export', 'Ctrl+Shift+E', 'Export File', self.onFileExport))
        fileMenu.addAction(self.createAct('&Import', 'Ctrl+Shift+I', 'Import File', self.onFileImport))
        fileMenu.addSeparator()
        fileMenu.addAction(self.createAct('&Find', 'Ctrl+F', 'Find Word in File', self.onFind))
        fileMenu.addSeparator()
        fileMenu.addAction(self.createAct('E&xit', 'Ctrl+Q', "Exit application", self.close))

        editMenu = menubar.addMenu('&Edit')
        editMenu.addAction(self.createAct('&Undo', 'Ctrl+Z', "Undo last operation", self.onEditUndo))
        editMenu.addAction(self.createAct('&Redo', 'Ctrl+Shift+Z', "Redo last operation", self.onEditRedo))
        editMenu.addAction(self.createAct('Cu&t', 'Ctrl+X', "Cut to clipboard", self.onEditCut))
        editMenu.addAction(self.createAct('&Copy', 'Ctrl+C', "Copy to clipboard", self.onEditCopy))
        editMenu.addAction(self.createAct('&Paste', 'Ctrl+V', "Paste from clipboard", self.onEditPaste))
        # editMenu.addSeparator()
        # editMenu.addAction(self.createAct('&Delete', 'Del', "Delete selected items", self.onEditDelete))
        # editMenu.addSeparator()
        # editMenu.addAction(self.createAct('&Add a Node', 'Ctrl+A', "Add a new node", self.onEditAdd))

        compileMenu = menubar.addMenu('Compile')
        compileMenu.addAction(self.createAct('Compile project', 'Ctrl+Shift+C', 'Compile project to export', self.onCompile))


        # create dockable widget to have as place to write content in categories
        # Creating docker that can create categories
        # docker = None
        # docker = DockerWidget(self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.docker)

        # Creating table to hold and control tabs
        # self.tab_controller = TabController(self)
        self.editSpace = TabController(self, self.docker, window=self)
        self.setCentralWidget(self.editSpace)

        # Setting main editing area where Files will be displayed and can be edited
        # self.editSpace = QCodeEditor(docker)
        # self.setCentralWidget(self.editSpace)


        # create node editor widget (visualization of categories)
        # self.editSpace = EditorWidget(self)
        self.editSpace.graphview.scene.addHasBeenModifiedListener(self.changeTitle)
        # self.setCentralWidget(self.editSpace)

        ########## making connections to slots ################
        self.editSpace.graphview.catClicked.connect(self.categoryClicked) # connecting signal from EditorWidget to slot
        # self.editSpace.childClicked.connect(self.addChildClicked) # connecting signal from EditorWidget


        # status bar
        self.statusBar().showMessage("")
        self.status_mouse_pos = QLabel("")
        self.statusBar().addPermanentWidget(self.status_mouse_pos)
        # nodeeditor.view.scenePosChanged.connect(self.onScenePosChanged)

        # set window properties
        self.setWindowTitle("Program-R AIML Editor")
        self.showMaximized()

    # slot function for a category being created and displaying on editSpace
    @pyqtSlot(Tag)
    def categoryCreated(self, cat):
        if DEBUG: print("slot in EditorWindow - categoryCreated()")
        if DEBUG: print(str(cat))
        # emitting signal to send category received from docker to EditorWidget slot
        self.catCreated.emit(cat) 

    # @pyqtSlot(str)
    # def addChildClicked(self, thatStr):
    #     if DEBUG: print("In slot in Editor Window - addChildClicked()")
    #     self.childClicked.emit(thatStr) # Emitting signal to Docker Widget

    @pyqtSlot(Tag)
    def categoryClicked(self, cat):
        if DEBUG: print("slot in EditorWindow - categoryClicked()")
        self.catClicked.emit(cat) # emitting signal to send category to docker to repopulate fields

    def changeTitle(self):
        title = "Node Editor - "
        if self.filename is None:
            title += "New"
        else:
            title += os.path.basename(self.filename)

        if self.centralWidget().scene.has_been_modified:
            title += "*"

        self.setWindowTitle(title)

    def closeEvent(self, event):
        if DEBUG: print("closeEvent")
        # if self.maybeSave():
        #     event.accept()
        # else:
        #     event.ignore()

    def isModified(self):
        return self.centralWidget().scene.has_been_modified

    def maybeSave(self):
        if not self.isModified():
            return True

        res = QMessageBox.warning(self, "About to loose your work?",
                "The document has been modified.\n Do you want to save your changes?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
              )

        if res == QMessageBox.Save:
            return self.onFileSave()
        elif res == QMessageBox.Cancel:
            return False

        return True

    def onScenePosChanged(self, x, y):
        self.status_mouse_pos.setText("Scene Pos: [%d, %d]" % (x, y))

    def onFind(self):
        if DEBUG: print("Find command called")
        finder = Find(self.editSpace.editSpace)
        finder.show()

    def onFileNew(self):
        self.editSpace.aiml = AIML()
        self.editSpace.clear()
        # if self.maybeSave():
        #     self.centralWidget().scene.clear()
        #     self.filename = None
        #     self.changeTitle()

    def onFileOpen(self):
        try:
            if self.maybeSave():
                fname, filter = QFileDialog.getOpenFileName(self, 'Open graph from file')
                if fname == '':
                    return
                if os.path.isfile(fname):
                    if DEBUG: print("found file")
                    self.filename = os.path.splitext(fname)[0]  # removing extension from path name
                    self.editSpace.graphview.scene.loadFromFile(self.filename)
                    for node in self.editSpace.graphview.scene.nodes:
                        self.editSpace.aiml.append(node.category)
                        node.content.catClicked.connect(self.editSpace.categoryClicked)
                    if DEBUG: print("Opened file successfully")
        except Exception as ex:
            handleError(ex)
            print("Exception caught in onFileOpen!")
            print(ex)

    def onFileSave(self):
        try:
            if self.filename is None: return self.onFileSaveAs()
            self.editSpace.graphview.scene.saveToFile(self.filename)
            # Storage.save(self.filename, self.editSpace.aiml)  # save as a pickle file
            self.statusBar().showMessage("Successfully saved %s" % self.filename)
            return True
        except Exception as ex:
            print("Exception caught trying to save to file")
            print(ex)
            handleError(ex)

    def onFileExport(self):
        # Check for uncompiled changes
        retval = None
        if self.editSpace.up_to_date is False:
            if DEBUG: print("Code is not compiled. Compile before export.")
            retval = handleCompileMsg()

        if retval == QMessageBox.Cancel:
            return
        
        if retval == QMessageBox.Yes:
            if DEBUG: print('Compiling code before exporting')
            try:
                self.onCompile()
            except Exception as ex:
                print('Couldn\'t compile before exporting')
                return
        try:
            fname, filter = QFileDialog.getSaveFileName(self, 'Export to file')
            if fname == "":
                if DEBUG: print("Cancel clicked")
                return
            Storage.exportAIML(fname, self.editSpace.editSpace.aiml) # save as an aiml file
        except Exception as ex:
            print("Exception caught trying to export")
            print(ex)
            handleError(ex)

    def onFileImport(self):
        try:
            fname, filter = QFileDialog.getOpenFileName(self, "Import File")

            if fname == "":
                if DEBUG: print("Cancel was clicked")
                return
                
            yoffset = -4000
            if DEBUG: print("fname: " + fname)
            self.filename = os.path.splitext(fname)[0]  # removing extension from path name
            aiml = Storage.importAIML(self.filename) # import the aiml file
            numCats = 0
            if DEBUG: print(f"aiml tags:\n{aiml.tags}")
            for cat in aiml.tags:
                self.catCreated.emit(cat)
                numCats = numCats + 1
            if DEBUG: print("Finished creating " + str(numCats) + " categories")

            # for node in self.editSpace.graphview.scene.nodes:
            #     x = node.grNode.x()
            #     node.setPos(x, yoffset)
            #     yoffset = yoffset + 500
            print("file import successful")
            self.onCompile()
            print("Compile after import sucessful!")
        except Exception as ex:
            handleError(ex)
            print(ex)

    def onFileSaveAs(self):
        fname, filter = QFileDialog.getSaveFileName(self, 'Save graph to file')
        if fname == '':
            return False
        self.filename = fname
        # Storage.save(self.filename, self.editSpace.scene)  # save as a pickle file
        self.onFileSave()
        return True

    def onEditUndo(self):
        self.centralWidget().scene.history.undo()

    def onEditRedo(self):
        self.centralWidget().scene.history.redo()

    def onEditDelete(self):
        self.centralWidget().scene.grScene.views()[0].deleteSelected()

    def onEditAdd(self):
        widget = self.centralWidget()
        assert isinstance(widget, EditorWidget)
        widget.addNode("new", [0], [0], 0, 0)

    def onEditCut(self):
        data = self.centralWidget().scene.clipboard.serializeSelected(delete=True)
        str_data = json.dumps(data, indent=4)
        QApplication.instance().clipboard().setText(str_data)

    def onEditCopy(self):
        data = self.centralWidget().scene.clipboard.serializeSelected(delete=False)
        str_data = json.dumps(data, indent=4)
        QApplication.instance().clipboard().setText(str_data)

    def onEditPaste(self):
        raw_data = QApplication.instance().clipboard().text()

        try:
            data = json.loads(raw_data)
        except ValueError as e:
            print("Pasting of not valid json data!", e)
            return

        # check if the json data is correct
        if 'nodes' not in data:
            if DEBUG: print("JSON does not contain any nodes!")
            return

        self.centralWidget().scene.clipboard.deserializeFromClipboard(data)

    def onCompile(self):
        if DEBUG: print("Compile Pressed!!!")
        str_to_parse = self.editSpace.editSpace.toPlainText() # Grabs text from the text display
        if DEBUG: print("text to compile:\n{}".format(str_to_parse))
        if str_to_parse.isspace():
            handleError("There is nothing to compile. You must at least have one tag pair to successfully compile your work.")
            return
        try:
            aiml = Storage.compileToAIML(str_to_parse)
            if aiml == -1:
                if DEBUG: print("did not compile properly")
                return
            if DEBUG: print("compiling complete")

            # Updating code editor
            self.editSpace.aiml = aiml
            if DEBUG: print(f"new model for the aiml:\n{self.editSpace.aiml}")

            # Updating graph view.
            # FIXME: This is code makes it so when updating in graph view, 
            #       changes will not be made in code editor.
            # FIXME: Also causing system to crash if you move nodes then try to compile.
            self.editSpace.graphview.scene.clearAllNodes()
            self.editSpace.graphview.scene.clearAllEdges()
            for cat in self.editSpace.aiml.tags:
                self.editSpace.create_category_graph_view(cat) # Sending categories to be drawn on graph view

            if DEBUG: print("finished redrawing nodes")

            self.editSpace.up_to_date = True
            if DEBUG: print("set up_to_date to True")
            self.editSpace.tabs.setStyleSheet('')
            if DEBUG: print("set style sheet for tabs.")
        except Exception as ex:
            print("Exception caught trying to compile project")
            print(ex)
            handleError(ex)
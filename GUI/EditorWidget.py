from PyQt5.QtWidgets import QWidget, QTextEdit, QGraphicsItem,\
    QApplication, QVBoxLayout, QPushButton, QBoxLayout, QMainWindow
from PyQt5.QtGui import QBrush, QPen, QFont, QColor
from PyQt5.QtCore import QFile, Qt, pyqtSlot, pyqtSignal
from Utils.ErrorMessage import *
from Model.Data import *
from GUI.QLabel_Clickable import *
from GUI.ResponseSelection import *
from GUI.Node.Node import Node
from GUI.Node.Scene.Scene import Scene
from GUI.Node.Edge import Edge, EDGE_TYPE_BEZIER
from GUI.Node.QDM.GraphicsView import QDMGraphicsView
from GUI.Node.QDM.GraphicsNode import *
from GUI.Node.Utils.Socket import *

DEBUG = True


class EditorWidget(QWidget):

    # Adding signal
    catCreated = pyqtSignal(Tag)
    catClicked = pyqtSignal(Tag)
    childClicked = pyqtSignal(str)

    def __init__(self, window, parent=None):
        try:
            super().__init__(parent)

            self.stylesheet_filename = 'GUI/style/nodestyle.qss'
            self.loadStylesheet(self.stylesheet_filename)
            self.responseTable = None

            self.initUI(window)
        except Exception as ex:
            print("Exception caught in EditorWidget - __init__()")
            print(ex)
            handleError(ex)

    def initUI(self, window):
        try:
            self.layout = QBoxLayout(QBoxLayout.LeftToRight)
            self.layout.setContentsMargins(0, 0, 0, 0)
            self.setLayout(self.layout)

            # crate graphics scene
            self.scene = Scene()
            self.grScene = self.scene.grScene

            # create graphics view
            self.view = QDMGraphicsView(self.scene.grScene, self)
            self.layout.addWidget(self.view)
        except Exception as ex:
            print("Exception caught in EditorWidget - initUI()")
            print(ex)
            handleError(ex)


    
    # HACK: The function below was used for testing placement of nodes.
    #       Not needed for the program, might be helpful for debugging.
    # def addNodes(self):
    #     node1 = Node(self.scene, "My Awesome Node 1",
    #                  inputs=[0, 0, 0], outputs=[1])
    #     node2 = Node(self.scene, "My Awesome Node 2",
    #                  inputs=[3, 3, 3], outputs=[1])
    #     node3 = Node(self.scene, "My Awesome Node 3",
    #                  inputs=[2, 2, 2], outputs=[1])
    #     node4 = Node(self.scene, "A Category", inputs=[1, 1], outputs=[2, 2], )
    #     node1.setPos(-350, -250)
    #     node2.setPos(-75, 0)
    #     node3.setPos(200, -150)
    #     node4.setPos(200, -50)

    #     edge1 = Edge(
    #         self.scene, node1.outputs[0], node2.inputs[0], edge_type=EDGE_TYPE_BEZIER)
    #     edge2 = Edge(
    #         self.scene, node2.outputs[0], node3.inputs[0], edge_type=EDGE_TYPE_BEZIER)

    def addNode(self, title, inputs, outputs, posx, posy):
        try:
            node1 = Node(self.scene, title=title, inputs=inputs, outputs=outputs)
            node1.setPos(posx, posy)
        except Exception as ex:
            print("Exception caught in EditorWidget - addNode()")
            print(ex)
            handleError(ex)

    def updateNode(self, cat):
        try:
            if DEBUG: print("updating node in display")
            for node in self.scene.nodes:
                if node.category.cat_id == cat.cat_id:
                    if DEBUG: print("found node to update")
                    node.category = cat
                    if DEBUG: print(str(node.category))
                    
                    # Displaying updated content on node.
                    node.content.wdg_label.clear()
                    node.content.wdg_label.displayVisuals(cat)
        except Exception as ex:
            print("EXCEPTION CAUGHT! In EditorWidget - updateNode()")
            print(ex)
            handleError(ex)


    def addDebugContent(self):
        try:
            greenBrush = QBrush(Qt.green)
            outlinePen = QPen(Qt.black)
            outlinePen.setWidth(2)

            rect = self.grScene.addRect(-100, -100, 80,
                                        100, outlinePen, greenBrush)
            rect.setFlag(QGraphicsItem.ItemIsMovable)

            text = self.grScene.addText(
                "This is my Awesome text!", QFont("Ubuntu"))
            text.setFlag(QGraphicsItem.ItemIsSelectable)
            text.setFlag(QGraphicsItem.ItemIsMovable)
            text.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 1.0))

            widget1 = QPushButton("Hello World")
            proxy1 = self.grScene.addWidget(widget1)
            proxy1.setFlag(QGraphicsItem.ItemIsMovable)
            proxy1.setPos(0, 30)

            widget2 = QTextEdit()
            proxy2 = self.grScene.addWidget(widget2)
            proxy2.setFlag(QGraphicsItem.ItemIsSelectable)
            proxy2.setPos(0, 60)

            line = self.grScene.addLine(-200, -200, 400, -100, outlinePen)
            line.setFlag(QGraphicsItem.ItemIsMovable)
            line.setFlag(QGraphicsItem.ItemIsSelectable)
        except Exception as ex:
            print("Exception caught in EditorWidget - addDebugContent()")
            print(ex)
            handleError(ex)

    def loadStylesheet(self, filename):
        try:
            if DEBUG: print('STYLE loading:', filename)
            file = QFile(filename)
            file.open(QFile.ReadOnly | QFile.Text)
            stylesheet = file.readAll()
            QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))
        except Exception as ex:
            print("Exception caught in EditorWidget - loadStylesheet()")
            print(ex)
            handleError(ex)


    """
    Determine if the condition or random table has text afterwards.
    """
    def tableContainsTail(self, template):
        try:
            for tag in reversed(template.tags):
                if DEBUG: print("Beginning of loop")
                if DEBUG: print(f"Current tag: {tag}")

                if isinstance(tag, str) is True:
                    if DEBUG: print("String found before Condition or Random. Return True.")
                    return True, tag
                # Check for <oob> tag
                elif tag.type == "oob":
                    if DEBUG: print("oob found, keep searching.")
                elif tag.type == "condition" or tag.type == "random":
                    if DEBUG: print("Condition or Random found before String. Return False.")
                    return False, None
            # Made it to end without finding anything
            if DEBUG: print("Made it to end without finding anything. This should not happen!")
            return False, None
        except Exception as ex:
            print("Exception caught in EditorWidget - tableContainsTail_better()")
            print(ex)
            handleError(ex)


    """
    Function to find the sentence to be used for <that> tag of potential children.
    Returns a list of strings of last sentences in the <template> tag.
        Sentences will only contain more than 1 element if there is a <random> or
        <condition> tag. Sentences will then have a string for each <li> tag.
    """
    def getLastSentence(self, cat):
        if DEBUG: print("In getLastSentence()")
        try:
            template = cat.findTag("template")
            sentences = []
            if template is None:
                if DEBUG: print("Template is empty")
                return None
            condition = template.findTag("condition")
            random = template.findTag("random")
            if DEBUG: print("Before logic")
            if condition is None and random is None:
                if DEBUG: print("no random or condition tag found in template")
                if DEBUG: print(str(template))
                tempString = template.findTag("text")
                if DEBUG: print(f"tempString: {tempString}")
                if tempString is None:
                    if DEBUG: print("No sentence in category")
                    return None
                tempArr = tempString.split()
                index = 0
                for word in reversed(tempArr):
                    if "." in word or "?" in word or "!" in word:
                        if index == 0:
                            if DEBUG: print("Found last punctuation mark on very first word. Keep searching.")
                            if DEBUG: print(word)
                        else:
                            if DEBUG: print("Found the start of the last sentence")
                            if DEBUG: print(word)
                            arrSize = len(tempArr)
                            start = arrSize - (index)
                            lastSentence = tempArr[start:arrSize]
                            lastSentence = " ".join(lastSentence)
                            if DEBUG: print(f"appending: {lastSentence}")
                            sentences.append(lastSentence)
                    index = index + 1

                # If made it to end of array without finding another punctiation mark. return full text in template
                if len(sentences) is 0:
                    if DEBUG: print(f"appending: {tempString}")
                    sentences.append(tempString)
                return sentences
            else:
                if DEBUG: print("template contains either a random or condition tag")
                if DEBUG: print(str(template))
                contains_tail, tail = self.tableContainsTail(template)
                if contains_tail is True:
                    sentences.append(tail)
                    return sentences
                else:
                    if DEBUG: print("Random or Condition tag is the last thing in the template")
                    if condition is not None:
                        if DEBUG: print("table contains condition table")
                        for li in condition.tags:
                            liText = li.findTag("text")
                            if DEBUG: print("text inside condition: " + liText)
                            liArr = liText.split()
                            index = 0
                            punctuationExists = False
                            for word in reversed(liArr):
                                if "." in word or "?" in word or "!" in word:
                                    if index == 0:
                                        if DEBUG:print("Found last punctuation mark on very first word. Keep searching.")
                                        if DEBUG: print(word)
                                    else:
                                        if DEBUG: print("Found the start of the last sentence")
                                        if DEBUG: print(word)
                                        arrSize = len(liArr)
                                        start = arrSize - (index)
                                        lastSentence = liArr[start:arrSize]
                                        lastSentence = " ".join(lastSentence)
                                        if DEBUG: print(f"appending: {lastSentence}")
                                        sentences.append(lastSentence)
                                        punctuationExists = True
                                        break
                                index = index + 1
                            # If made it to end of array without finding another punctiation mark. return full text in tag
                            if punctuationExists is False:
                                sentences.append(liText)
                        return sentences
                        if DEBUG: print("done goofed")
                    else:
                        if DEBUG: print("table contains random table")
                        for li in random.tags:
                            liText = li.findTag("text")
                            if DEBUG: print("text inside random: " + liText)
                            liArr = liText.split()
                            index = 0
                            punctuationExists = False
                            for word in reversed(liArr):
                                if "." in word or "?" in word or "!" in word:
                                    if index == 0:
                                        if DEBUG: print("Found last punctuation mark on very first word. Keep searching.")
                                        if DEBUG: print(word)
                                    else:
                                        if DEBUG: print("Found the start of the last sentence")
                                        if DEBUG: print(word)
                                        arrSize = len(liArr)
                                        start = arrSize - (index)
                                        lastSentence = liArr[start:arrSize]
                                        lastSentence = " ".join(lastSentence)
                                        if DEBUG: print(f"appending: {lastSentence}")
                                        sentences.append(lastSentence)
                                        punctuationExists = True
                                        break
                                index = index + 1
                            # If at the end of array without finding another punctiation mark. return full text in tag
                            if punctuationExists is False:
                                if DEBUG: print(f"appending: {liText}")
                                sentences.append(liText)
                        return sentences
                    if DEBUG: print("done goofed")
        except Exception as ex:
            print("Exception caught in EditorWidget - getLastSentence()")
            print(ex)
            handleError(ex)

    """
    Find child nodes in the scene and add edges based off of <that> tags
    """
    def findChildNodes(self, newnode, thatStr):
        try:
            if DEBUG: print("looking for child nodes")
            xOffset = 0
            for node in self.scene.nodes:
                thatTag = node.category.findTag("that")
                if DEBUG: print(f"Current Category:\n{node.category}")
                if DEBUG: print(f"that: {str(thatTag)}")
                if newnode == node:
                    if DEBUG: print("looking at node just created. Do nothing")
                elif thatTag is None:
                    if DEBUG: print("no that tag found in category: " + str(node.category))
                else:
                    # That tag was found, add an edge
                    if DEBUG: print("that tag was found in category: " + str(node.category))
                    thatText = thatTag.findTag("text")
                    if DEBUG: print(f"Return type of findTag(\"text\"): {type(thatText)}")
                    if DEBUG: print(f"{thatText}")
                    if DEBUG: print(f"Data type of parameter thatStr: {type(thatStr)}")
                    if DEBUG: print(f"{thatStr}")
                    if thatText.lower() == thatStr.lower():
                        if DEBUG: print("FOUND CHILD!")
                        self.updateChildSockets(newnode, node)
                    else:
                        if DEBUG: print("Not a match for a child")

            if DEBUG: print("No child found in scene")
        except Exception as ex:
            print("Exception caught in EditorWidget when looking for child nodes")
            print(ex)
            handleError(ex)


    """
    Find parent nodes in the scene and add edges based off of <that> tags.
    """
    def findParentNodes(self, newnode):
        try:
            if DEBUG: print("looking for parent nodes")
            mythatTag = newnode.category.findTag("that")
            if mythatTag is None:
                if DEBUG: print("no that tag so node will not have any parents")
                return
            thatText = mythatTag.findTag("text")
            if DEBUG: print("Text of That Tag to look for: " + thatText)
            xOffset = 0
            for node in self.scene.nodes:
                if node == newnode:
                    if DEBUG: print("looking at node just created, do nothing")
                else:
                    if DEBUG: print("looking at node with category: " + str(node.category))
                    self.updateParentSockets(newnode, node, thatText)
        except Exception as ex:
            print("Exception caught in EditorWidget - findParentNodes()")
            print(ex)
            handleError(ex)

    
    """
    Function to update the edges connecting to child nodes.
    """
    def updateChildSockets(self, newnode, node):
        try:
            parentsocket = Socket(newnode, position=RIGHT_BOTTOM, socket_type=2)
            newnode.inputs.append(parentsocket) # outputs is children

            if node not in newnode.children:
                newnode.children.append(node)

            childsocket = Socket(node)
            node.outputs.append(childsocket)

            if newnode not in node.parents:
                node.parents.append(newnode)

            edge = Edge(self.scene, parentsocket, childsocket)
            
            return edge
        except Exception as ex:
            print("Exception caught in EditorWidget - updateChildSockets()")
            print(ex)
            handleError(ex)


    """
    Function to update the edges connecting to parent nodes.
    """
    def updateParentSockets(self, newnode, node, thatText):
        try:
            templateText = self.getLastSentence(node.category)
            for text in templateText:
                if thatText.lower() == text.lower():
                    if DEBUG: print("Found parent node!")
                    parentsocket = Socket(node, position=RIGHT_BOTTOM, socket_type=2)
                    node.inputs.append(parentsocket)

                    # need to check if node exists in list before appending
                    if newnode not in node.children:
                        node.children.append(newnode)

                    childsocket = Socket(newnode)
                    newnode.outputs.append(childsocket)

                    if node not in newnode.parents:
                        newnode.parents.append(node)

                    edge = Edge(self.scene, parentsocket, childsocket)
                else:
                    if DEBUG: print("Not a match for a parent")
        except Exception as ex:
            print("Exception caught in EditorWidget - updateParentSockets()")
            print(ex)
            handleError(ex)
  

    """
    Function to organize nodes based on parents and children
    """
    def placeNodes(self, nodes, depth=0, yOffset=0):
        # TODO: Recursively look through children. place parents on left, children on the right.
        try:
            if DEBUG: print("placing nodes")
            if depth > 5:
                if DEBUG: print("reached max depth")
                return

            xOffset = 500
            
            for node in nodes:
                if len(node.parents) is 0:
                    if DEBUG: print("node has no parents place to the left.")
                    if DEBUG: print(f"Placing category:\n{node.category}")
                    node.setPos(-900, -900 + yOffset)
                    yOffset += 575
                else:
                    if DEBUG: print("node has parents")
                    yOffset = 0
                    for child in node.children:
                        depth = depth + 1
                        y = node.grNode.y()
                        child.setPos(xOffset, y + yOffset)
                        xOffset += 200
                        yOffset += 575
                        if DEBUG: print(f"Placing category:\n{node.category}")
                        self.placeNodes(child.children, depth, yOffset)
                    node.setPos(xOffset, yOffset)
                    xOffset += 300
        except Exception as ex:
            print("Exception caught placing nodes!")
            print(ex)
            handleError(ex)

    # @pyqtSlot(Tag)
    # def addChildClicked(self, cat):
    #     try:
    #         if DEBUG: print("In slot of editor widget")
    #         template = cat.findTag("template")
    #         if DEBUG: print("template tags list: " + str(template.tags))
    #         if template.findTag("condition") is None and template.findTag("random") is None:
    #             if DEBUG: print("no table inside template")
    #             thatStr = self.getLastSentence(cat)
    #             if DEBUG: print(thatStr)
    #             self.childClicked.emit(thatStr[0])  # emitting to Editor Window
    #         else:
    #             if self.tableContainsTail(template) is False:
    #                 if DEBUG: print("table is last thing in template. Must choose response to use for that")
    #                 template = cat.findTag("template")
    #                 condition = template.findTag("condition")
    #                 random = template.findTag("random")
    #                 if condition is not None:
    #                     if DEBUG: print("create response table out of condition items")
    #                     self.responseTable = ResponseSelection(tag=condition, category=cat, editspace=self)
    #                 else:
    #                     if DEBUG: print("create response table out of random items")
    #                     self.responseTable = ResponseSelection(tag=random, category=cat, editspace=self)
    #             else:
    #                 if DEBUG: print("table contains tail, there is only one possible sentence to use for that")
    #                 thatStr = self.getLastSentence(cat)
    #                 if DEBUG: print(thatStr[0])
    #                 self.childClicked.emit(thatStr[0]) # emitting to Editor Window
    #     except Exception as ex:
    #         print(ex)
    #         handleError(ex)

    def setNodeStyleSheet(self, node):
        node.content.setStyleSheet(self.stylesheet_filename)
        return node

    @pyqtSlot(Tag)
    def categoryClicked(self, cat):
        if DEBUG: print("slot in EditorWidget - categoryClicked()")
        
        # Resetting all nodes to original style sheet
        self.scene.nodes = list(map(self.setNodeStyleSheet, self.scene.nodes))
        
        try:
            # FIXME: Optimize by maybe place parent and children nodes in something other than lists.
            for node in self.scene.nodes:
                if DEBUG: print("Searching for correct node")
                if node.category.cat_id == cat.cat_id:
                    node.content.setStyleSheet("QDMNodeContentWidget { background: #ffff1a; }")
                    for child in node.children:
                        if DEBUG: print("Changing background of child")
                        child.content.setStyleSheet("QDMNodeContentWidget { background: #f82f04; }")

                    for parent in node.parents:
                        if DEBUG: print("Changing background of parent")
                        parent.content.setStyleSheet("QDMNodeContentWidget { background: #0cfdd8; }")
            
            self.catClicked.emit(cat) # emitting signal to be sent to EditorWindow
        except Exception as ex:
            print("Exception caught when category is clicked.")
            print(ex)
            handleError(ex)
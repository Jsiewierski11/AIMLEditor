import json
from collections import OrderedDict
from GUI.Node.Utils.Serializable import Serializable
from GUI.Node.QDM.GraphicsScene import QDMGraphicsScene
from GUI.Node.Node import Node
from GUI.Node.Edge import Edge
from GUI.Node.Scene.SceneHistory import SceneHistory
from GUI.Node.Scene.SceneClipboard import SceneClipboard
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from Model.Data import *
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QFont

DEBUG = True

class Scene(Serializable):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.edges = []

        self.scene_width = 64000
        self.scene_height = 64000

        self._has_been_modified = False
        self._has_been_modified_listeners = []

        if DEBUG: print("Initializing UI")
        self.initUI()
        if DEBUG: print("UI Initialized")
        self.history = SceneHistory(self)
        self.clipboard = SceneClipboard(self)

    @property
    def has_been_modified(self):
        return self._has_been_modified

    @has_been_modified.setter
    def has_been_modified(self, value):
        if not self._has_been_modified and value:
            self._has_been_modified = value

            # call all registered listeners
            for callback in self._has_been_modified_listeners:
                callback()

        self._has_been_modified = value

    def addHasBeenModifiedListener(self, callback):
        self._has_been_modified_listeners.append(callback)

    def initUI(self):
        self.grScene = QDMGraphicsScene(self)
        if DEBUG: print("Created graphics scene")
        self.grScene.setGrScene(self.scene_width, self.scene_height)
        if DEBUG: print("Set scene dimensions")

    def addNode(self, node):
        self.nodes.append(node)

    def addEdge(self, edge):
        self.edges.append(edge)

    def removeNode(self, node):
        self.nodes.remove(node)

    def removeEdge(self, edge):
        self.edges.remove(edge)

    def clearAllEdges(self):
        for edge in self.edges:
            # edge.start_socket = []
            # edge.end_socket = []
            # self.removeEdge(edge)
            edge.remove()

    def clear(self):
        while len(self.nodes) > 0:
            self.nodes[0].remove()

        self.has_been_modified = False

    def saveToFile(self, filename):
        with open(filename+'.aib', "w") as file:
            file.write( json.dumps( self.serialize(), indent=4 ) )
            if DEBUG: print("saving to ", filename, " was successful.")

            self.has_been_modified = False

    def loadFromFile(self, filename):
        with open(filename+'.aib', "r") as file:
            raw_data = file.read()
            data = json.loads(raw_data, encoding='utf-8')
            self.deserialize(data)
            
            self.has_been_modified = False

    def serialize(self):
        if DEBUG: print("Serializing Scene")
        nodes, edges = [], []
        for node in self.nodes: nodes.append(node.serialize())
        for edge in self.edges: edges.append(edge.serialize())
        return OrderedDict([
            ('id', self.objId),
            ('scene_width', self.scene_width),
            ('scene_height', self.scene_height),
            ('nodes', nodes),
            ('edges', edges),
        ])

    def deserialize(self, data, hashmap={}, restore_id=True):
        if DEBUG: print("Deserializing scene")
        self.clear()
        hashmap = {}

        if restore_id: self.objId = data['id']

        # create nodes
        for node_data in data['nodes']:
            Node(self).deserialize(node_data, hashmap, restore_id)

        # create edges
        for edge_data in data['edges']:
            Edge(self).deserialize(edge_data, hashmap, restore_id)

        return True

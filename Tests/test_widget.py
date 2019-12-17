import os, sys

sys.path.append(os.path.abspath('..'))
from Model.Data import *
from Utils.ErrorMessage import *
from GUI import EditorWidget
from GUI.Node.Utils.Socket import *
from GUI.Node.Scene.Scene import Scene
from GUI.Node.Node import Node

DEBUG = True

class TestEditorWidget(object):
    def __init__(self):
        # if DEBUG: print("creating scene")
        # self.scene = Scene()
        # if DEBUG: print("scene created")
        pass

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
                if sentences is None:
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
                if DEBUG: print(str(thatTag))
                if thatTag is None:
                    if DEBUG: print("no that tag found in category: " + str(node.category))
                elif newnode == node:
                    if DEBUG: print("looking at node just created. Do nothing")
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
            print("Exception caught in test_widget - findParentNodes()")
            print(ex)
            handleError(ex)


    """
    Function to update the edges connecting to child nodes.
    """
    def updateChildSockets(self, newnode, node):
        parentsocket = Socket(newnode, position=RIGHT_BOTTOM, socket_type=2)
        newnode.inputs.append(parentsocket) # outputs is children

        if node not in newnode.children:
            newnode.children.append(node)

        childsocket = Socket(node)
        node.outputs.append(childsocket)

        if newnode not in node.parents:
            node.parents.append(newnode)

        edge = Edge(self.scene, parentsocket, childsocket)


    """
    Function to update the edges connecting to parent nodes.
    """
    def updateParentSockets(self, newnode, node, thatText):
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
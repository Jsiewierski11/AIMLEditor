from Model.Data import *
from Utils.ErrorMessage import *

DEBUG = True

class EditorWidget(object):
    def __init__(self):
        pass

    """
    Determine if the condition or random table has text afterwards
    """
    def tableContainsTail(self, template):
        try:
            index = 0
            for tag in template.tags:
                if DEBUG: print("Beginning of for loop")
                if isinstance(tag, str) is True and tag is not " ":
                    if DEBUG: print("found string")
                    continue
                elif tag.type == "condition" or tag.type == "random":
                    # Check to see if we are at end of array
                    if index == len(template.tags) - 1:
                        return False

                    if DEBUG: print("next item in tags list: " + str(template.tags[index+1]))
                    if isinstance(template.tags[index+1], str) is True:
                        print("returning true")
                        return True
                    else:
                        if DEBUG: print("returning false")
                        return False
                index = index + 1
        except Exception as ex:
            print("Exception caught in EditorWidget - tableContainsTail()")
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
                if self.tableContainsTail(template) is True:
                    if DEBUG: print("Random or Condition tag has text after")
                    tempString = template.findTag("text", 1)
                    if DEBUG: print(tempString)
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
                    sentences.append(tempString)
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
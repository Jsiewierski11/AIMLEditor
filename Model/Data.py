from textwrap import indent
from Tree.CommentedTreeBuilder import *
import Model.Formatting as Formatting
from PyQt5.QtCore import QUuid
from GUI.Node.Utils.Serializable import Serializable
from collections import OrderedDict




class Tag(Serializable):
    def __init__(self, type, single=False, acceptable_tags=[], attrib={}):
        super().__init__()
        self.type = type
        self.single = single
        self.tags = []
        self.acceptable_tags = acceptable_tags
        self.attrib = attrib

        self.tag_list = {"aiml": AIML,
            "topic": Topic,
            "category": Category,
            "pattern": Pattern,
            "template": Template,
            "condition": Condition,
            "li": ConditionItem,
            "random": Random,
            "set": Set,
            "think": Think,
            "that": That,
            "oob": Oob,
            "robot": Robot,
            "options": Options,
            "option": Option,
            "image": Image,
            "video": Video,
            "filename": Filename,
            "srai": Srai,
            "bot": Bot,
            "star": Star,
            "comment": Comment}

    def decode_tag(self, tag_type):
        if tag_type in tag_list:
            return tag_list[tag_type]()
        return False

    def serialize(self):
        try:
            print("attempting to serialize tag")
            tags = []
            for tag in self.tags:
                try:
                    tags.append(tag.serialize())
                except:
                    tags.append(str(tag))

            print("created tags array")

            print(tags)

            print(self.attrib)
            return OrderedDict([
                ('id', self.objId),
                ('type', str(self.type)),
                ('tags', tags),
                ('attrib', self.attrib)
            ])
        except Exception as ex:
            print("Exception caught in serializing tag!")
            print(ex)

    def deserialize(self, data, hashmap={}, restore_id=True):
        try:
            print("attempting to deserialize tag")
            if restore_id: self.objId = data['id']

            self.type = data['type']
            self.attrib = data['attrib']

            print("about to recursively decode tags")

            for tag in data['tags']:
                print("printing tag contents")
                print(tag)
                try:
                    aTag = self.decode_tag(tag['type'])
                    print(aTag)
                    self.tags.append(aTag)
                    aTag.deserialize(tag)
                except:
                    print("appending text between tags")
                    self.tags.append(tag)
            return True
        except Exception as ex:
            print("Exception caught in deserialize Tag!")
            print(ex)

    def append(self, tag):
        if type(tag) in self.acceptable_tags:
            self.tags.append(tag)
            return self
        raise Exception("Type: " + str(type(tag)) +
                        " not allowed in " + self.type)

    def setAttrib(self, attrib):
        self.attrib = attrib

    def find(self, id):
        print("trying to find category with id of " + str(id))
        if id is None:
            print("Bad id, id was never generated and is currently null")
            return None

        for cat in self.tags:
            if cat.type == "category":
                if cat.id == id:
                    return cat
            else:
                print("tag type: " + cat.type)

        print("No category found")
        return None

    def update(self, newCat):
        print("UPDATING CATEGORY")
        if id is None:
            print("Bad id, id was never generated and is currently null")
            return None

        for index, cat in enumerate(self.tags):
            if cat.type == "category":
                if cat.id == newCat.id:
                    print("category to be removed: " + str(cat))
                    self.tags.remove(cat)
                    self.tags.append(newCat)
            elif cat.type == "topic":
                print("topic tag")
                for ind, tag in enumerate(cat.tags):
                    if tag.id == newCat.id:
                        print("category to be removed: " + str(tag))
                        cat.tags.remove(tag)
                cat.tags.append(tag)
            else:
                print("tag type: " + cat.type)

        return newCat

    """
    Finds nth occurrence (if no parameter given for n then finds the first occurence) of Tag, type, in array tags of Parent Tag.
    If wanting to find the text that the tag contains pass through text as the type.
    """
    def findTag(self, tagType, n=1):
        try:
            if self.tags is None:
                print("This tag has no child tags")
                return None
            occurrence = 1
            for child in self.tags:
                print(f"current Child in findTag:\n{child} ")
                print(f"data type of child: {type(child)}")
                if tagType == "text":
                    if isinstance(child, str) is True:
                        if n == occurrence:
                            return child
                        else:
                            occurrence = occurrence + 1
                else:
                    print("Inside else of findTag")
                    if isinstance(child, str) is True:
                        print("looking at string there is no type to check")
                    else:
                        if child.type == tagType:
                            if n == occurrence:
                                return child
                            else:
                                occurrence = occurrence + 1
            return None
        except Exception as ex:
            print("Exception caught in findTag!")
            print(ex)


    def __str__(self):
        attrib = (' ' + ' '.join('{}=\"{}\"'.format(
                key, val) for key, val in self.attrib.items())) if len(self.attrib) > 0 else ""

        if self.type == 'pattern' or self.type == 'srai' or \
           self.type == 'li' or self.type == "think" or \
           self.type == 'that' or self.type == "set" or \
           self.type == 'filename' or self.single == True:
            # NOTE: If tag is one of the types listed above, 
            #       keep everything on one line
            tags = "".join(map(str, self.tags))
        elif self.type == 'comment':
            # print("At comment tag")
            # print(f"self.tags:\n{self.tags}")
            if self.tags != []:
                temp_str = self.tags[0].replace("    ", "")
                tags = " ".join(temp_str.split(" "))
            else:
                tags = "".join(map(str, self.tags))
        elif len(self.tags) > 0:
            tags = self.map_to_string()
        else:
            tags = ""

        if self.type == 'comment':
            return "<!-- {} -->".format(tags)
        elif self.type == 'set' and self.attrib == {}:
            return " <{}{}>{}</{}> ".format(str(self.type), attrib, tags, str(self.type))
        elif self.single == True:
            if len(attrib) > 0:
                return "<{} {}/>".format(str(self.type), attrib)
            else:
                return "<{}/>".format(str(self.type))
        else:
            return "<{}{}>{}</{}>".format(str(self.type), attrib, tags, str(self.type))

    def map_to_string(self):
        tags = ''
        # print(f"In map_to_string, tag.type: {self.type}")
        for index, tag in enumerate(self.tags):
            if type(tag) is str:
                # print('in the str case')
                tags += '\n' + indent(tag, Formatting.indentation)
            else:
                if tag.type == "star":
                    tags += ''.join(str(tag))
                elif tag.type == "set" and tag.attrib == {}:
                    tags += ' ' + ''.join(str(tag)) + ' '
                elif tag.type == "pattern" or tag.type == "that" or \
                     tag.type == "li" or tag.type == "random" or tag.type == "comment":                   
                    # Checking to see if we are at end of list
                    # print("in the outer edge case")
                    # print(f"tag.type: {tag.type}")
                    if index < len(self.tags)-1:
                        # NOTE: If the next tag is one of the following listed 
                        #       then we need to add an \n char to the end of our string
                        if type(self.tags[index+1]) != str:
                            if self.tags[index+1].type != "li" and self.tags[index+1].type != "comment" and \
                            self.tags[index+1].type != "template" and self.tags[index+1].type != "oob" and \
                            self.tags[index+1].type != "category" and self.tags[index+1].type != "that":
                                # print("in the inner edge case")
                                # print(f"tag.type: {tag.type}")
                                tags += '\n' + indent(''.join(str(tag)),
                                        Formatting.indentation) + '\n'
                            else:
                                tags += '\n' + indent(''.join(str(tag)),
                                            Formatting.indentation)
                        else:
                                tags += '\n' + indent(''.join(str(tag)),
                                            Formatting.indentation)
                    else:
                        tags += '\n' + indent(''.join(str(tag)),
                                    Formatting.indentation)                        
                else:
                    tags += '\n' + indent(''.join(str(tag)),
                                Formatting.indentation) + '\n'
        return tags

    def getContents(self):
        attrib = (' ' + ' '.join('{}=\"{}\"'.format(
            key, val) for key, val in self.attrib.items())) if len(self.attrib) > 0 else ""
        if len(self.tags) > 1:
            tags = '\n' + indent('\n'.join(map(str, self.tags)),
                                 Formatting.indentation) + '\n'
            tags = tags.strip()
        elif len(self.tags) > 0:
            tags = '\n'.join(map(str, self.tags))
            tags = tags.strip()
        else:
            tags = ""
        return "{}".format(tags)


class AIML(Tag):
    def __init__(self, version="2.0"):
        super().__init__("aiml", acceptable_tags=[Category, Topic, Comment], attrib={'version': version})


class Comment(Tag):
    def __init__(self, version="2.0"):
        super().__init__("comment", acceptable_tags=[str, AIML, Category, Topic, Pattern, Template,  
                                                     That, Srai, Random, Condition, ConditionItem, Bot, 
                                                     Star, Set, Think, Oob, Robot, Option, Options, 
                                                     Video, Image, Filename])


class Topic(Tag):
    def __init__(self, name=""):
        if name != "":
            super().__init__("topic", acceptable_tags=[
                Category], attrib={'name': name})
        else:
            super().__init__("topic", acceptable_tags=[Category, Comment])


class Category(Tag):
    def __init__(self, id=""):
        super().__init__("category", acceptable_tags=[
            Pattern, Template, Think, That, Comment])
        # id to distinguish categories within an AIML object
        if id == "":
            newId = QUuid.createUuid()
            self.id = newId.toString()
        else:
            self.id = id


class Pattern(Tag):
    def __init__(self):
        super().__init__("pattern", acceptable_tags=[Set, Comment, str])


class Template(Tag):
    def __init__(self):
        super().__init__("template", acceptable_tags=[
            Set, Think, Condition, Oob, Random, Srai, Bot, Star, Comment, str])


class That(Tag):
    def __init__(self):
        super().__init__("that", acceptable_tags=[Comment, str])


class Srai(Tag):
    def __init__(self):
        super().__init__("srai", acceptable_tags=[Comment, str])


class Random(Tag):
    def __init__(self):
        super().__init__("random", acceptable_tags=[ConditionItem, Oob, Comment])


class Condition(Tag):
    def __init__(self, name=""):
        if name != "":
            super().__init__("condition", attrib={
                "name": name}, acceptable_tags={ConditionItem, Comment})
        else:
            super().__init__("condition", acceptable_tags={ConditionItem, Comment})


class ConditionItem(Tag):
    def __init__(self, value=""):
        if value != "":
            super().__init__("li", attrib={
                "value": value}, acceptable_tags=[Oob, Set, Srai, Bot, Comment, str])
        else:
            super().__init__("li", acceptable_tags=[Oob, Set, Srai, Bot, Comment, str])


class Bot(Tag):
    def __init__(self, name="", single=True):
        if name != "":
            super().__init__("bot", single=single, attrib={
                "name": name}, acceptable_tags=[])
        else:
            super().__init__("bot", single=single, acceptable_tags=[])


class Star(Tag):
    def __init__(self, single=True):
        super().__init__("star", single=single, attrib={}, acceptable_tags=[Comment])


class Set(Tag):
    def __init__(self, name=""):
        if name != "":
            super().__init__("set", attrib={
                'name': name}, acceptable_tags=[Star, Comment, str])
        else:
            super().__init__("set", acceptable_tags=[Star, Comment, str])


class Think(Tag):
    def __init__(self):
        super().__init__("think", acceptable_tags=[Set, Star, Comment, str])


class Oob(Tag):
    def __init__(self):
        super().__init__("oob", acceptable_tags=[Robot, Comment])


class Robot(Tag):
    def __init__(self):
        super().__init__("robot", acceptable_tags=[Options, Video, Image, Comment])


class Options(Tag):
    def __init__(self):
        super().__init__("options", acceptable_tags=[Option, Comment])


class Option(Tag):
    def __init__(self, value=""):
        if value != "":
            super().__init__("option", acceptable_tags=[Comment, str])
            super().append(value)
        else:
            super().__init__("option", acceptable_tags=[Comment, str])


class Video(Tag):
    def __init__(self):
        super().__init__("video", acceptable_tags=[Filename, Comment])


class Image(Tag):
    def __init__(self):
        super().__init__("image", acceptable_tags=[Filename, Comment])


class Filename(Tag):
    def __init__(self):
        super().__init__("filename", acceptable_tags=[Comment, str])
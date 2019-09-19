from Model.Data import *
import Utils.Storage as Storage

# TODO: Find a way to identify Comment tags when parsing the tree. 
#       What attribute do we need to use/make?

comment_handler = CommentedTreeBuilder()

parser = ET.XMLParser(target=comment_handler)

with open('test_aimls/utils.aiml', 'r') as f:
    tree = ET.parse(f, parser)

root = tree.getroot()
print(root.tag)

for child in root:
    print("child.tag: {}".format(child.tag))
    print("child.text: {}".format(child.text))
    print(type(child.text))
    print(ET.iselement(child))
    print("checking type: {}".format(type(child) == type.functionType))
    tag_obj = Storage.decode_tag(child.tag.lower())
    print(tag_obj)
    raise exception
# ET.dump(tree)
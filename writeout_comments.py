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
    text = ''.join(child.text.strip())
    print("child.text: {}".format(text))
    print(type(child.text))
    tag_obj = Storage.decode_tag(child.tag.lower())
    print(tag_obj)
    raise exception
# ET.dump(tree)
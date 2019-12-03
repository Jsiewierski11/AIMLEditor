import os, sys

sys.path.append(os.path.abspath('..'))
import Utils.Storage as Storage
from Model.Data import *


aiml = AIML()
category = Category()
pattern = Pattern()
template = Template()
random = Random()
comment = Comment()
li1 = ConditionItem()
li2 = ConditionItem()
li3 = ConditionItem()
li4 = ConditionItem()
oob = Oob()
robot = Robot()

aiml.append(category.append(
    pattern).append(template.append(random.append(
        li1).append(
        comment.append(li2.append('hi')).append(li3.append('hi')).append(li4.append('hi'))
        )
    ).append(oob.append(robot)))
)

Storage.exportAIML('test_multiline_comments', aiml)

print(aiml)
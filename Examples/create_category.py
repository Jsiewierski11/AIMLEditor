
import os,sys
sys.path.append(os.path.abspath('..'))
from Model.Data import *

# create the category object
cat = Category()

# print the category
print(cat)  # this should print: <Category></Category>

# create a pattern object
pattern = Pattern()

# add some body to the pattern object
pattern.append("HELLO *")

template = Template()
template.append(Star())

# add the pattern to the category
cat.append(pattern).append(template)

# print the category
print(cat)  # this should print: <Category><Pattern>HELLO *</Pattern></Category>

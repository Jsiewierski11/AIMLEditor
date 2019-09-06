from Model.Data import *

# create the category object
cat = Category()

# print the category
print(cat)  # this should print: <Category></Category>

# create a pattern object
pattern = Pattern()

# add some body to the pattern object
pattern.append("HELLO *")

# create a comment object
comment = Comment()
print(comment)
print(comment.type)
comment.append("This is a comment")

# adding comment to the category
cat.append(comment)

# add the pattern to the category
cat.append(pattern)

# print the category
print(cat)  # this should print: <Category><Pattern>HELLO *</Pattern></Category>

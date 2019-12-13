from Model.Data import *

class CategoryCreator(object):
    def __init__(self):
        pass

    def make_simple_cat(self):
        category = Category()
        pattern = Pattern()
        template = Template()
        template.append("It is so good to see you. How are you doing?")
        category.append(pattern)
        category.append(template)

        return category

    def make_cat_rand(self):
        category = Category()
        pattern = Pattern()
        template = Template()
        random = Random()

        random.append(ConditionItem().append("This is a joke."))
        random.append(ConditionItem().append("This is a funny joke. How did you like it?"))
        random.append(ConditionItem().append("I like to play sports. What is your favorite?"))

        template.append(random)
        category.append(pattern)
        category.append(template)
        return category

    def make_cat_rand_tail(self):
        category = Category()
        pattern = Pattern()
        template = Template()
        random = Random()

        random.append(ConditionItem().append("This is a joke."))
        random.append(ConditionItem().append("This is a funny joke. How did you like it?"))
        random.append(ConditionItem().append("I like to play sports. What is your favorite?"))

        template.append(random)
        template.append("This is the actual last sentence.")
        category.append(pattern)
        category.append(template)
        return category

    def make_cat_rand_head_tail(self):
        category = Category()
        pattern = Pattern()
        template = Template()
        random = Random()

        template.append("This is the first sentence.")

        random.append(ConditionItem().append("This is a joke."))
        random.append(ConditionItem().append("This is a funny joke. How did you like it?"))
        random.append(ConditionItem().append("I like to play sports. What is your favorite?"))

        template.append(random)
        template.append("This is the actual last sentence.")
        category.append(pattern)
        category.append(template)
        return category
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

    def make_cat_rand_head_tail_oob(self):
        category = Category()
        pattern = Pattern()
        template = Template()
        random = Random()
        oob = Oob()
        robot = Robot()

        template.append("This is the first sentence.")

        random.append(ConditionItem().append("This is a joke."))
        random.append(ConditionItem().append("This is a funny joke. How did you like it?"))
        random.append(ConditionItem().append("I like to play sports. What is your favorite?"))

        template.append(random)
        template.append("This is the actual last sentence.")
        template.append(oob.append(robot))
        category.append(pattern)
        category.append(template)
        return category

    def make_cat_and_child(self):
        parent_category = Category()
        parent_pattern = Pattern()
        parent_template = Template()
        parent_oob = Oob()
        parent_robot = Robot()

        child_category = Category()
        child_pattern = Pattern()
        child_that = That()
        child_template = Template()
        child_oob = Oob()
        child_robot = Robot()

        parent_template.append("How are you?")
        parent_template.append(parent_oob.append(parent_robot))
        parent_category.append(pattern)
        parent_category.append(template)
    
        child_that.append("How are you?")
        child_template.append(child_oob.append(robot))
        child_category.append(pattern)
        child_category.append(that)
        child_category.append(template)

        return parent_category, child_category
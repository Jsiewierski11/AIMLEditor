from Model.Data import *

class AimlCreator(object):
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

    def make_aiml1(self):
        # create AIML structure
        aiml = AIML().append(
            Category().append(
                Pattern().append("START SESSION 1 *")
            ).append(
                Template().append(
                    Think().append(
                        Set("username").append("star")
                    ).append(
                        Set("topic").append("Session 1")
                    )
                ).append("Ok. Let's begin our session. How are you doing today?").append(Star()).append(
                    Oob().append(Robot())
                )
            )
        ).append(
            Topic("session").append(
                Category().append(
                    Pattern().append("*")
                ).append(
                    Template().append(
                        Think().append(Set("data").append(Star()))
                    ).append(
                        Condition("getsetimnet").append(
                            ConditionItem("verypositive").append("I am happy").append(
                                Oob().append(
                                    Robot().append(
                                        Options().append(
                                            Option("Yes")
                                        ).append(
                                            Option("No")
                                        )
                                    )
                                )
                            )
                        ).append(
                            ConditionItem("positive").append(
                                "I am not as happy")
                        )
                    )
                )
            )
        )
        return aiml

    def make_aiml2(self):
        aiml = AIML().append(
                        Category().append(
                            Pattern().append("YOU CAN DO BETTER")
                        ).append(
                            Template().append("Ok I will try.").append(Oob().append(Robot()))
                            )
                    ).append(
                        Category().append(
                            Pattern().append("WHAT DO YOU WANT TO TALK ABOUT")
                        ).append(
                            Template().append("I'll talk about whatever with you.")
                            .append(
                                Oob().append(Robot())
                            )
                        )
        )
        return aiml

    def make_cat_star(self):
        aiml = AIML().append(
                        Category().append(
                            Pattern().append("HELLO FRIEND")
                        ).append(
                            Template().append("Hey there").append(Star()).append(Oob().append(Robot()))
                        )
                )
        return aiml
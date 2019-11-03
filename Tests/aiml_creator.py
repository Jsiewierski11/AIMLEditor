from Model.Data import *

class AimlCreator(object):
    def __init__(self):
        pass

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
                ).append("Ok. Let's begin our session. How are you doing today <star/>?").append(
                    Oob().append(Robot())
                )
            )
        ).append(
            Topic("session").append(
                Category().append(
                    Pattern().append("*")
                ).append(
                    Template().append(
                        Think().append(Set("data").append("<star/>"))
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
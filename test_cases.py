import unittest
import Utils.Storage as Storage
from Model.Data import *


def make_aiml():
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

class TestFunctions(unittest.TestCase):

    def test_save_restore_aiml(self):
        aiml = make_aiml()
        Storage.save('test1', aiml)
        aiml2 = Storage.restore('test1')
        self.assertEqual(str(aiml), str(aiml2))

    def test_create_simple_category(self):
        cat = Category() #Create category obj
        pattern = Pattern() #Create pattern obj
        pattern.append("HELLO *") #Adding text to patter obj
        cat.append(pattern) #Placing pattern inside category obj
        self.assertEqual(str(cat), '<category><pattern>HELLO *</pattern></category>')


if __name__ == '__main__':
    unittest.main()
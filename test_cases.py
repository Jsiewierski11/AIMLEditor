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

def make_aiml2():
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

class TestFunctions(unittest.TestCase):

    def test_create_simple_category(self):
        cat = Category() #Create category obj
        pattern = Pattern() #Create pattern obj
        pattern.append("HELLO *") #Adding text to patter obj
        cat.append(pattern) #Placing pattern inside category obj
        self.assertEqual(str(cat), '<category><pattern>HELLO *</pattern></category>')
    
    def test_save_restore_aiml(self):
        aiml = make_aiml()
        Storage.save('test1', aiml)
        aiml2 = Storage.restore('test1')
        self.assertEqual(str(aiml), str(aiml2))

    # TODO: Make file path relative to project
    # def test_import(self):
    #     expected = make_aiml2()
    #     #NOTE: Make sure to not have the '.aiml' after file name. 
    #     #      Causes an aborted core dump. Why?
    #     imported = Storage.importAIML('/home/jarid/DFT/Test_Save/atomic')
    #     self.assertEqual(str(expected), str(imported))

    def test_export(self):
        #NOTE: Works with make_aiml2 but NOT make_aiml() might have
        #      something to do with the topic tag
        export = make_aiml2()
        Storage.exportAIML('./test_aimls/exporting', export)
        imported = Storage.importAIML('./test_aimls/exporting')
        self.assertEqual(str(export), str(imported))
    
    def test_import_jupiter(self):
        imported = Storage.importAIML('./test_aimls/jupiter')
        exported = Storage.importAIML('./test_aimls/jupiter_exp', imported)
        jup = open('./test_aimls/jupiter', 'r')
        jup_contents = jup.read()
        jup_exp = open('./test_aimls/jupiter_exp', 'r')
        jup2_contents = jup_exp.read()
        self.assertEqual(jup_contents, jup2_contents)

if __name__ == '__main__':
    unittest.main()
    # make_aiml2()
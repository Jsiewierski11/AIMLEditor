import unittest
import Utils.Storage as Storage
from Model.Data import *
# import xml.etree.ElementTree as ET
# from Tree.CommentedTreeBuilder import *

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
        Storage.save('test_pickle/test1', aiml)
        aiml2 = Storage.restore('test_pickle/test1')
        self.assertEqual(str(aiml), str(aiml2))

    def test_import(self):
        expected = make_aiml2()
        #NOTE: Make sure to not have the '.aiml' after file name. 
        #      Causes an aborted core dump. Why?
        imported = Storage.importAIML('./test_aimls/atomic')
        self.assertEqual(str(expected), str(imported))

    def test_export(self):
        #NOTE: Works with make_aiml2 but NOT make_aiml() might have
        #      something to do with the topic tag
        export = make_aiml2()
        Storage.exportAIML('./test_aimls/exporting', export)
        imported = Storage.importAIML('./test_aimls/exporting')
        self.assertEqual(str(export), str(imported))

    
    def test_print_comment(self):
        comment = Comment()
        self.assertEqual(str(comment), "<!--  -->")

    def test_parsing_commented_tree(self):
        parser = ET.XMLParser(target=CommentedTreeBuilder())
        tree = ET.parse('test_aimls/utils.aiml', parser)
        tree.write('test_aimls/out.aiml', xml_declaration=True, encoding='UTF-8')
        util = Storage.importAIML('./test_aimls/utils')
        out = Storage.importAIML('./test_aimls/out')
        self.assertEqual(str(util), str(out))


    # TODO: Figure out a consistent whitespace formatting
    '''

    # NOTE: Fails due to whitespace mismatch. Is this a concern?
    def test_comments_util_import(self):
        imported = Storage.importAIML('./test_aimls/utils')
        Storage.exportAIML('./test_aimls/utils_exp', imported)
        exported = Storage.importAIML('./test_aimls/utils_exp')
        self.assertEqual(str(imported),str(exported))

    # NOTE: Fails due to whitespace mismatch. Is this a concern?
    def test_import_jupiter(self):
        imported = Storage.importAIML('./test_aimls/jupiter')
        exported = Storage.exportAIML('./test_aimls/jupiter_exp', imported)
        jup = open('./test_aimls/jupiter.aiml', 'r')
        jup_contents = jup.read()
        jup_exp = open('./test_aimls/jupiter_exp.aiml', 'r')
        jup2_contents = jup_exp.read()
        self.assertEqual(jup_contents, jup2_contents)
    '''

    def test_compile(self):
        expected_aiml = make_aiml()
        test_aiml = compileToAIML(aiml)
        self.assertEqual(test_aiml, expected_aiml)
        

    
if __name__ == '__main__':
    unittest.main()
    # make_aiml2()
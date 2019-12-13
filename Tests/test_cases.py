import unittest
import os, sys

sys.path.append(os.path.abspath('..'))
import Utils.Storage as Storage
from Model.Data import *
from Tests.aiml_creator import AimlCreator
from Tests.category_creator import CategoryCreator
from Tests.test_widget import EditorWidget



class TestFunctions(unittest.TestCase):

    def test_create_simple_category(self):
        cat = Category() #Create category obj
        pattern = Pattern() #Create pattern obj
        pattern.append("HELLO *") #Adding text to patter obj
        cat.append(pattern) #Placing pattern inside category obj
        template = Template()
        cat.append(template)
        self.assertEqual(str(cat), '<category>\n    <pattern>HELLO *</pattern>\n    <template></template>\n</category>')
    
    def test_save_restore_aiml(self):
        ac = AimlCreator()
        aiml = ac.make_aiml1()
        Storage.save('test_pickle/test1', aiml)
        aiml2 = Storage.restore('test_pickle/test1')
        self.assertEqual(str(aiml), str(aiml2))

    def test_import(self):
        ac = AimlCreator()
        expected = ac.make_aiml2()
        #NOTE: Make sure to not have the '.aiml' after file name. 
        #      Causes an aborted core dump. Why?
        imported = Storage.importAIML('./test_aimls/atomic')
        self.assertEqual(str(expected), str(imported))

    def test_export(self):
        #NOTE: Works with make_aiml2 but NOT make_aiml() might have
        #      something to do with the topic tag
        ac = AimlCreator()
        export = ac.make_aiml2()
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


    def test_comments_util_import(self):
        imported = Storage.importAIML('./test_aimls/utils')
        Storage.exportAIML('./test_aimls/utils_exp', imported)
        exported = Storage.importAIML('./test_aimls/utils_exp')
        print(f'TEST:\n{imported}')
        print(f'EXPECTED:\n{exported}')
        self.maxDiff = None
        self.assertEqual(str(imported),str(exported))

    
    def test_import_jupiter(self):
        imported = Storage.importAIML('./test_aimls/jupiter')
        Storage.exportAIML('./test_aimls/jupiter_exp', imported)
        exported = Storage.importAIML('./test_aimls/jupiter_exp')
        self.assertEqual(str(imported),str(exported))

        # NOTE: This way of reading a file and checking for assertion fails. Why?
        # jup = open('./test_aimls/jupiter.aiml', 'r')
        # jup_contents = jup.read()
        # jup_exp = open('./test_aimls/jupiter_exp.aiml', 'r')
        # jup2_contents = jup_exp.read()
        # self.assertEqual(jup_contents, jup2_contents)


    def test_topic_import(self):
        imported = Storage.importAIML('./test_aimls/mexican_food')
        Storage.exportAIML('./test_aimls/mexican_food_exp', imported)
        exported = Storage.importAIML('./test_aimls/mexican_food_exp')
        # print(f'TEST:\n{imported}')
        # print(f'EXPECTED:\n{exported}')
        self.assertEqual(str(imported),str(exported))
    

    # def test_map_to_string(self):
    #     ac = AimlCreator()
    #     aiml = ac.make_aiml()
    #     try:
    #         print(aiml)
    #     except Exception as ex:
    #         print(ex)

    
    def test_compile_aiml1(self):
        ac = AimlCreator()
        expected_aiml = ac.make_aiml1()
        test_aiml = Storage.compileToAIML(str(expected_aiml))
        # print('TEST:\n{}'.format(test_aiml))
        # print('EXPECTED:\n{}'.format(expected_aiml))
        self.assertEqual(str(test_aiml), str(expected_aiml))

    def test_compile_aiml2(self):
        ac = AimlCreator()
        expected_aiml = ac.make_aiml2()
        test_aiml = Storage.compileToAIML(str(expected_aiml))
        # print('TEST:\n{}'.format(test_aiml))
        # print('EXPECTED:\n{}'.format(expected_aiml))
        self.assertEqual(str(test_aiml), str(expected_aiml))
    
    def test_make_cat_start_compile(self):
        ac = AimlCreator()
        expected_aiml = ac.make_cat_star()
        # print('EXPECTED:\n{}'.format(expected_aiml))
        test_aiml = Storage.compileToAIML(str(expected_aiml))
        # print('TEST:\n{}'.format(test_aiml))
        self.assertEqual(str(test_aiml), str(expected_aiml))

    
    def test_getLastSentence(self):
        cc = CategoryCreator()
        category = cc.make_simple_cat()
        true = ["How are you doing?"]
        widget = EditorWidget()
        result = widget.getLastSentence(category)
        self.assertEqual(result, true)

    def test_getLastSentence_rand(self):
        cc = CategoryCreator()
        category = cc.make_cat_rand()
        widget = EditorWidget()
        true = ["This is a joke.", "How did you like it?", "What is your favorite?"]
        result = widget.getLastSentence(category)
        self.assertEqual(result, true)

    def test_getLastSentence_rand_tail(self):
        cc = CategoryCreator()
        category = cc.make_cat_rand_tail()
        widget = EditorWidget()
        true = ["This is the actual last sentence."]
        result = widget.getLastSentence(category)
        self.assertEqual(result, true)

    def test_getLastSentence_rand_head_tail(self):
        cc = CategoryCreator()
        category = cc.make_cat_rand_head_tail()
        widget = EditorWidget()
        true = ["This is the actual last sentence."]
        result = widget.getLastSentence(category)
        print(f"category created for test:\n{category}")
        self.assertEqual(result, true)

    def test_getLastSentence_rand_head_tail_oob(self):
        cc = CategoryCreator()
        category = cc.make_cat_rand_head_tail_oob()
        widget = EditorWidget()
        true = ["This is the actual last sentence."]
        result = widget.getLastSentence(category)
        print(f"category created for test:\n{category}")
        self.assertEqual(result, true)

    
if __name__ == '__main__':
    unittest.main()
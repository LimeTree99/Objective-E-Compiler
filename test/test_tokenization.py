import unittest
from src import Token, Tokenize


class TestTokenize(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fh = open("test/snipets/code_example_2.e", 'r')
        cls.code = fh.read()
        fh.close()
        
        cls.tokenize = Tokenize()
    
    @classmethod
    def tearDownClass(cls):
        pass
        
    def test_compute_first(self):
        expected1 = '''class Example { void Example ( ) { print ('''
        expected2 = ''') ; } }'''
        
        expected = expected1.split(' ')
        expected.append('"1 . / \ @ initalized"')
        expected.extend(expected2.split(' '))
        
        self.tokenize.tokenize(self.code)
        
        
        result = []
        for token in self.tokenize.tokens:
            result.append(token.content)
        
        
        
        
        self.assertEqual(result, expected)
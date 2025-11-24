import unittest
from src import Token, Tokenize


class TestTokenize(unittest.TestCase):
    def assertTokenEqual(self, a, b, msg=None):
        if a.id == b.id and a.name == b.name and a.type == b.typ \
            and a.content == b.content and a.line == b.line:
            return True
        else:
            a.failureException(msg + "aaaaaaaaaaaaaaaaaaaaaaa")
            return False
        
    def setup(self):
        self.addTypeEqualityFunc(type(Token), self.assertTokenEqual)
        
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
        expected1 = 'class Example { void Example ( ) { print ('
        expected2 = ') ; } }'
        
        expected = expected1.split(' ')
        expected.append('"1 . / \ @ initalized"')
        expected.extend(expected2.split(' '))
        
        self.tokenize.tokenize(self.code)
        
        
        result = []
        for token in self.tokenize.tokens:
            result.append(token.content)
        
        
        
        
        self.assertEqual(result, expected)
        
    def test_testing_class(self):
        result = Token(1,"a","a","a",1)
        expected = Token(1,"a","a","a",1)
        
        if result.id == expected.id and result.name == expected.name and result.type == expected.type \
            and result.content == expected.content and result.line == expected.line:
            return True
        else:
            self.fail("erin waz heer")
        
        
        
        
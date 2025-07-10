import unittest
from src import Grammar, Symbol


class TestGrammar1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.grammar = Grammar([
            Symbol('S', ['x OP x', 'x'], False),
            Symbol('OP', ['+','-'], False)
        ])
        cls.grammar.link()
        cls.grammar.compute_first()
        cls.grammar.compute_follow()
    
    @classmethod
    def tearDownClass(cls):
        del cls.grammar
        
    def test_compute_first(self):
        expected = [
            {'x'},
            {'+','-'}
        ]
        
        result = []
        for prod in self.grammar.productions:
            result.append(set(prod.get_first()))
        
        self.assertEqual(result, expected)
        
    def test_compute_follow(self):
        expected = [
            {'$'},
            {'x'}
        ]
        
        result = []
        for prod in self.grammar.productions:
            result.append(set(prod.follow))
        
        self.assertEqual(result, expected)
        
class TestGrammar2(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.grammar = Grammar([
            Symbol('S', ['INT OP INT', 'INT'], False),
            Symbol('OP', ['+','-', '*', '/'], False),
            Symbol('INT', ['1','2','3','4','5'], False),
        ])
        
        cls.grammar.link()
        cls.grammar.compute_first()
        cls.grammar.compute_follow()
        
    @classmethod
    def tearDownClass(cls):
        del cls.grammar
        
    def test_compute_first(self):
        expected = [
            {'5', '4', '2', '3', '1'}, 
            {'-', '/', '+', '*'}, 
            {'5', '4', '2', '3', '1'}
        ]
        
        result = []
        for prod in self.grammar.productions:
            result.append(set(prod.get_first()))
        
        self.assertEqual(result, expected)
        
    def test_compute_follow(self):
        expected = [
            {'$'},
            {'5', '4', '2', '3', '1'},
            {'+','-', '*', '/', '$'}
        ]
        
        result = []
        for prod in self.grammar.productions:
            result.append(set(prod.follow))
        
        self.assertEqual(result, expected)

class TestGrammarWithEpsilon1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.grammar = Grammar([
            Symbol('S', ['( ARGS )'], False),
            Symbol('ARGS', ["ARG ARGS'", 'ε'], False),
            Symbol("ARGS'", [", ARGS'", 'ε'], False),
            Symbol('ARG', ['type name'], False),
        ])
        cls.grammar.link()
        cls.grammar.compute_first()
        cls.grammar.compute_follow()
    
    @classmethod
    def tearDownClass(cls):
        del cls.grammar
        
    def test_compute_first(self):
        expected = [
            {'('}, 
            {'ε', 'type'}, 
            {'ε', ','}, 
            {'type'}
        ]
        
        result = []
        for prod in self.grammar.productions:
            result.append(set(prod.get_first()))
        
        self.assertEqual(result, expected)
        
    def test_compute_follow(self):
        expected = [
            {'$'},
            {')'},
            {')'},
            {')',','}
        ]
        
        result = []
        for prod in self.grammar.productions:
            result.append(set(prod.follow))
        
        self.assertEqual(result, expected)


class TestGrammarWithEpsilon2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.grammar = Grammar([
            Symbol('S', ['START MAYBE end'], False),
            Symbol('START', ['start'], False),
            Symbol('MAYBE', ['maybe', 'ε'], False),
        ])
        cls.grammar.link()
        cls.grammar.compute_first()
        cls.grammar.compute_follow()
    
    @classmethod
    def tearDownClass(cls):
        del cls.grammar
        
    def test_compute_first(self):
        expected = [
            {'start'},
            {'start'},
            {'maybe', 'ε'}
        ]
        
        result = []
        for prod in self.grammar.productions:
            result.append(set(prod.get_first()))
        
        self.assertEqual(result, expected)
        
    def test_compute_follow(self):
        expected = [
            {'$'},
            {'maybe', 'end'},
            {'end'}
        ]
        
        result = []
        for prod in self.grammar.productions:
            result.append(set(prod.follow))
        
        self.assertEqual(result, expected)
    
    
   
#if __name__ == '__main__':
#    unittest.main()
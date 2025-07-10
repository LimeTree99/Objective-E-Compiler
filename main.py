from src import Token, Tokenize, Symbol, Grammar
 

    
def run_tokenizer():
    tokenize = Tokenize()
    
    fh = open('test.code', 'r')
    code = fh.read()
    fh.close()
    
    tokenize.tokenize(code)
    
    
    for token in tokenize.tokens:
        print(token.type, token.value,end='\n')
    print()
            
if __name__ == '__main__':
    print('Gram 1')
    gram1 = Grammar([Symbol('S', ['INT OP INT', 'INT', 'ε'], False),
                    Symbol('OP', ['+','-', '*', '/'], False),
                    Symbol('INT', ['1','2','3','4','5'], False),
                    ],)
    
    print(gram1)
    
    gram1.link()
    gram1.compute_first()
    gram1.compute_follow()
    print('------------------------------------------')
    gram1.print_first_follow()
    
    print('==========================================')
    print('Gram 2')
    gram2 = Grammar([Symbol('S', ['x OP x', 'x'], False),
                    Symbol('OP', ['+','-'], False),
                    ],)
    
    print(gram2)
    
    gram2.link()
    gram2.compute_first()
    gram2.compute_follow()
    print('------------------------------------------')
    gram2.print_first_follow()
    
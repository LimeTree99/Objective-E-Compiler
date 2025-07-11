from src import Token, Tokenize, Symbol, Grammar
 

    
def run_tokenizer():
    tokenize = Tokenize()
    
    fh = open('specification/test.code', 'r')
    code = fh.read()
    fh.close()
    
    tokenize.tokenize(code)
    
    
    for token in tokenize.tokens:
        print(token.type, token.value,end='\n')
    print()
    
    
def language_grammar():
    print('Objective E Grammar')
    
    a = [
        ['S',['CLASS','IMPORT']],
        ['IMPORT',['import identifier']],
        ['CLASS',['class identifier { CLASS_CONTENT }']],
        []
    ]
    format_gram = []
    for line in a:
        format_gram.append(Symbol(a[0], a[1], False))
    
    gram = Grammar(format_gram)
    
    print(gram)
    
    gram.link()
    gram.compute_first()
    gram.compute_follow()
    print('------------------------------------------')
    gram.print_first_follow()
            
if __name__ == '__main__':
    run_tokenizer()
    print('==========================================')
    print()
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
    gram2 = Grammar([
                        Symbol('S', ['START MAYBE end'], False),
                        Symbol('START', ['start'], False),
                        Symbol('MAYBE', ['maybe', 'ε'], False),
                    ],)
    
    print(gram2)
    
    gram2.link()
    gram2.compute_first()
    gram2.compute_follow()
    print('------------------------------------------')
    gram2.print_first_follow()
    
    
    
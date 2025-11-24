from src import Token, Tokenize, Symbol, Grammar, LL1_Table
 
    
    
def run():
    print('Objective E')
    
    tokenize = Tokenize()
    
    fh = open('specification/test.e', 'r')
    code = fh.read()
    fh.close()
    
    tokenize.tokenize(code)
    print('----------------')
    print('| TOKENIZATION |')
    print('----------------')
    for token in tokenize.tokens:
        print(token.line, token.type, token.content,end='\n')
    print()
    
    fh = open('specification/objective_e_grammar.txt', 'r')
    grammar_string = fh.read()
    fh.close()
        
    gram = Grammar(grammar_string)
    print('---------------------')
    print('| GRAMMAR FROM FILE |')
    print('---------------------')
    print(gram)
    print('------------------------------------------')
    
    gram.link()
    gram.compute_first()
    gram.compute_follow()
    print()
    print('-----------------------------------')
    print('| FIRST & FOLLOW OF ABOVE GRAMMAR |')
    print('-----------------------------------')
    gram.print_first_follow()
    print('------------------------------------------')
    print()
    print('-------------------------------')
    print('| LL1 TABLE OF ABOVE GRAMMEAR |')
    print('-------------------------------')
    lex = LL1_Table(gram)
    lex.print()
    print('------------------------------------------')
    
if __name__ == '__main__':
    run()
    
    
    
    
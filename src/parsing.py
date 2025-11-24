


class Symbol:
    def __init__(self, name:str, rules:list, terminal:bool):
        """
        A symbol for use within a grammar, can be either a termial or a production
        
        param:
            name (str): the name of the production
            rules [str, ...]: a list of rules
            terminal (bool): if the symbol is a termial
        """
        self.name = name
        self.rules = rules
        self.terminal = terminal
        
        # has the following format:
        # [ 
        #   [ link, link, ... ], 
        #   [ link, link, ... ], 
        #   ... 
        # ]
        # link is a reference to other Productions()
        # if link is None then that is a terminal
        #
        # naming convention:
        # [ <rules>
        #   [ <symbol>, ... ], <string>
        #   ... 
        # ]
        self.rules_link = []
        
        self.first = []
        self.follow = []
        
    def compute_first(self):
        for string_i in range(len(self.rules_link)):
            self.first.append([])
            string = self.rules_link[string_i]
            symbol = string[0]
            if symbol.terminal:
                self.first[-1] = list(set(self.first[-1] + [symbol.name]))
            else:
                if len(symbol.first) == 0:
                    symbol.compute_first()
                self.first[-1] = list(set(self.first[-1] + symbol.get_first()))
    
    def get_first(self):
        first = []
        for string in self.first:
            for terminal in string:
                first.append(terminal)
                
        return list(set(first))
    
    def compute_follow(self, grammar):
        """
        given a grammar compute the follow set for this production 
        
        param:
        grammar (Grammar): the grammar this symbol is a part of
        """
        # be sure that there is no left recursion
        
        # for epsilon:
        # only relivent in situations such as for 
        # follow of B: A->aBC, C->ε
        # where 1 or more productions with ε follow 
        # the production we are trying to find the 
        # follow of 
        # stratagy:
        # recursively add the follow of each production 
        # where A->ε to the current production
        # ex. 
        # A->aBCDb, C->ε, D->ε
        # follow(B) = follow(C) = follow(C)
        
        if len(self.follow) == 0:
            if self.name == grammar.productions[0].name:
                self.follow.append('$')
            for search_prod in grammar.productions:
                if search_prod.name != self.name:
                    for rule in search_prod.rules:
                        rule_split = rule.split(' ')
                        for index in range(len(rule_split)):
                            if self.name == rule_split[index]:
                                if index + 1 == len(rule_split):
                                    # at end of this production
                                    search_prod.compute_follow(grammar)
                                    self.follow.extend(search_prod.follow)
                                    pass
                                else:
                                    # symbol found in middile of production
                                    next_prod = grammar.get_production(rule_split[index + 1])
                                    if next_prod == None:
                                        # terminal
                                        self.follow.append(rule_split[index + 1])
                                    else:
                                        # other production
                                        self.follow.extend(next_prod.get_first())
                                        if 'ε' in next_prod.get_first():
                                            self.follow.remove('ε')
                                            next_prod.compute_follow(grammar)
                                            self.follow.extend(next_prod.follow)
                                    
                            
            
        
    def print_link(self):
        for string in self.rules_link:
            for symbol in string:
                print(symbol.name, end=' ')
            print('| ', end='')
        print()
    
    def __str__(self):
        s = self.name + ' ' * (15 - len(self.name)) + '->   '
        for rule in self.rules:
            s = f'{s}{rule} | '
        if len(self.rules) > 0:
            s = s[:-2]
        return s
        
    
class Grammar:
    def __init__(self, definition):
        """
        the definition can either be a list of symbols or a correcly formated string to be parsed  
        """
        if type(definition) == str:
            # a quick and dirty parser for the string definitions of grammars 
            self.productions = []
    
            for line in definition.split('\n'):
                line = line.strip()
                if line != '' and line[0] != '#':
                    line = line.split('->')
                    line[0] = line[0].strip()
                    line[1] = line[1].strip()
                    self.productions.append(Symbol(line[0], line[1].split(' | '), False))
        else:
            self.productions = definition
        
    def link(self):
        # I do not trust that this is correct
        # its a little hard to verify if it is 
        # but so far I have found no bugs 
        # but I've done almost no testing
        
        # update: I ended up implimnting some unit testing 
        # and it's been good to varify that it's working
        # all right. It could probably use some work though 
        # stll, I'm not super confident of the test coveage.
        for prod in self.productions:
            prod.rules_link = []
            for string in prod.rules:
                prod.rules_link.append([])
                symbols = string.split(' ')
                for symbol in symbols:
                    i = 0
                    found = False
                    while not found and i < len(self.productions):
                        if symbol == self.productions[i].name:
                            found = True
                        i += 1
                    i -= 1
                    if found:
                        prod.rules_link[-1].append(self.productions[i])
                    else:
                        prod.rules_link[-1].append(Symbol(symbol, [], True))
                
    def compute_first(self):
        for prod in self.productions:
            if len(prod.first) == 0:
                prod.compute_first()
    
    def compute_follow(self):
        self.productions[0].compute_follow(self)
        
        for prod in self.productions[1:]:
            prod.compute_follow(self)
    
    def get_production(self, name):
        i = 0
        prod = None
        while i < len(self.productions) and prod == None:
            if self.productions[i].name == name:
                prod = self.productions[i]
            i += 1
        return prod
    
    def print_first_follow(self):
        print("Production          First               Follow")
        for prod in self.productions:
            print(prod.name + ' ' * (20 - len(prod.name)), end='')
            
            s = ''
            for symbol in prod.get_first():
                s = s + symbol + ', '
                
            print('{' + s[:-2] + '}' + ' ' * (20 - len(s)),end='')
            
            s = ''
            for symbol in prod.follow:
                s = s + symbol + ', '
            print('{' + s[:-2] + '}')
        
    def __str__(self):
        s = ''
        for prod in self.productions:
            s = f'{s}{str(prod)}\n'
        if len(self.productions) > 0:
            s = s[:-1]
        return s
    


# how do I wnat to do the accesing of table elements? dict (obvously)
# for x it should be the Token.id accesed through Grammar.
class LL1_Table:
    def __init__(self, grammar:Grammar):
        self.grammar = grammar
        self.table = {}
        self.terminals = []
        
        self.generate_table()
        # table structure
        # {  
        #   production_name(str) : { 
        #       token_name(str) : production
        #   }
        # }
        #
        #
        
    # should I just put this in __init__ ?
    # what does the above question mean? why would I do that?
    def generate_table(self):
        "generate the table based on the given grammar"  
        for prod in self.grammar.productions:
            self.table[prod.name] = {}
            #print("production: " + prod.name)
            for i in range(len(prod.rules)):
                rule = prod.rules[i]
                first = prod.first[i]
                self.terminals = list(set(self.terminals + first))
                #print("\trule: "+ rule + ", first: " + str(first))                
                for token in first:
                    self.table[prod.name][token] = rule
                    
        print()
    
    def parse(self, tokens):
        pass
           
    def print(self, space=20):
        print(space * ' ',end='')
        for terminal in self.terminals:
            print('|' + terminal + ((space-len(terminal)) * ' '), end='')
        print()
        for prod in self.table:
            print(prod + ((space-len(prod)) * ' '), end='')
            for terminal in self.terminals:
                if terminal in self.table[prod]:
                    print('|' + self.table[prod][terminal] + ((space-len(self.table[prod][terminal])) * ' '), end='')
                else:
                    print('|' + space * '-', end='')
            print()
        
                
        
        
        
        
        
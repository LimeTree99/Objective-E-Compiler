import re


class Token:
    def __init__(self, name, typ, content):
        self.name = name
        self.type = typ
        self.value = content
        
    def __str__(self):
        return f"<Token object; type={self.type}, value={self.value}>"

class Tokenize:
    def __init__(self):
        # order of this list is important
        self.token_re = [
            {"name":"class" ,"type":"keyword", "re":re.compile(r"class")},
            {"name":"return" ,"type":"keyword", "re":re.compile(r"return")},
            {"name":"if" ,"type":"keyword", "re":re.compile(r"if")},
            {"name":"else" ,"type":"keyword", "re":re.compile(r"else")},
            {"name":"while" ,"type":"keyword", "re":re.compile(r"while")},
            {"name":"for" ,"type":"keyword", "re":re.compile(r"for")},
            {"name":"true" ,"type":"literal_bool", "re":re.compile(r"true")},
            {"name":"false" ,"type":"literal_bool", "re":re.compile(r"false")},
            {"name":"float" ,"type":"literal", "re":re.compile(r"\d+\.\d*")},
            {"name":"int" ,"type":"literal", "re":re.compile(r"\d+")},
            {"name":"+" ,"type":"operator", "re":re.compile(r"\+")},
            {"name":"-" ,"type":"operator", "re":re.compile(r"-")},
            {"name":"*" ,"type":"operator", "re":re.compile(r"\*")},
            {"name":"/" ,"type":"operator", "re":re.compile(r"/")},
            {"name":"{" ,"type":"seperator", "re":re.compile(r"{")},
            {"name":"}" ,"type":"seperator", "re":re.compile(r"}")},
            {"name":"(" ,"type":"seperator", "re":re.compile(r"\(")},
            {"name":")" ,"type":"seperator", "re":re.compile(r"\)")},
            {"name":"," ,"type":"seperator", "re":re.compile(r",")},
            {"name":";" ,"type":"seperator", "re":re.compile(r";")},
            {"name":"=" ,"type":"assignment", "re":re.compile(r"=")},
            {"name":"identifier" ,"type":"identifier", "re":re.compile(r"[\w]+[\w\d-]*")},
            {"name":"attribute" ,"type":"attribute", "re":re.compile(r"@[\w]+[\w\d-]*")},
        ]
        self.tokens = []
        self.cursor = 0
        self.code = None
        
    def get_cur(self)->str:
        "return the current character that the cursor is on"
        return self.code[self.cursor]
        
    def cursor_move(self, amount:int=1)->bool:
        "returns true upon succesful move"
        self.cursor += amount
        if self.cursor >= len(self.code):
            self.cursor = len(self.code) - 1
            return False
        else:
            return True
            
    def cursor_at_end(self)->bool:
        if self.cursor >= len(self.code) - 1:
            return True
        else:
            return False
        
    def get_next_token(self)->re.Match:
        "return the next token and advance cursor to after it"
        "return None if not found"
        i = 0
        match = None
        while i < len(self.token_re) and match == None:
            match = self.token_re[i]["re"].match(self.code[self.cursor:])
            i += 1
        # so i points to found token
        i -= 1
            
        if match == None:
            token = None
        else:
            self.cursor_move(match.end())
            token = Token(self.token_re[i]["name"], self.token_re[i]["type"], match.group())
        return token
        
    def tokenize(self, code:str):
        self.code = code
        token_i = 0
        found = False
        
        
        while not self.cursor_at_end():
            
            # remove whitespace
            while self.get_cur() in " \n":
                self.cursor_move()
                
            #comments
            if self.get_cur() == "/":
                self.cursor_move()
                if self.get_cur() == "/":
                    while self.get_cur() != "\n" and not self.cursor_at_end():
                        self.cursor_move()
            
            #strings
            if self.get_cur() == '"':
                end = False
                string = ""
                self.cursor_move()
                while not end:
                    if self.get_cur() == "\\":
                        self.cursor_move()
                        string = string + self.get_cur()
                    elif self.get_cur() == "\"":
                        end = True
                    else:
                        string = string + self.get_cur()
                    self.cursor_move()
                self.tokens.append(Token("string", "literal", string))
            
            if not self.cursor_at_end():
                token = self.get_next_token()
                
                if token != None:
                    self.tokens.append(token)  
                else:
                    for token in self.tokens:
                        print(token)
                    print(f"Error: token number {len(self.tokens)} not found")
                    print(self.code[self.cursor:])
                    
                    # bad form here change this in the future
                    # you'll probably want to continue processing the code and 
                    # here you can output an error report for each syntax error 
                    break
       
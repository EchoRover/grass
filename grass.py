from lexer import *

def run(text,filename):
    lexer = Lexer(text,filename)
    tokens,error = lexer.tokeniser()
    if error:
        return error.stringfy()
    else:
        return tokens



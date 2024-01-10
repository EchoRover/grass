from lexerMod import *
from parserMod import *
from interpreterMod import *



def run(text,filename):
    #tokens
    lexer = Lexer(text,filename)
    tokens,error = lexer.tokeniser()
    if error:
        return error.stringfy()

    #parser

    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return ast.error.stringfy()
    
    # print(ast.node,"ast nodes")
    
    interpreter = Interpreter()
    context = Context('<program>')
    result = interpreter.visit(ast.node,context)
    if result.error:
        return result.error.stringfy()

    return result.value
    
    #interpreter




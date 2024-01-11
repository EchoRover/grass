from lexerMod import *
from parserMod import *
from interpreterMod import *


global_symbol_table = Symbols()
global_symbol_table.set_var(K_NULL,Number(0))
global_symbol_table.set_var(K_TRUE,Number(1))
global_symbol_table.set_var(K_FALSE,Number(0))



def run(text,filename):
    #tokens
    lexer = Lexer(text,filename)
    tokens,error = lexer.tokeniser()
    if error:
        return error.stringfy()
    
    # print(tokens)

    #parser

    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return ast.error.stringfy()
    
    # print(ast.node,"ast nodes")
    
    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node,context)
    if result.error:
        return result.error.stringfy()

    if result :
        return result.value
    
    #interpreter




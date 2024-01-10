
from globaltools import *

#Errors
class InvalidSyntaxError(Error):
     def __init__(self,details,error_start_cursor,error_end_cursor):
        super().__init__('Syntax Error',details,error_start_cursor,error_end_cursor)



#Nodes
class UnaryOperationNode:
    def __init__(self,operator,node):
        self.node = node
        self.operator = operator
        self.pos_start = self.operator.pos_start
        self.pos_end = self.node.pos_end    
    def __repr__(self):
        return f"({self.operator} {self.node})"

class NumberNode:
    def __init__(self,token):
        self.token = token
        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

    
    def __repr__(self):
        return f"{self.token}"

class BinaryOperationNode:
    def __init__(self,leftnode,token,rightnode):
        self.left_node = leftnode
        self.token = token
        self.right_node = rightnode
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    
    def __repr__(self):
        return f"({self.left_node},{self.token},{self.right_node})"

#parser

class CheckParserResult:
    def __init__(self):
        self.error = None
        self.node = None
    def register(self,result):
        if isinstance(result,CheckParserResult):
            if result.error:
                self.error = result.error
            return result.node
        return result
    def success(self,node):
        self.node = node
        return self
    def failure(self,error):
        self.error = error
        return self


class Parser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.current_token = None
        self.token_cursor = -1
        self.move_cursor()
    
    def move_cursor(self):
        self.token_cursor += 1
        if self.token_cursor < len(self.tokens):
            self.current_token = self.tokens[self.token_cursor]
        return self.current_token
    
    def parse(self):
        result = self.expression()
        if not result.error and self.current_token.type != T_EOF:
            return result.failure(InvalidSyntaxError("Excepted + - / *",self.current_token.pos_start,self.current_token.pos_end))
        return result
    
    def atom(self):
        response = CheckParserResult()
        token = self.current_token 

        if token.type in (T_INT,T_FLOAT):
            response.register(self.move_cursor())
            return response.success(NumberNode(token))
        
        elif token.type == T_LPARM:
            response.register(self.move_cursor())
            expr = response.register(self.expression())
            if response.error:
                return response
            if self.current_token.type == T_RPARM:
                response.register(self.move_cursor())
                return response.success(expr)
            else:
                return response.failure(InvalidSyntaxError('Expected " ) "',self.current_token.pos_start,self.current_token.pos_end))
        else:
            return response.failure(InvalidSyntaxError("Excepted + - int float (",self.current_token.pos_start,self.current_token.pos_end))
    
    def power(self):
        return self.binaryOpertation(self.atom,(T_POW,),self.factor)



    
    def factor(self):
        response = CheckParserResult()
        token = self.current_token 

        if token.type in (T_PLUS,T_MINUS):
            response.register(self.move_cursor())
            myfactor = response.register(self.factor())
            if response.error:
                return response
            return response.success(UnaryOperationNode(token,myfactor))
        
        return self.power()





        
    
    def term(self):
        return self.binaryOpertation(self.factor,(T_DIV,T_MUL))

    def expression(self):
        return self.binaryOpertation(self.term,(T_PLUS,T_MINUS))

     
    
    def binaryOpertation(self,sidefunc,operations,sidefunc2 = None):
        if sidefunc2 == None:
            sidefunc2 = sidefunc

        response = CheckParserResult()
        left = response.register(sidefunc())
        if response.error:
            return response
        while self.current_token.type in operations:
            operation_token = self.current_token
            response.register(self.move_cursor())
            right = response.register(sidefunc2())
            if response.error:
                return response
            left = BinaryOperationNode(left,operation_token,right)
        return response.success(left)



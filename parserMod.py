
from globaltools import *

#Errors
class InvalidSyntaxError(Error):
     def __init__(self,details,error_start_cursor,error_end_cursor):
        super().__init__('Syntax Error',details,error_start_cursor,error_end_cursor)



#Nodes
class IfNode:
    def __init__(self,cases,else_case):
        self.cases = cases
        self.else_case = else_case
        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_case or self.cases[-1][0]).pos_end 
class VarAssignNode:
    def __init__(self,var_name_token,var_value_node):
        self.name_token = var_name_token
        self.value_node = var_value_node
       
        self.pos_start = self.name_token.pos_start
        self.pos_end = self.value_node.pos_end

class VarAccessNode:
    def __init__(self,token):
        self.var_name_token = token

        self.pos_start = self.var_name_token.pos_start
        self.pos_end = self.var_name_token.pos_end


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
        self.advance_count = 0
    
    def register_move_cursor(self):
        self.advance_count += 1
    def register(self,result):
        self.advance_count += result.advance_count
        if result.error:
            self.error = result.error
        return result.node
       
    def success(self,node):
        self.node = node
        return self
    def failure(self,error):
        if not self.error or self.advance_count == 0:
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
    
    def if_expression(self):
        response = CheckParserResult()
        cases = []
        else_case = None
        if not self.current_token.matches(T_KEYWORD,K_IF):
            return response.failure(InvalidSyntaxError("expected if",current_token.pos_start,current_token.pos_end))
        response.register_move_cursor()
        self.move_cursor()
        condition = response.register(self.expression())
        if response.error:
            return response
        if not self.current_token.matches(T_KEYWORD,K_THEN):
            return response.failure(InvalidSyntaxError("expected then",self.current_token.pos_start,self.current_token.pos_end))
        response.register_move_cursor()
        self.move_cursor()

        expression = response.register(self.expression())
        if response.error:
            return response
        cases.append((condition,expression))

        while self.current_token.matches(T_KEYWORD,K_ELIF):
            response.register_move_cursor()
            self.move_cursor()
            condition = response.register(self.expression())
            if response.error:
                return response
            if not self.current_token.matches(T_KEYWORD,K_THEN):
                return response.failure(InvalidSyntaxError("expected then",self.current_token.pos_start,self.current_token.pos_end))
            response.register_move_cursor()
            self.move_cursor()

            expression = response.register(self.expression())
            if response.error:
                return response
            cases.append((condition,expression))
        if self.current_token.matches(T_KEYWORD,K_ELSE):
            response.register_move_cursor()
            self.move_cursor()
            else_case = response.register(self.expression())
            if response.error:
                return response
        return response.success(IfNode(cases,else_case))



    
    def atom(self):
        response = CheckParserResult()
        token = self.current_token 

        if token.type in (T_INT,T_FLOAT):
            response.register_move_cursor()
            self.move_cursor()
            return response.success(NumberNode(token))
        elif token.type == T_IDENTIFIER:
            response.register_move_cursor() 
            self.move_cursor()
            return response.success(VarAccessNode(token))
        
        elif token.type == T_LPARM:
            response.register_move_cursor() 
            self.move_cursor()
            expr = response.register(self.expression())
            if response.error:
                return response
            if self.current_token.type == T_RPARM:
                response.register_move_cursor() 
                self.move_cursor()
                return response.success(expr)
            else:
                return response.failure(InvalidSyntaxError('Expected " ) "',self.current_token.pos_start,self.current_token.pos_end))
        elif token.matches(T_KEYWORD,K_IF):
            if_expression = response.register(self.if_expression())
            if response.error:
                return response
            return response.success(if_expression)
            
        else:
            return response.failure(InvalidSyntaxError("Excepted identifier + - int float (",self.current_token.pos_start,self.current_token.pos_end))
    
    def power(self):
        return self.binaryOpertation(self.atom,(T_POW,),self.factor)
    

    
    def factor(self):
        response = CheckParserResult()
        token = self.current_token 

        if token.type in (T_PLUS,T_MINUS):
            response.register_move_cursor() 
            self.move_cursor()
            myfactor = response.register(self.factor())
            if response.error:
                return response
            return response.success(UnaryOperationNode(token,myfactor))
        
        return self.power()

    def term(self):
        return self.binaryOpertation(self.factor,(T_DIV,T_MUL))

    
    def arthimatic_expression(self):
        return self.binaryOpertation(self.term,(T_PLUS,T_MINUS))
    
    def comparison_expression(self):
        response = CheckParserResult()
        if self.current_token.matches(T_KEYWORD,K_NOT):
            operation_token = self.current_token
            response.register_move_cursor()
            self.move_cursor()
            node = response.register(self.comparison_expression())
            if response.error:
                return response
            

            return response.success(UnaryOperationNode(operation_token,node))
        node =  response.register(self.binaryOpertation(self.arthimatic_expression,(T_EQUAL,T_DOBEQUAL,T_GREATERTHEN,T_GREATEREQUALTHEN,T_LESSTHEN,T_LESSEREQUALTHEN)))
        if response.error:
            return response.failure(InvalidSyntaxError("Excepted identifier + - int float (",self.current_token.pos_start,self.current_token.pos_end))
        
        return response.success(node)


    def expression(self):
        response = CheckParserResult()
        if self.current_token.matches(T_KEYWORD,K_VAR):
            response.register_move_cursor() 
            self.move_cursor()

            if self.current_token.type != T_IDENTIFIER:
                return response.failure(InvalidSyntaxError("Expected Identifier",self.current_token.pos_start,self.current_token.pos_end))
            
            var_name = self.current_token
            response.register_move_cursor() 
            self.move_cursor()

            if self.current_token.type != T_EQUAL:
                return response.failure(InvalidSyntaxError("Expected =",self.current_token.pos_start,self.current_token.pos_end))
  
            response.register_move_cursor() 
            self.move_cursor()
            expression_val = response.register(self.expression())
            if response.error:
                 return response
            return response.success(VarAssignNode(var_name,expression_val))
        else:
            node = response.register(self.binaryOpertation(self.comparison_expression,((T_KEYWORD,K_AND),(T_KEYWORD,K_OR))))
            if response.error:
                return response.failure(InvalidSyntaxError("Excepted VAR int float identifier + - ( NOT",self.current_token.pos_start,self.current_token.pos_end))
            return response.success(node)


     
    
    def binaryOpertation(self,sidefunc,operations,sidefunc2 = None):
        if sidefunc2 == None:
            sidefunc2 = sidefunc

        response = CheckParserResult()
        left = response.register(sidefunc())
        if response.error:
            return response
        while self.current_token.type in operations or (self.current_token.type,self.current_token.value) in operations:
            operation_token = self.current_token
            response.register_move_cursor() 
            self.move_cursor()
            right = response.register(sidefunc2())
            if response.error:
                return response
            left = BinaryOperationNode(left,operation_token,right)
        return response.success(left)



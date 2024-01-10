from globaltools import *

#Error

class RuntimeError(Error):
    def __init__(self,details,error_start_cursor,error_end_cursor,context):
        super().__init__('RunTime Error',details,error_start_cursor,error_end_cursor)
        self.context = context

    def stringfy(self):
        result = self.generateback()
        result += f"{self.error}: {self.details}\n"
        result += self.extrabit()
        return result
    
    def generateback(self):
        result = ''
        pos = self.atstart
        context = self.context
        

        while context:
            result += f' File {pos.file_name}, line{str(pos.line_no + 1)}, in {context.display_name}\n'
            pos = context.parent_entry_pos
            context = context.parent
        return 'Traceback (most recent call last):\n' + result

    
    



#DATA TYPES

class Number:
    def __init__(self,value):
        self.value = value
        self.set_pos()
        self.set_context()
    def __repr__(self):
        return f"{self.value}"
    
    def set_pos(self,pos_start = None,pos_end = None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self
    def set_context(self,context = None):
        self.context = context
        return self
    def add(self,other):
        if isinstance(other,Number):
            return Number(self.value + other.value).set_context(self.context),None
        return None,RuntimeError("Type Error",other.pos_start,other.pos_end)
    def subtract(self,other):
        if isinstance(other,Number):
            return Number(self.value - other.value).set_context(self.context),None
        return None,RuntimeError("Type Error",other.pos_start,other.pos_end)
        
    def multiply(self,other):
        if isinstance(other,Number):
            return Number(self.value * other.value).set_context(self.context),None
        return None,RuntimeError("Type Error",other.pos_start,other.pos_end)
    
    def power_by(self,other):
        if isinstance(other,Number):
            return Number(self.value ** other.value).set_context(self.context),None
        print("Hihg")
        return None,RuntimeError("Type Error",other.pos_start,other.pos_end)
        
    def divided_by(self,other):
        if isinstance(other,Number):
            if other.value == 0:
                return None,RuntimeError("Division by Zero",
                other.pos_start,other.pos_end,self.context)
            return Number(self.value / other.value).set_context(self.context),None
        return None,RuntimeError("Type Error",other.pos_start,other.pos_end)
        
#Context

class Context:
    def __init__(self,display_name,parent = None,parent_entry_pos = None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos

#Interpreter

class CheckInterpreterResult:
    def __init__(self):
        self.value = None
        self.error = None
    def register(self,result):
        if result.error:
            self.error = result.error
        return result.value
    def success(self,value):
        self.value = value
        return self
    def failure(self,error):
        self.error = error
        return self

class Interpreter:
    def visit(self,node,context):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self,method_name,self.no_visit_method)
        return method(node,context)
    
    def no_visit_method(self,node,context):
        raise Exception(f"no visit_{type(node).__name__}")


    def visit_NumberNode(self,node,context):
        temp =  Number(node.token.value)
        temp.set_pos(node.pos_start,node.pos_end)

        return CheckInterpreterResult().success(Number(node.token.value).set_context(context).set_pos(node.pos_start,node.pos_end))

    def visit_BinaryOperationNode(self,node,context):
        response = CheckInterpreterResult()
       

        left = response.register(self.visit(node.left_node,context))
        if response.error:
            return response
        right = response.register(self.visit(node.right_node,context))
        if response.error:
            return response

        if node.token.type == T_PLUS:
            result,error = left.add(right)
        elif node.token.type == T_MINUS:
            result,error = left.subtract(right)
        elif node.token.type == T_MUL:
            result,error = left.multiply(right)
        elif node.token.type == T_DIV:
            result,error = left.divided_by(right)
        elif node.token.type == T_POW:
            result,error = left.power_by(right)
        
        if error:
            return response.failure(error)
        else:
            return response.success(result.set_pos(node.pos_start,node.pos_end))



    def visit_UnaryOperationNode(self,node,context):
        response = CheckInterpreterResult()
        number = response.register(self.visit(node.node,context))
        if response.error:
            return response
        
        error = None
    
        if node.operator.type == T_MINUS:
          
            number,error = number.multiply(Number(-1))
        if error:
            return response.failure(error)
        else:
            return response.success(number.set_pos(node.pos_start,node.pos_end))
       

        
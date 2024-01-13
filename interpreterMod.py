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
    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start,self.pos_end)
        copy.set_context(self.context)
        return copy

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
        return None,RuntimeError("Type Error",other.pos_start,other.pos_end)
        
    def divided_by(self,other):
        if isinstance(other,Number):
            if other.value == 0:
                return None,RuntimeError("Division by Zero",
                other.pos_start,other.pos_end,self.context)
            return Number(self.value / other.value).set_context(self.context),None
        return None,RuntimeError("Type Error",other.pos_start,other.pos_end)
    
    def equal_to(self,other):
        if isinstance(other,Number):
            return Number(int(self.value == other.value)).set_context(self.context),None
        return None,RuntimeError("Type Error",other.pos_start,other.pos_end)
    def not_equal_to(self,other):
        if isinstance(other,Number):
            return Number(int(self.value != other.value)).set_context(self.context),None
        return None,RuntimeError("Type Error",other.pos_start,other.pos_end)
    def greater_than(self,other):
        if isinstance(other,Number):
            return Number(int(self.value > other.value)).set_context(self.context),None
        return None,RuntimeError("Type Error",other.pos_start,other.pos_end)
    def lesser_than(self,other):
        if isinstance(other,Number):
            return Number(int(self.value < other.value)).set_context(self.context),None
        return None,RuntimeError("Type Error",other.pos_start,other.pos_end)
    def greater_than_equal(self,other):
        if isinstance(other,Number):
            return Number(int(self.value >= other.value)).set_context(self.context),None
        return None,RuntimeError("Type Error",other.pos_start,other.pos_end)
    def lesser_than_equal(self,other):
        if isinstance(other,Number):
            return Number(int(self.value <= other.value)).set_context(self.context),None
        return None,RuntimeError("Type Error",other.pos_start,other.pos_end)
    
    def anded(self,other):
        if isinstance(other,Number):
            return Number(int(self.value and other.value)).set_context(self.context),None
        return None,RuntimeError("Type Error",other.pos_start,other.pos_end)
    def ored(self,other):
        if isinstance(other,Number):
            return Number(int(self.value or other.value)).set_context(self.context),None
        return None,RuntimeError("Type Error",other.pos_start,other.pos_end)
    
    def notted(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context),None
    
    def is_true(self):
        return self.value != 0
   

        
#Context

class Context:
    def __init__(self,display_name,parent = None,parent_entry_pos = None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None


#symbols

class Symbols:
    def __init__(self):
        self.symbols = {}
        self.parent = None
    
    def get(self,name):
        value = self.symbols.get(name,None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value
    def set_var(self,name,value):
        self.symbols[name] = value

    def remove(self,name):
        del self.symbols[name]

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
    
    def visit_IfNode(self,node,context):
        response = CheckInterpreterResult()
        for condition,expr in node.cases:
            condition_val = response.register(self.visit(condition,context))

            if response.error:
                return response
            if condition_val.is_true():
                expression_val = response.register(self.visit(expr,context))
                if response.error:
                    return response
                return response.success(expression_val)
        if node.else_case:
            expression_val = response.register(self.visit(node.else_case,context))
            if response.error:
                return response
            return response.success(expression_val)
        return response.success(None)
    
    def visit_ForNode(self,node,context):
        response = CheckInterpreterResult()
        start_val = response.register(self.visit(node.start_val,context))
        if response.error:return response

        end_val = response.register(self.visit(node.end_val,context))
        if response.error:return response

        if node.step_val:
            step_val = response.register(visit(node.step_val,context))
            if response.error:return response
        else:
            step_val = Number(1)
        
        i = start_val.value
        
        if step_val.value >= 0:
            condition = lambda : i < end_val.value
        else:
            condition = lambda : i > end_val.value
        
        while condition():
            context.symbol_table.set_var(node.var_name_token.value,Number(i))
            i += step_val.value

            response.register(self.visit(node.bodyNode,context))
            if response.error:
                return response
        return response.success(None)
    
    def visit_WhileNode(self,node,context):
        response = CheckInterpreterResult()
        
        while True:
            condition = response.register(self.visit(node.condition_node,context))
            if response.error:
                return response
            if not condition.is_true():
                break
            response.register(self.visit(node.bodyNode,context))
            if response.error:
                return response
        return response.success(None)



    
    def visit_VarAccessNode(self,node,context):
        response = CheckInterpreterResult()
        var_name = node.var_name_token.value
        value = context.symbol_table.get(var_name)

        if not value:
            return response.failure(RuntimeError(f"{var_name} not defined",node.pos_start,node.pos_end,context))
        value = value.copy().set_pos(node.pos_start,node.pos_end)
        return response.success(value)
    
    def visit_VarAssignNode(self,node,context):
        response = CheckInterpreterResult()
        var_name = node.name_token.value
        value = response.register(self.visit(node.value_node,context))
        if response.error:
            return response
        context.symbol_table.set_var(var_name,value)
        return response.success(value)


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
        
        elif node.token.type == T_DOBEQUAL:
            result,error = left.equal_to(right) 
        elif node.token.type == T_NOTEQUAL:
            result,error = left.not_equal_to(right)
        elif node.token.type == T_GREATERTHEN:
            result,error = left.greater_than(right)
        elif node.token.type == T_LESSTHEN:
            result,error = left.lesser_than(right)
        elif node.token.type == T_GREATEREQUALTHEN:
            result,error = left.greater_than_equal(right)
        elif node.token.type == T_LESSEREQUALTHEN:
            result,error = left.lesser_than_equal(right)
        elif node.token.matches(T_KEYWORD,K_AND):
            result,error = left.anded(right)
        elif node.token.matches(T_KEYWORD,K_OR):
            result,error = left.ored(right)
        print(node.token)
        
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
        if node.operator.matches(T_KEYWORD,K_NOT):
            number,error = number.notted()
        if error:
            return response.failure(error)
        else:
            return response.success(number.set_pos(node.pos_start,node.pos_end))
       

        
line = 'print "hello, world"'

T_IDENTIFIER = "IDENTIFIER"
T_KEYWORD = "KEYWORD"
T_EQUAL = "EQUAL"
LETTERS = "abcdefghijklmnopqrstuvwxyz" + "abcdefghijklmnopqrstuvwxyz".upper()
DIGITS = "0123456789"
ALPHANUM = LETTERS + DIGITS
T_INT = "INT"
T_FLOAT = "FLOAT"
T_PLUS = "PLUS"
T_MINUS ="MINUS"
T_MUL = "MUL"
T_POW = "POW"
T_DIV = "DIV"
T_RPARM = "RPARM"
T_LPARM = "LPARM"
T_EOF = "EOF"

T_DOBEQUAL = "DOUBLE_EQUAL"
T_NOTEQUAL = "NOT_EQUAL"
T_GREATERTHEN = "GREATER_THEN"
T_LESSTHEN = "LESS_THEN"
T_GREATEREQUALTHEN = "GREATER_EQUAL_THEN"
T_LESSEREQUALTHEN = "LESSER_EQUAL_THEN"


K_NULL = "null"
K_TRUE = "true"
K_FALSE = "false"

K_VAR = "VAR"
K_AND = "AND"
K_OR = "OR"
K_NOT = "NOT"
K_IF = "IF"
K_ELSE = "ELSE"
K_THEN = "THEN"
K_ELIF = "ELIF"

K_FOR = "FOR"
K_TO = "TO"
K_WHILE = "WHILE"
K_STEP = "STEP"





KEYWORDS = [
    K_VAR,
    K_AND,
    K_OR,
    K_NOT,
    K_IF,
    K_THEN,
    K_ELIF,
    K_ELSE,

    K_STEP,
    K_TO,
    K_WHILE,
    K_FOR
    

]
#ERRORS

class Error:
    def __init__(self,error_name,details,atstart,atend):
        self.error = error_name
        self.atstart = atstart
        self.atend = atend
        self.details = details

    
    def stringfy(self):
        result = f"{self.error}: {self.details}"
        result += f"\nFile {self.atstart.file_name}, at line {self.atstart.line_no + 1}\n"
        result += self.extrabit()
        return result
    
    def extrabit(self):
        file_content = self.atstart.file_content
        ourline = "\n  " + file_content.split("\n")[self.atstart.line_no] 
        errorlen = self.atend.column_no - self.atstart.column_no

        line2  ="\n  " + " " * self.atstart.column_no + "^" * errorlen + " here maybe?"

        return ourline + line2 + "\n"

#TOKENS
class Token:
    def __init__(self,type_,value = None,pos_start = None,pos_end = None):
        self.type = type_
        self.value = value
        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = self.pos_start.copy()
            self.pos_end.updata_position()
        if pos_end:
            self.pos_end = pos_end.copy()
    
    def matches(self,type_,value):
        return self.type == type_ and self.value == value

    



    def __repr__(self):
        if self.value:
            return f"{self.type}:{self.value}"
        else:
            return self.type


#POSITIONS

class WHEREAMI:
    def __init__(self,exact_position,line_no,column_no,file_name,file_content):
        self.exact_position = exact_position
        self.line_no = line_no
        self.column_no = column_no
        self.file_content = file_content
        self.file_name = file_name
    
    def updata_position(self,char = None):
        self.exact_position += 1
        self.column_no += 1
        if char == "\n":
            self.line_no += 1
            self.column_no = 0

        return self
    
    def copy(self):
        return WHEREAMI(self.exact_position,self.line_no,self.column_no,self.file_name,self.file_content)

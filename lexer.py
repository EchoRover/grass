
line = 'print "hello, world"'
DIGITS = "0123456789"
T_INT = "INT"
T_FLOAT = "FLOAT"
T_PLUS = "PLUS"
T_MINUS ="MINUS"
T_MUL = "MUL"
T_DIV = "DIV"
T_RPARM = "RPARM"
T_LPARM = "LPARM"

# ERRORS 
class Error:
    def __init__(self,error_name,details,atstart,atend):
        self.error = error_name
        self.atstart = atstart
        self.atend = atend
        self.details = details
    
    def stringfy(self):
        result = f"{self.error}:{self.details}"
        result += f"\nFile {self.atstart.file_name}, at line {self.atstart.line_no + 1}"
        return result


class IllegalCharError(Error):
    def __init__(self,details,error_start_cursor,error_end_cursor):
        super().__init__('Illegal Charater',details,error_start_cursor,error_end_cursor)

#TOKENS
class Token:
    def __init__(self,type_,value = None):
        self.type = type_
        self.value = value
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
    
    def updata_position(self,char):
        self.exact_position += 1
        self.column_no += 1
        if char == "\n":
            self.line_no += 1
            self.column_no = 0

        return self
    
    def copy(self):
        return WHEREAMI(self.exact_position,self.line_no,self.column_no,self.file_name,self.file_content)


#LEXER

class Lexer:
    def __init__(self,string,filename):
        self.string = string
        self.cursor = WHEREAMI(exact_position = -1,line_no = 0,column_no = -1,file_name = filename,file_content = string)
        self.current_char = None
        self.next_char()

    
    def next_char(self):
        self.cursor.updata_position(self.current_char)
        self.current_char = self.string[self.cursor.exact_position] if self.cursor.exact_position < len(self.string) else None


    
    
    def tokeniser(self):
        tokens = []
        while self.current_char != None:
            if self.current_char in " \t":
                pass
                
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
                

            elif self.current_char in "+-/*()":
                match self.current_char:
                    case "+":
                        tokens.append(Token(T_PLUS))
                    case "-":
                        tokens.append(Token(T_MINUS))
                    case "*":
                        tokens.append(Token(T_MUL))
                    case "/":
                        tokens.append(Token(T_DIV))
                    case ")":
                        tokens.append(Token(T_LPARM))
                    case "(":
                        tokens.append(Token(T_RPARM))
                
            
            else:
                error_start_cursor = self.cursor.copy()
                char = self.current_char
                self.next_char()
                return [],IllegalCharError(f'[ {char} ]',error_start_cursor,self.cursor)



            self.next_char()
        
        return tokens,None
    
    def make_number(self):
        number = ''
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + ".":
            if self.current_char == ".":
                if dot_count == 1:
                    break
                else:
                    dot_count += 1
        
                number += "."
           
            
            else:
                number += self.current_char
            
            self.next_char()
        if dot_count == 0:
            return Token(T_INT,int(number))
        else:
            return Token(T_FLOAT,float(number))





        

        

from globaltools import *

# ERRORS 

class IllegalCharError(Error):
    def __init__(self,details,error_start_cursor,error_end_cursor):
        super().__init__('Illegal Charater',details,error_start_cursor,error_end_cursor)
class ExceptedCharError(Error):
    def __init__(self,details,error_start_cursor,error_end_cursor):
        super().__init__('Expected Charater',details,error_start_cursor,error_end_cursor)



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
                continue

            elif self.current_char in ALPHANUM + "_":
                tokens.append(self.make_identifier())
                continue
            

                

            elif self.current_char in "+-/*()^=><!":
                match self.current_char:
                    case "+":
                        tokens.append(Token(T_PLUS,pos_start = self.cursor ))
                    case "-":
                        tokens.append(Token(T_MINUS,pos_start = self.cursor))
                    case "*":
                        tokens.append(Token(T_MUL,pos_start = self.cursor))
                    case "^":
                        tokens.append(Token(T_POW,pos_start = self.cursor))
                    case "/":
                        tokens.append(Token(T_DIV,pos_start = self.cursor))
                    case ")":
                        tokens.append(Token(T_RPARM,pos_start = self.cursor))
                    case "(":
                        tokens.append(Token(T_LPARM,pos_start = self.cursor))
                    case "=":
                        tokens.append(self.checkdouble(next_char = "=",othertoken =T_DOBEQUAL,def_token = T_EQUAL))
                        continue
                    case ">":
                        tokens.append(self.checkdouble(next_char = "=",othertoken =T_GREATEREQUALTHEN,def_token = T_GREATERTHEN))
                        continue
                    case "<":
                        tokens.append(self.checkdouble(next_char = "=",othertoken =T_LESSEREQUALTHEN,def_token = T_LESSTHEN))
                        continue
                    case "!":
                        result = self.checkdouble(next_char = "=",othertoken = T_NOTEQUAL,def_token = None)
                        if type(result) != Token:
                            return None,ExceptedCharError(" = (after !)",result,self.cursor)
                        tokens.append(result)
                        continue
                
                
                
            
            else:
                error_start_cursor = self.cursor.copy()
                char = self.current_char
                self.next_char()
                return [],IllegalCharError(f'[ {char} ]',error_start_cursor,self.cursor)



            self.next_char()
        tokens.append(Token(T_EOF,pos_start = self.cursor))
        return tokens,None
    
    def checkdouble(self,next_char,othertoken,def_token):
        start = self.cursor.copy()
        self.next_char()
        if self.current_char != None and self.current_char == next_char:
            end = self.cursor.copy()
            self.next_char()
            return Token(othertoken,pos_start = start,pos_end = end)
        else:
            if not def_token: return start
            return Token(def_token,pos_start = start)
    
    def make_number(self):
        number = ''
        dot_count = 0
        start = self.cursor.copy()

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
        end = self.cursor.copy()
        if dot_count == 0:
            return Token(T_INT,int(number),pos_start  = start,pos_end = end)
        else:
            return Token(T_FLOAT,float(number),pos_start = start,pos_end = end)
    
    def make_string(self):
        string = ""
        start = self.cursor.copy()

        while self.current_char != None and self.current_char in ALPHANUM + "_":
            ...
    
    def make_identifier(self):
        id_str = ""
        start = self.cursor.copy()

        while self.current_char != None and self.current_char in ALPHANUM + "_":
            id_str += self.current_char
            self.next_char()
        if id_str in KEYWORDS:
            return Token(T_KEYWORD,id_str,pos_start = start,pos_end = self.cursor.copy())
        return Token(T_IDENTIFIER,id_str,pos_start = start,pos_end = self.cursor.copy())
         
        







        

        

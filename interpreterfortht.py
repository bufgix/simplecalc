INTEGER = "INTEGER"
PLUS = "PLUS"
MINUS = "MINUS"
EOF = "EOF"      #EOF(End Of File) girilen 
                 #ifadenin bittigini anlayacagiz

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return "<Token(type = {}, value = {})>".format(self.type,
        	                                             self.value)

    def __str__(self):
        return self.__repr__()
        

class Interpreter(object):
    def __init__(self, text):
        self.text = text  #Gelen veri
        self.pos = 0      #Imlec gibi dusunulebilir
        self.current_token = None      #O anki Token i tutacak
        
        self.current_char = self.text[self.pos] # Su an bulunulan 
                                                #karakter
                                                
    def error(self):
        raise Exception("Error parsing input")
        
    def advice(self):
        self.pos += 1       
        if self.pos > len(self.text) - 1:   #Ifadenin sonuna gelinirse
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]   #Degeri bul!
            
    def skip_whitespace(self):
        """  Bosluk karakterlerini gecmek icin """
        while self.current_char is not None and self.current_char.isspace():
            self.advice()
    
    def integer(self):
        """ 1 ve daha fazla haneli sayi alabilmemiz icin"""
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advice()
        return int(result)
    
    def get_next_token(self):
        """
        LEXER: bu kod verilen ifadenin parcalanmasindan
        sorumludur. buna 'Sozculsel Analiz' denir.
        """
        while self.current_char is not None:          
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char.isdigit():
                token = Token(INTEGER, self.integer())
                print token
                return token
            
            if self.current_char == '+':
                token = Token(PLUS, '+')
                print token
                self.advice()
                return token
            
            if self.current_char == '-':
                token = Token(MINUS, '-')
                print token
                self.advice()
                return token
            
            self.error()
        return Token(EOF,None)
    
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()
            
    def expr(self):
        """Parser / Interpreter

        expr -> INTEGER PLUS INTEGER
        expr -> INTEGER MINUS INTEGER
        """
        # Ilm tokenimizi alalim
        self.current_token = self.get_next_token()

        # istedigimiz token bir INTEGER ise
        left = self.current_token
        self.eat(INTEGER)

        # oparotor + veya - 
        op = self.current_token
        if op.type == PLUS:
            self.eat(PLUS)
        else:
            self.eat(MINUS)

        # oparatorden sonra gelen bir sayi ise
        right = self.current_token
        self.eat(INTEGER)
        # bundan sonra cagirilacak token:
        # EOF token
        
        if op.type == PLUS:
            result = left.value + right.value
        else:
            result = left.value - right.value
        return result
            


if __name__ == '__main__':
    while True:
        text = raw_input('Interpreter> ')
        if not text:
            continue
        inter = Interpreter(text)
        print inter.expr()

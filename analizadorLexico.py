r'''
#mclexer.py
El papel de un analizador léxico es convertir texto sin procesar en símbolos 
reconocidos conocidos como tokens.

Se requiere que el analizador léxico de MiniC reconozca los siguientes 
símbolos. El nombre sugerido del token está a la izquierda. El texto 
coincidente está a la derecha.


Palabras Reservadas:
    STATIC  : 'static'
    EXTERN  : 'extern'
    INT     : 'int'
    FLOAT   : 'float'
    CHAR    : 'CHAR'
    CONST   : 'const'
    RETURN  : 'return'
    BREAK   : 'break'
    CONTINUE: 'continue'
    IF      : 'if'
    ELSE    : 'else'
    WHILE   : 'while'
    FOR     : 'for'
    TRUE    : 'true'
    FALSE   : 'false'

Identificadores:
    ID      : Texto iniciando con una letra o '_' seguido de cualquier 
            número de letras, digitos o '_'. 
            Ejemplo: 'abc' 'ABC' 'abc123' '_abc' 'a_b_c'

Literales:
    INUMBER : 123 (decimal)

    FNUMBER : 1.234
            .1234
            1234.

    CHARACTER:'a' (un solo caracter - byte)
            '\xhh' (valor byte)
            '\n' (newline)
            '\'' (literal comilla simple)

    STRING  : "cadena" (varios caracteres entre comilla doble)
        permite secuenciads de escape como: '\n', '\t\, etc..

Asignadores
    ASSIGN : '='
    PLUS_ASSIGN :'+='
    MINUS_ASSIGN : '-='
    TIMES_ASSIGN : '\*='
    DIVIDE_ASSIGN : '/='
    MODULO_ASSIGN : '%='

Operadores:
    PLUS    : '+'
    MINUS   : '-'
    TIMES   : '*'
    DIVIDE  : '/'
    LT      : '<'
    LE      : '<='
    GT      : '!
    GE      : '>='
    EQ      : '=='
    NE      : '!='
    LAND    : '&&'
    LOR     : '||'
    LNOT    : '!'

Simbolos Miselaneos
    ASSIGN  : '='
    SEMI    : ';'
    LPAREN  : '('
    RPAREN  : ')'
    LBRACE  : '{'
    RBRACE  : '}'
    COMMA   : ','

Comentarios: Deben ser ignorados
    //          Ignora el resto de la linea
    /* ... */   Ignora un bloque (no se permite anidar)

Errores: Su lexer puede opcionalmente reconocer e informar los siguientes 
mensajes de error:

    lineno: character 'c' ilegal
    lineno: constante de caracter no terminada
    lineno: comentario sin terminar

'''

from sly import Lexer

class C_Lexer(Lexer):
    # Nombre de los tokens
    tokens = {
        #*IDENTIFICADOR
        ID, 
        #*LITERALES
        INUMBER, FNUMBER, CHARACTER, STRING,
        #*SIMBOLOS ESPECIALES
        PLUS, MINUS, TIMES, DIVIDE, MODULO,
        #*ASIGANDORES
        ASSIGN, PLUS_ASSIGN, MINUS_ASSIGN, TIMES_ASSIGN, DIVIDE_ASSIGN, MODULO_ASSIGN,
        INCREMENT, DECREMENT,
        #*OPERADORES ARITMETICOS Y LOGICOS
        EQ, NE, LT, GT, LE, GE,LAND, LOR, LNOT, AMPERSAND,
        #*SIMBOLOS MISELANEOS
        LPAR, RPAR, LBRACKET, RBRACKET, LBRACE, RBRACE,COMMA, SEMICOLON,
        #*PALABRAS RESERVADAS
        STATIC,EXTERN,INT,FLOAT,CHAR,DOUBLE,RETURN,BREAK,CONTINUE,IF,ELSE,WHILE,FOR,DO,VOID,ELLIPSIS
    }
    
    #!Expresiones regulares para los tokens
    #!Hay que tener encuenta que el orden importa
    
    #Identificador
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    
    @_(r'/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/')
    def cuenta_b(self,t):
        self.lineno += 1

    @_(r'//.*\n')
    def cuenta_lin(self,t):
        self.lineno += 1

    @_(r'\n+')
    def cuenta_nl(self,t):
        self.lineno += 1

    # Ignorar comentarios en bloque
    ignore_blockcomment = r'/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/'
    # Ignorar comentarios de linea
    ignore_linecomment = r'//.*\n'
    # Ignorar caracteres en blanco
    ignore_tab = r'\t+'
    ignore_carr = r'\r+'
    ignore_esp = r' '
    # Salto de linea
    ignore_newline = r'\n+'
    
    #Palabras reservadas
    ID['static'] = STATIC
    ID['extern'] = EXTERN
    ID['int']    = INT
    ID['float']  = FLOAT
    ID['char']   = CHAR
    ID['double'] = DOUBLE
    ID['return'] = RETURN
    ID['break'] = BREAK
    ID['continue'] = CONTINUE
    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE
    ID['for'] = FOR
    ID['do'] = DO
    ID['void'] = VOID
    
    #Literales
    FNUMBER = r'([0-9]*\.[0-9]+)|([0-9]+\.[0-9]*)'
    INUMBER = r'\d+'
    CHARACTER = r"'(\\.|[^'])+'"
    STRING = r'"(\\.|[^"])*"'

    #Operadores
    LE = r'<='
    EQ = r'=='
    NE = r'!='
    LT = r'<'
    GT = r'>'
    GE = r'>='
    LAND = r'&&'
    LOR = r'\|\|'
    LNOT = r'!'
    AMPERSAND = r'&'
    ELLIPSIS = r'\.\.\.'
    
    #Asignadores
    ASSIGN = r'='
    PLUS_ASSIGN = r'\+='
    MINUS_ASSIGN = r'-='
    TIMES_ASSIGN = r'\*='
    DIVIDE_ASSIGN = r'/='
    MODULO_ASSIGN = r'%='
    INCREMENT = r'\+\+'
    DECREMENT = r'--'

    #Simbolos especiales
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    MODULO = r'%'

    #Simbolos Miselaneos
    LPAR = r'\('
    RPAR = r'\)'
    LBRACKET = r'\['
    RBRACKET = r'\]'
    LBRACE = r'\{'
    RBRACE = r'\}'
    COMMA = r','
    SEMICOLON = r';'
    
    # Control de errores
    def error(self, t):
        print("Caracter Ilegal '%s'" % t.value[0])
        self.index += 1   

"""
with open('codigoC.c', 'r') as archivo:
    codigo_fuente = archivo.read()

lexer = C_Lexer()

for token in lexer.tokenize(codigo_fuente):
    print(token)
"""

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("msage: analizadorLexico.py codigoC.c")
        exit(1)

    lexer = C_Lexer()
    fuente = open(sys.argv[1], encoding='utf=8').read()

    for token in lexer.tokenize(fuente):
        print(token)
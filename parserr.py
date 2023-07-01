import sly
from analizadorLexico import C_Lexer
from const_ast import * 
from rich import print


class Parser(sly.Parser):
    debugfile = "sintaxis.txt"

    tokens = C_Lexer.tokens

    @_("translation_unit")
    def program(self, p):
        return translation_unit(p.translation_unit)

    @_("external_declaration")
    def translation_unit(self, p):
        return [ p.external_declaration ]

    @_("translation_unit external_declaration")
    def translation_unit(self, p):
        return p.translation_unit + [ p.external_declaration ]

    @_("function_definition",
       "declaration")
    def external_declaration(self, p):
        return p[0]

    @_("type_specifier declarator compound_statement")
    def function_definition(self, p):
        return f_definition(p.type_specifier, p.declarator, p.compound_statement)
    
    @_("STATIC type_specifier declarator compound_statement")
    def function_definition(self, p):
        return f_definition(p.type_specifier, p.declarator, p.compound_statement, static = True)

    @_("type_specifier declarator SEMICOLON")
    def declaration(self, p):
        return d_variables(p.type_specifier, p.declarator)

    @_("EXTERN type_specifier declarator SEMICOLON")
    def declaration(self, p):
        return d_variables(p.type_specifier, p.declarator, extern = True)

    @_("empty")
    def declaration_list_opt(self, p):
        return p.empty

    @_("declaration_list")
    def declaration_list_opt(self, p):
        return p.declaration_list

    @_("declaration")
    def declaration_list(self, p):
        return [ p.declaration ]

    @_("declaration_list declaration")
    def declaration_list(self, p):
        return p.declaration_list + [ p.declaration ]

    @_("INT", "FLOAT", "DOUBLE", "CHAR", "VOID")
    def type_specifier(self, p):
        return p[0]

    @_("direct_declarator")
    def declarator(self, p):
        return p.direct_declarator

    @_("TIMES declarator")
    def declarator(self, p):
        return unary(p[0], p.declarator)

    @_("ID")
    def direct_declarator(self, p):
        return variable(p[0])

    @_("direct_declarator LPAR parameter_type_list RPAR")
    def direct_declarator(self, p):
        return (p.direct_declarator, p.parameter_type_list)

    @_("direct_declarator LPAR RPAR")
    def direct_declarator(self, p):
        return (p.direct_declarator, )

    @_("parameter_list")
    def parameter_type_list(self, p):
        return l_parametros(p.parameter_list)

    @_("parameter_list COMMA ELLIPSIS")
    def parameter_type_list(self, p):
        return l_parametros(p.parameter_list, True)

    @_("parameter_declaration")
    def parameter_list(self, p):
        return p.parameter_declaration

    @_("parameter_list COMMA parameter_declaration")
    def parameter_list(self, p):
        return p.parameter_list, p.parameter_declaration

    @_("type_specifier declarator")
    def parameter_declaration(self, p):
        return parametros(p.type_specifier, p.declarator)

    @_("LBRACE declaration_list_opt statement_list RBRACE")
    def compound_statement(self, p):
        return compound(p.declaration_list_opt, p.statement_list)

    @_("LBRACE declaration_list_opt RBRACE")
    def compound_statement(self, p):
        return compound(decl = p.declaration_list_opt)

    @_("expression SEMICOLON")
    def expression_statement(self, p):
        return p.expression

    @_("equality_expression")
    def expression(self, p):
        return p.equality_expression

    @_("equality_expression ASSIGN expression",
        "equality_expression INCREMENT",
        "equality_expression DECREMENT",
        "equality_expression MINUS_ASSIGN expression",
        "equality_expression PLUS_ASSIGN expression",
        "equality_expression TIMES_ASSIGN expression",
        "equality_expression MODULO_ASSIGN expression",
        "equality_expression DIVIDE_ASSIGN expression")
    def expression(self, p):
        return binary(p[1], p.equality_expression, p.expression)

    @_("relational_expression")
    def equality_expression(self, p):
        return p.relational_expression

    @_("equality_expression EQ relational_expression",
       "equality_expression NE relational_expression")
    def equality_expression(self, p):
        return binary(p[1], p.equality_expression, p.relational_expression)

    @_("additive_expression")
    def relational_expression(self, p):
        return p.additive_expression
    
    @_("relational_expression LT additive_expression",
       "relational_expression LE  additive_expression",
       "relational_expression GT additive_expression",
       "relational_expression GE  additive_expression",
       "relational_expression LAND  additive_expression",
       "relational_expression LOR  additive_expression")
    def relational_expression(self, p):
        return binary(p[1], p.relational_expression, p.additive_expression) 

    @_("primary_expression")
    def postfix_expression(self, p):
        return p.primary_expression

    @_("postfix_expression LPAR argument_expression_list RPAR")
    def postfix_expression(self, p):
        return llamada(p.postfix_expression, p.argument_expression_list)

    @_("postfix_expression LPAR RPAR")
    def postfix_expression(self, p):
        return p.postfix_expression

    @_("postfix_expression LBRACKET expression RBRACKET")
    def postfix_expression(self, p):
        return llamada(p.postfix_expression, p.expression)

    @_("expression")
    def argument_expression_list(self, p):
        return [p.expression]

    @_("argument_expression_list COMMA expression")
    def argument_expression_list(self, p):
        return p.argument_expression_list + [p.expression]

    @_("postfix_expression")
    def unary_expression(self, p):
        return p.postfix_expression

    @_("MINUS unary_expression")
    def unary_expression(self, p):
        return unary(p[0], p.unary_expression)

    @_("PLUS unary_expression")
    def unary_expression(self, p):
        return unary(p[0], p.unary_expression)

    @_("LNOT unary_expression")
    def unary_expression(self, p):
        return unary(p[0], p.unary_expression)

    @_("TIMES unary_expression")
    def unary_expression(self, p):
        return unary(p[0], p.unary_expression)

    @_("AMPERSAND unary_expression")
    def unary_expression(self, p):
        return unary(p[0], p.unary_expression)

    @_("unary_expression")
    def mult_expression(self, p):
        return p.unary_expression

    @_("mult_expression TIMES unary_expression",
       "mult_expression DIVIDE unary_expression",
       "mult_expression MODULO unary_expression")
    def mult_expression(self, p):
        return binary(p[1], p.mult_expression, p.unary_expression)
    
    @_("mult_expression")
    def additive_expression(self, p):
        return p.mult_expression
    
    @_("additive_expression PLUS mult_expression",
       "additive_expression MINUS mult_expression")
    def additive_expression(self, p):
        return binary(p[0], p.additive_expression, p.mult_expression)

    @_("ID")
    def primary_expression(self, p):
        return variable(p[0])

    @_("FNUMBER")
    def primary_expression(self, p):
        return numero_f(p[0])

    @_("INUMBER")
    def primary_expression(self, p):
        return numero_i(p[0])

    @_("CHARACTER")
    def primary_expression(self, p):
        return caracter(p[0])

    @_("string_literal")
    def primary_expression(self, p):
        return cadena(p.string_literal)
    
    @_("LPAR expression RPAR")
    def primary_expression(self, p):
        return p[1]

    @_("STRING")
    def string_literal(self, p):
        return p[0]

    @_("string_literal STRING")
    def string_literal(self, p):
        return p.string_literal + p[0]

    @_("matched_statement",
       "open_statement")
    def statement(self, p):
        return p[0]

    @_("compound_statement",
       "expression_statement",
       "jump_statement")
    def simple_statement(self, p):
        return p[0]

    @_("RETURN SEMICOLON")
    def jump_statement(self, p):
        return rturn(p[0])

    @_("RETURN expression SEMICOLON")
    def jump_statement(self, p):
        return rturn(p.expression)
    
    @_("BREAK SEMICOLON")
    def jump_statement(self, p):
        return brk(p[0])
    
    @_("CONTINUE SEMICOLON")
    def jump_statement(self, p):
        return cont(p[0])

    @_("IF LPAR expression RPAR statement")
    def open_if(self, p):
        return ifcondicion(p.expression, p.statement)
    
    @_("IF LPAR expression RPAR matched_statement ELSE open_statement")
    def open_if(self, p):
        return ifelsecondicion(p.expression, p.matched_statement, p.open_statement)

    @_("IF LPAR expression RPAR matched_statement ELSE matched_statement")
    def matched_if(self, p):
        return ifelsecondicion(p.expression, p.matched_statement0, p.matched_statement1)

    @_("WHILE LPAR expression RPAR open_statement")
    def open_while(self, p):
        return whilebucle(p.expression, p.open_statement)
    @_("WHILE LPAR expression RPAR matched_statement")
    def matched_while(self, p):
        return whilebucle(p.expression, p.matched_statement)

    @_("DO matched_statement WHILE LPAR expression RPAR ")
    def matched_dowhile(self, p):
        return dowhilebucle(p.matched_statement, p.expression)

    @_("DO open_statement WHILE LPAR expression RPAR ")
    def open_dowhile(self, p):
        return dowhilebucle(p.open_statement, p.expression)

    @_("FOR LPAR expression_statement expression_statement expression RPAR open_statement")
    def open_for(self, p):
        return forbucle(p.expression_statement0, p.expression_statement1, p.expression, p.open_statement)

    @_("FOR LPAR expression_statement expression_statement expression RPAR matched_statement")
    def matched_for(self, p):
        return forbucle(p.expression_statement0, p.expression_statement1, p.expression, p.matched_statement)


    @_("matched_if",
        "matched_while",
        "matched_dowhile",
        "matched_for",
        "simple_statement")
    def matched_statement(self, p):
        return p[0]
    
    @_("open_if",
       "open_while",
       "open_dowhile",
       "open_for",
       )
    def open_statement(self, p):
        return p[0]
# --------------------------------------------------------------------

    @_("statement")
    def statement_list(self, p):
        return [ p.statement ]
    @_("statement_list statement")
    def statement_list(self, p):
        return p.statement_list + [ p.statement ]
    @_("")
    def empty(self, p):
        pass

    def error(self, p):
        
        lineno = p.lineno if p else 'EOF'
        value = p.value if p else 'EOF'
        print(f"{lineno}: Error de Sintaxis en {value}")

        #   raise SyntaxError()

# _______________________________________________


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print("msage: comp.py foo_lib.c")
        exit(1)

    l = C_Lexer()
    p = Parser()
    fuente = open(sys.argv[1], encoding='utf-8').read()

    ast = p.parse(l.tokenize(fuente))

    print(ast)


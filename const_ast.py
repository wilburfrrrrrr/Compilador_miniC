from dataclasses import dataclass, field
from multimethod import multimeta


################################################DEFINICIÓN DE NODOS DE AST###############################################
'''
**Participantes**
Stiven Cardona Salazar
Kevin Ossa Varela
'''

@dataclass
class visitor(metaclass = multimeta):
    pass

@dataclass
class nodo:
    def acepta(self, v: visitor, *args, **kwargs):
        return v.visit(self, *args, **kwargs)

@dataclass
class statement(nodo):
    pass

@dataclass
class expressions(nodo):
    pass

@dataclass
class declaration(statement):
    pass

#---------------------------------------------------Instrucciones--------------------------------------------------------

@dataclass
class translation_unit(statement):
    decl    : list[declaration] = field(default_factory = list)

@dataclass
class whilebucle(statement):
    cond    : expressions
    instr   : list[statement] = field(default_factory = list)

@dataclass
class dowhilebucle(statement):
    instr   : list[statement] 
    cond    : expressions

@dataclass
class forbucle(statement):
    ini     : statement
    expr    : expressions
    fin     : statement
    instr   : list[statement] = field(default_factory = list)

@dataclass
class ifcondicion(statement):
    cond    : expressions
    ins     : list[statement] = field(default_factory = list)

@dataclass
class ifelsecondicion(statement):
    cond    : expressions
    ins     : list[statement] = field(default_factory = list)
    els     : list[statement] = field(default_factory = list)

@dataclass
class rturn(statement):
    expr    : expressions

@dataclass
class brk(statement):
    arg     : str

@dataclass
class cont(statement):
    arg     : str

@dataclass
class null(statement):
    vacio   : statement

@dataclass
class expres_stmnt(statement):
    expr    : expressions
    ins     : statement

@dataclass
class compound(statement):
    decl    : list[declaration] = field(default_factory= list)
    inst    : list[statement] = field(default_factory=list)
    



#---------------------------------------------------Declaraciones--------------------------------------------------------

@dataclass
class parametros(declaration):
    type    : str
    nombre  : str

@dataclass
class l_parametros(declaration):
    params  : list[parametros] = field(default_factory = list)
    ellipsis: bool = False

@dataclass
class f_definition(declaration):
    type    : str
    nombre  : str
    params  : l_parametros
    stmnts  : compound = field(default_factory = list)
    static  : bool = False
    extern  : bool = False

@dataclass
class d_variables(declaration):
    type    : str
    nombre  : str
    exp     : expressions = None
    static  : bool = False
    extern  : bool = False


#-------------------------------------------------------Expresiones----------------------------------------------------------------
    
@dataclass
class binary(expressions):
    op      : str
    left    : expressions
    right   : expressions

@dataclass
class unary(expressions):
    op      : str
    expr    : expressions

@dataclass
class variable(expressions):
    nombre   : str

@dataclass
class llamada(expressions):
    funcion : str
    exp     : list[expressions] 

@dataclass
class constante(expressions):
    nombre    : str

@dataclass
class numero_i(expressions):
    type    : str = field(init=False, default = 'int')
    nombre  : int

@dataclass
class numero_f(expressions):
    type    : str = field(init=False, default = 'float')
    nombre  : float

@dataclass
class caracter(expressions):
    type    : str = field(init=False, default = 'char')
    nombre  : str

@dataclass
class cadena(expressions):
    type    : str = field(init=False, default = 'char*')
    nombre  : str
import graphviz as grp
from const_ast import *
from parserr import Parser
from analizadorLexico import C_Lexer

from _collections_abc import Iterable
from rich import print
import pydot


#####################################################RENDERIZADOR DEL AST###############################

class renderAST(visitor):
	node_default = {
		'shape' : 'box',
		'color' : 'deepskyblue',
		'style' : 'filled',
	}

	edge_defaults = {
		'arrowhead' : 'none'
	}

	color = 'chartreuse'

	def __init__(self):
		self.dot = grp.Digraph('AST', comment='AST para Mini C')
		self.dot.attr('node', **self.node_default)
		self.dot.attr('edge', **self.edge_defaults)
		self.seq = 0
    	

	def id(self):
		self.seq += 1
		return f"n{self.seq:02d}"

	@classmethod
	def render(cls, n: nodo):
		dot = cls()
		n.acepta(dot)
		return dot.dot

#------------------------------------------------------------PATRÓN VISITANTE PARA INSTRUCCIONES


	def visit(self, n: translation_unit):
		name = self.id()
		self.dot.node(name, label = f"Traduccion")
		if n.decl is not None:
			for dec in n.decl:
				if isinstance(dec, Iterable):
					for d in dec:
						self.dot.edge(name, d.acepta(self))
				else:
					self.dot.edge(name, dec.acepta(self))
		return name

	def visit(self, n: whilebucle):
		name = self.id()
		self.dot.node(name, label = f"While")
		self.dot.edge(name, n.cond.acepta(self))
		if isinstance(n.instr, Iterable):
			for ins in n.instr:
				if isinstance(ins, Iterable):
					for i in ins:
						self.dot.edge(name, i.acepta(self))
				else:
					self.dot.edge(name, ins.acepta(self))
		else: 
			self.dot.edge(name, n.instr.acepta(self))
		return name

	def visit(self, n: dowhilebucle):
		name = self.id()
		self.dot.node(name, label = f"Do While")
		if isinstance(n.instr, Iterable):
			for ins in n.instr:
				if isinstance(ins, Iterable):
					for i in ins:
						self.dot.edge(name, i.acepta(self))
				else:
					self.dot.edge(name, ins.acepta(self))
		else:
			self.dot.edge(name, n.instr)
		self.dot.edge(name, n.cond.acepta(self))
		return name
	
	def visit(self, n: forbucle):
		name = self.id()
		self.dot.node(name, label = f"For")
		self.dot.edge(name, n.ini.acepta(self))
		self.dot.edge(name, n.expr.acepta(self))
		self.dot.edge(name, n.fin.acepta(self))
		if isinstance(n.instr, Iterable):
			for ins in n.instr:
				if isinstance(ins, Iterable):
					for i in ins:
						self.dot.edge(name, i.acepta(self))
				else:
					self.dot.edge(name, ins.acepta(self))
		else:
			self.dot.edge(name, n.instr.acepta(self))
		return name

	def visit(self, n: ifcondicion):
		name = self.id()
		self.dot.node(name, label = f"If")
		self.dot.edge(name, n.cond.acepta(self))
		if isinstance(n.ins, Iterable):
			for i in n.ins:
				if isinstance(i, Iterable):
					for e in i:
						self.dot.edge(name, e.acepta(self))
				else:
					self.dot.edge(name, i.acepta(self))
		else:
			self.dot.edge(name, n.ins.acepta(self))
		return name
	
	def visit(self, n: ifelsecondicion):
		name = self.id()
		self.dot.node(name, label = f"If + Else")
		self.dot.edge(name, n.cond.acepta(self))
		if isinstance(n.ins, Iterable):
			for i in n.ins:
				if isinstance(i, Iterable):
					for e in i:
						self.dot.edge(name, e.acepta(self))
				else:
					self.dot.edge(name, i.acepta(self))
		else:
			self.dot.edge(name, n.ins.acepta(self))
		if isinstance(n.els, Iterable):
			for el in n.els:
				if isinstance(el, Iterable):
					for e in el:
						self.dot.edge(name, e.acepta(self))
				else:
					self.dot.edge(name, el.acepta(self))
		else:
			self.dot.edge(name, n.els.acepta(self))
		return name

	def visit(self, n: rturn):
		name = self.id()
		self.dot.node(name, label = f"Return")
		self.dot.edge(name, n.expr.acepta(self))
		return name

	def visit(self, n: brk):
		name = self.id()
		self.dot.node(name, label = f"Break \nop = '{n.arg}'")
		return name

	def visit(self, n: cont):
		name = self.id()
		self.dot.node(name, label = f"Continue \nop = '{n.arg}'")
		return name

	def visit(self, n: null):
		name = self.id()
		self.dot.node(name, label = f"Nulo")
		self.dot.edge(name, n.vacio.acepta(self))
		return name

	def visit(self, n: expres_stmnt):
		name = self.id()
		self.dot.node(name, label = f"Instrucción de expression")
		self.dot.edge(name, n.expr.acepta(self))
		self.dot.edge(name, n.ins.acepta(self))
		return name

	def visit(self, n: compound):
		name = self.id()
		self.dot.node(name, label = f"Compuesto")
		if n.decl is not None:
			if isinstance(n.decl, Iterable):
				for dec in n.decl:
					if isinstance(dec, Iterable):
						for d in dec:
							self.dot.edge(name, d.acepta(self))
					else:
						self.dot.edge(name, dec.acepta(self))
			else: 
				self.dot.node(name, n.decl.acepta(self))
		if isinstance(n.inst, Iterable):
			for ins in n.inst:
				if isinstance(ins, Iterable):
					for i in ins:
						self.dot.edge(name, i.acepta(self))
				else:
					self.dot.edge(name, ins.acepta(self))
		else:
			self.dot.edge(name, n.inst.acepta(self))
		return name

#-----------------------------------------------------PATRÓN VISITANTE PARA DECLARACIONES

	def visit(self, n: parametros):
		name = self.id()
		self.dot.node(name, label = f"Parametros \nTipo = '{n.type}' \nVar = '{n.nombre}'")
		self.dot.edge(name, n.nombre.acepta(self))
		return name
		
	def visit(self, n: l_parametros):
		name = self.id()
		self.dot.node(name, label = f"Lista de Parámetros")
		for par in n.params:
			self.dot.edge(name, par.acepta(self))
		self.dot.edge(name, n.ellipsis.acepta(self))
		return name

	def visit(self, n: f_definition):
		name = self.id()
		self.dot.node(name, label = f"Definición de funcion \nTipo = '{n.type}' \nNombre = '{n.nombre}'")		
		self.dot.edge(name, n.params.acepta(self))
		if isinstance(n.stmnts, Iterable):
			for st in n.stmnts:
				if isinstance(n.stmnts, Iterable):
					for s in st:
						self.dot.edge(name, s.acepta(self))
				else:
						self.dot.edge(name, st.acepta(self))
		else:
			self.dot.edge(n.stmnts.acepta(self))
		self.dot.edge(name, str(n.static))
		self.dot.edge(name, str(n.extern))
		return name

	def visit(self, n: d_variables):
		name = self.id()
		self.dot.node(name, label = f"Definición de variables \nTipo = '{n.type}' \nVar = {n.nombre}")
		if n.exp is not None:
			self.dot.edge(name, n.exp.acepta(self))
		self.dot.edge(name, str(n.static))
		self.dot.edge(name, str(n.extern))
		return name	


#-----------------------------------------------------PATRÓN VISITANTE PARA EXPRESIONES

	def visit(self, n: binary):
		name = self.id()
		self.dot.node(name, label = f"Operador Binario \nop = '{n.op}'")
		self.dot.edge(name, n.left.acepta(self))
		self.dot.edge(name, n.right.acepta(self))
		return name

	def visit(self, n: unary):
		name = self.id()
		self.dot.node(name, label = f"Operador Unario \nop = '{n.op}'")
		self.dot.edge(name, n.expr.acepta(self))
		return name

	def visit(self, n: variable):
		name = self.id()
		self.dot.node(name, label = f"Variable \nNombre = '{n.nombre}'")
		return name

	def visit(self, n: constante):
		name = self.id()
		self.dot.node(name, label = f"Constante \nNombre = '{n.nombre}'")
		return name

	def visit(self, n: llamada):
		name = self.id()
		self.dot.node(name, label = f"Llamada a función \nNombre = '{n.funcion}'")
		if isinstance(n.exp, Iterable):
			for expr in n.exp:
				self.dot.edge(name, expr.acepta(self))
		else:
			self.dot.edge(name, n.exp.acepta(self))
		return name

	def visit(self, n: caracter):
		name = self.id()
		self.dot.node(name, label = f"Char \nNombre = '{n.nombre}'")
		return name

	def visit(self, n: cadena):	
		name = self.id()
		self.dot.node(name, label = f"String \nNombre = '{n.nombre}'")
		return name

	def visit(self, n: numero_i):
		name = self.id()
		self.dot.node(name, label = f"Int \nNombre = '{n.nombre}'")
		return name

	def visit(self, n: numero_f):
		name = self.id()
		self.dot.node(name, label = f"Float \nNombre = '{n.nombre}'")
		return name



if __name__ == '__main__':
	import sys
	if len(sys.argv) != 2:
		print("msage: comp.py foo_lib.c")
		exit(1)


	lex = C_Lexer()
	par = Parser()
	ren = renderAST()
	fuente = open(sys.argv[1], encoding='utf=8').read()

	ast = par.parse(lex.tokenize(fuente))
	print(ast)
	arb = ren.render(ast)
	arb.save('arbol.dot')
	(imagen,) = pydot.graph_from_dot_file('arbol.dot')
	imagen.write_png('arbol.png')



	
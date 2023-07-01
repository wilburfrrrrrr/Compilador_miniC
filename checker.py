from _collections_abc import Iterable
from typing import Hashable
from tabulate import tabulate

from analizadorLexico import C_Lexer
from parserr import Parser
from const_ast import *
from rich import print


#------------------------------------------------------ANALIZADOR SEMÁNTICO
'''
**Participantes**
Stiven Cardona Salazar
Kevin Ossa Varela
'''


class tabla_s:

	def def_error(Exception):
		pass

	def __init__(self, padre: None):
		self.simbolos = {}
		self.padre = padre
		if self.padre:
			self.padre.hijo.append(self)
		self.hijo = []

	def agregar(self, nombre, valor):
		if nombre is Hashable:
			if nombre in self.simbolos:
				raise tabla_s.def_error()
			self.simbolos[nombre] = valor
		else:
			cade = str(nombre)
			if cade in self.simbolos:
				raise tabla_s.def_error()
			self.simbolos[cade] = valor


	def sacar(self, nombre):
		if nombre is Hashable:
			if nombre in self.simbolos:
				return self.simbolos[nombre]
			elif self.padre:
				return self.padre.sacar(nombre)
			return None
		else:
			cade = str(nombre)
			if cade in self.simbolos:
				return self.simbolos[cade]
			elif self.padre:
				return self.padre.sacar(cade)
			return None

	def __str__(self):
		return str(self.simbolos)
	
	def __iter__(self):
		return iter(self.simbolos.items())

class Checker(visitor):
	def agrega_simb(self, nodo, ent: tabla_s):
		try:
			ent.agregar(nodo.nombre, nodo)
		except tabla_s.def_error():
			self.error(f"simbolo '{nodo.nombre}' ya definido")
		

	@classmethod
	def check(cls, modelo):
		checker = cls()
		tabla = tabla_s(padre = None)
		modelo.acepta(checker, tabla)
		return tabla

#--------------------------------------------------------------DECLARACIONES

	def visit(self, nodo: parametros, ent: tabla_s):
		self.agrega_simb(self, ent)
		nodo.var.acepta(self, ent)

	def visit(self, nodo: l_parametros, ent: tabla_s):
		self.agrega_simb(nodo, ent)
		for par in nodo.params:
			par.acepta(self, ent)

	def visit(self, nodo: f_definition, ent: tabla_s):
		self.agrega_simb(nodo, ent)
		ent = tabla_s(ent)
		#Hacer una condición que verifique si el nodo es instancia de un compound
		if isinstance(nodo.params, Iterable):
			for par in nodo.params:
				if isinstance(nodo.params, compound):
					for d in par.decl:
						n_variable = d_variables(	type 	= d.type, 
													nombre 	= d.nombre, 
													exp 	= d.exp)
						self.agrega_simb(n_variable, ent)

				else:
				
						n_variable = d_variables(	type 	= par.type, 
													nombre 	= par.nombre, 
													exp 	= par.exp)
						self.agrega_simb(n_variable, ent)
		else:
			if isinstance(nodo.params, compound):
				if nodo.params.decl:
					for d in nodo.params.decl:
						n_variable = d_variables(	type 	= d.type, 
													nombre 	= d.nombre, 
													exp 	= d.exp)
						self.agrega_simb(n_variable, ent)
			else:
				n_variable = d_variables(	type 	= nodo.type, 
											nombre 	= nodo.params.nombre, 
											exp 	= nodo.params.exp)
				self.agrega_simb(n_variable, ent)
		if isinstance(nodo.stmnts, Iterable):
			for ins in nodo.stmnts:
				if isinstance(ins, Iterable):
					for i in ins:
						i.acepta(self, ent)
				else:
					ins.acepta(self, ent)
		else: 
			nodo.stmnts.acepta(self, ent)

	def visit(self, nodo: d_variables, ent: tabla_s):
		self.agrega_simb(nodo, ent)
		if nodo.exp:
			nodo.exp.acepta(self, ent)

#--------------------------------------------------------------INSTRUCCIONES

	def visit(self, nodo: translation_unit, ent: tabla_s):
		if nodo.decl is not None:
			for d in nodo.decl:
				if isinstance(d, Iterable):
					for dec in d:
						dec.acepta(self, ent)
				else:
					d.acepta(self, ent)

	def visit(self, nodo: whilebucle, ent: tabla_s):
		nodo.cond.acepta(self, ent)
		if isinstance(nodo.instr, Iterable):
			for ins in nodo.instr:
				if isinstance(ins, Iterable):
					for i in ins:
						i.acepta(self, ent)
				else:
					ins.acepta(self, ent)
		else:
			nodo.instr.acepta(self, ent)

	def visit(self, nodo: dowhilebucle, ent: tabla_s):
		if isinstance(nodo.instr, Iterable):
			for ins in nodo.instr:
				if isinstance(ins, Iterable):
					for i in ins:
						i.acepta(self, ent)
				else:
					ins.acepta(self, ent)
		else:
			nodo.instr.acepta(self, ent)
		nodo.cond.acepta(self, ent)

	def visit(self, nodo: forbucle, ent: tabla_s):
		nodo.ini.acepta(self, ent)
		nodo.expr.acepta(self, ent)
		nodo.fin.acepta(self, ent)
		if isinstance(nodo.instr, Iterable):
			for ins in nodo.instr:
				if isinstance(ins, Iterable):
					for i in ins:
						i.acepta(self, ent)
				else:
					ins.acepta(self, ent)
		else:
			nodo.instr.acepta(self, ent)

	def visit(self, nodo: ifcondicion, ent: tabla_s):
		nodo.cond.acepta(self, ent)
		if isinstance(nodo.ins, Iterable):
			for i in nodo.ins:
				if isinstance(i, Iterable):
					for e in i:
						e.acepta(self, ent)
				else:
					i.acepta(self, ent)
		else:
			nodo.ins.acepta(self, ent)

	def visit(self, nodo: ifelsecondicion, ent: tabla_s):
		nodo.cond.acepta(self, ent)
		if isinstance(nodo.ins, Iterable):
			for i in nodo.ins:
				if isinstance(i, Iterable):
					for e in i:
						e.acepta(self, ent)
				else:
					i.acepta(self, ent)
		else:
			nodo.ins.acepta(self, ent)
		if isinstance(nodo.els, Iterable):
			for el in nodo.els:
				if isinstance(el, Iterable):
					for e in el:
						e.acepta(self, ent)
				else:
					el.acepta(self, ent)
		else:
			nodo.els.acepta(self, ent)

	def visit(self, nodo: rturn, ent: tabla_s):
		nodo.expr.acepta(self, ent)

	def visit(self, nodo: brk, ent: tabla_s):
		pass

	def visit(self, nodo: cont, ent: tabla_s):
		pass

	def visit(self, nodo: null, ent: tabla_s):
		nodo.vacio.acepta(self, ent)

	def visit(self, nodo: expres_stmnt, ent: tabla_s):
		nodo.expr.acepta(self, ent)
		nodo.ins.acepta(self, ent)

	def visit(self, nodo: compound, ent: tabla_s):
		if isinstance(nodo.decl, Iterable):
			for d in nodo.decl:
				if isinstance(d, Iterable):
					for dec in d:
						dec.acepta(self, ent)
				else:
					d.acepta(self, ent)
		else:
			nodo.decl.acepta(self, ent)
		if isinstance(nodo.inst, Iterable):
			for i in nodo.inst:
				if isinstance(nodo.inst):
					for ii in i:
						ii.acepta(self, ent)
				else:
					i.acepta(self, ent)
		else:
			nodo.inst.acepta(self, ent)
		
#-------------------------------------------------------------VARIABLES		


	def visit(self, nodo: binary, ent: tabla_s):
		nodo.left.acepta(self, ent)
		nodo.right.acepta(self, ent)

	def visit(self, nodo: unary, ent: tabla_s):
		nodo.expr.acepta(self, ent)

	def visit(self, nodo: constante, ent: tabla_s):
		pass

	def visit(self, nodo: numero_i, ent: tabla_s):
		pass

	def visit(self, nodo: numero_f, ent: tabla_s):
		pass

	def visit(self, nodo: caracter, ent: tabla_s):
		pass

	def visit(self, nodo: cadena, ent: tabla_s):
		pass

	def visit(self, nodo: variable, ent: tabla_s):
		nom = ent.sacar(nodo.nombre)
		if nom is None:
			print(f'La variable {nodo.nombre} no está definida')

	def visit(self, nodo: llamada, ent: tabla_s):	
		func = ent.sacar(nodo.funcion)
		if func is not None:
			express = ent.sacar(nodo.exp)
			
			tam_e 	= sum(1 for _ in express)
			tam_ll 	= sum(1 for _ in nodo.exp)
			if tam_e == tam_ll:
#		nodo.funcion.acepta(self, ent)
				if isinstance(nodo.exp, Iterable):
					for ex in nodo.exp:
						ex.acepta(self, ent)
				else:
					nodo.exp.acepta(self, ent)
			else:
				print(f'Error en la llamada de la funcion {nodo.funcion}: Error en el número de argumentos')
		else:
			print(f'Error en la llamada de la funcion {nodo.funcion}: La función no está definida')
				
if __name__ == '__main__':
	import sys

	if len(sys.argv) != 2:
		print("msage: comp.py foo_lib.c")
		exit(1)

	l = C_Lexer()
	p = Parser()

	fuente 	= open(sys.argv[1], encoding='utf-8').read()
	ast 	= p.parse(l.tokenize(fuente))
	sim 	= Checker.check(ast)

	datos 		= [(str(nombre)[:40], str(valor)[:80]) for nombre, valor in sim.simbolos.items()]
	titulo 		= ["Nombre", "Valor"]
	tabla 		= tabulate(datos, titulo, tablefmt = 'psq1')

	print(tabla)
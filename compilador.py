import argparse
from contextlib	import redirect_stdout
from dataclasses import dataclass
from rich import print
import pydot
from tabulate import tabulate


from analizadorLexico import C_Lexer
from parserr import Parser
from render_ast import renderAST
from checker import Checker
from const_ast import *



#----------------------------------Patrón fachada para compilador

def parse_args():
	cli = argparse.ArgumentParser(
		prog='compilador.py',
		description='Compilador para programas en miniC'
	)

	cli.add_argument(
		'-v',
		'--version',
		action = 'version',
		version = '0.8'
	)

	fgrup = cli.add_argument_group('Opciones de formateo')
	fgrup.add_argument(
		'files',
		type = str,
		nargs = '+',
		help = 'Archivo de programa de miniC para compilar'
	)

	mutex = fgrup.add_mutually_exclusive_group()
	mutex.add_argument(
		'-l',
		'--lex',
		action = 'store_true',
		default = False,
		help =  'Guardado de output para lexer'
	)
	mutex.add_argument(
		'-d',
		'--dot',
		action = 'store_true',
		default = False,
		help = 'Genera una grafica AST en formato de .dot'
	)
	mutex.add_argument(
		'-p',
		'--p',
		action = 'store_true',
		help = 'Genera una grafica AST en formato.png'
	)
	mutex.add_argument(
		'--sym',
		action = 'store_true',
		help = 'Almacenamiento de tabla de simbolos'
	)

	return cli.parse_args()


if __name__ == '__main__':
	args = parse_args()
	
		
	if args.lex:
		for file in args.files:
			l = C_Lexer()

			fuente = open(file, encoding = 'utf-8').read() 
			tokens = l.tokenize(fuente)
			for t in tokens:
				print(t)
	
	if args.p:
		for file in args.files:
			fuente = open(file, encoding = 'utf-8').read() 
			l = C_Lexer()
			p = Parser()
			ren = renderAST()

			tokens = l.tokenize(fuente)
			ast = p.parse(tokens)
			arb = ren.render(ast)
			arb.save('arbol.dot')
			(imagen,) = pydot.graph_from_dot_file('arbol.dot')
			imagen.write_png('arbol.png')

	if args.dot:
		for file in args.files:
			l = C_Lexer()
			p = Parser()
			ren = renderAST()

			fuente = open(file, encoding = 'utf-8').read() 
			tokens = l.tokenize(fuente)
			ast = p.parse(tokens)
			dot = ren.render(ast)
			print(dot)
			
	if args.sym:
		for file in args.files:
			fuente 	= open(file, encoding='utf-8').read()
			l = C_Lexer()
			p = Parser()
			ast 	= p.parse(l.tokenize(fuente))
			sim 	= Checker.check(ast)

			datos 		= [(str(nombre)[:40], str(valor)[:80]) for nombre, valor in sim.simbolos.items()]
			titulo 		= ["Nombre", "Valor"]
			tabla 		= tabulate(datos, titulo, tablefmt = 'psq1')

			print(tabla)
	print(args.files)


#python compilador.py -l archivo.c

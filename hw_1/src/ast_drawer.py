import ast
import networkx as nx
from ast_visitor import AstVisitor


def draw_ast(input_src: str, output_src: str):
    with open(input_src, 'r') as file:
        program = file.read()
    program_ast = ast.parse(program)
    graph = nx.DiGraph()
    AstVisitor(graph).visit(program_ast)
    nx.drawing.nx_pydot.to_pydot(graph).write(output_src, format='png')

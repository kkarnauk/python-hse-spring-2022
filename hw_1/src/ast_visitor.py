import ast
import networkx as nx
from typing import Type


class AstVisitor:
    __nodes_colors: dict[Type[ast.AST], str] = {
        ast.Constant: '#F4E285',
        ast.arg: '#CBCBD4',
        ast.arguments: '#5B8E7D',
        ast.Sub: '#F4A259',
        ast.Add: '#885A89',
        ast.Name: '#D1B490',
        ast.Load: '#EE7B30',
        ast.Attribute: '#EAF7CF',
        ast.Assign: '#92828D',
        ast.Compare: '#CEB5A7',
        ast.BinOp: '#5FB49C',
        ast.Lt: '#414288',
        ast.Call: '#EE4B6A',
        ast.Subscript: '#F7F9F7',
        ast.UnaryOp: '#87919E',
        ast.List: '#F49390',
        ast.Module: '#C45AB3',
        ast.FunctionDef: '#6D7275',
        ast.Slice: '#ECEBF3',
        ast.USub: '#C0F5FA',
        ast.Store: '#BD8B9C',
        ast.While: '#B3DEC1',
        ast.Return: '#AC7B7D',
        ast.Expr: '#BD8B9C'
    }

    def __init__(self, graph: nx.DiGraph):
        self.__graph = graph
        self.__node_index = 0

    @staticmethod
    def __label(node: ast.AST) -> str:
        if isinstance(node, ast.Constant):
            return f"Constant '{node.value}'"
        if isinstance(node, ast.Name):
            return f"Name '{node.id}'"
        if isinstance(node, ast.arg):
            return f"Argument '{node.arg}'"
        if isinstance(node, ast.FunctionDef):
            return f"Function definition '{node.name}'"
        if isinstance(node, ast.Attribute):
            return f"Attribute '{node.attr}'"
        return node.__class__.__name__

    def __visit_impl(self, node: ast.AST) -> int:
        node_index = self.__node_index
        self.__node_index += 1
        self.__graph.add_node(
            node_index,
            style='filled',
            label=self.__label(node),
            color=self.__nodes_colors.get(node.__class__, '#BC4B51')
        )

        for name, value in ast.iter_fields(node):
            if isinstance(value, ast.AST):
                self.__graph.add_edge(node_index, self.__visit_impl(value))
            elif isinstance(value, list):
                for child_node in value:
                    if isinstance(child_node, ast.AST):
                        self.__graph.add_edge(node_index, self.__visit_impl(child_node))
        return node_index

    def visit(self, node: ast.AST):
        self.__visit_impl(node)

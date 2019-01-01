"""Development tools.

These are utility classes and functions used in the development process for new operations
and features. They are not used by the main program, and are not covered in standard testing.
"""
import ast


class NodeLister(ast.NodeVisitor):
    """Generic node listing tool to investigate operations on testing files.

    Use interactively by passing an AST e.g.

    >>> tree = mutatest.transformers.get_ast_from_src("somefile.py")
    >>> NodeLister().visit(tree)
    """

    def visit_FunctionDef(self, node):
        print(f"Function: {node.name}")
        print(ast.dump(node))
        self.generic_visit(node)

    def visit_BinOp(self, node):
        print(f"BinOP: {node}")
        print(ast.dump(node))
        self.generic_visit(node)

    def visit_If(self, node):
        print(f"If: {node}")
        print(ast.dump(node))
        self.generic_visit(node)

    def visit_Compare(self, node):
        print(f"Compare: {node}")
        print(ast.dump(node))
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        print(f"Bool: {node}")
        print(ast.dump(node))
        self.generic_visit(node)
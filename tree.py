"""
Class implementation of an n-ary tree with a tree-dictionary method that helps in creating a JSON tree file
Value is only stored when the node is a literal
"""

class tree(): 
    def __init__(self, node_type, value = None ):
        self.node_type = node_type 
        self.value = value 
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def to_dict(self):
        return {
            "Type": self.node_type,
            "Literal": self.value,  
            "children": [child.to_dict() for child in self.children]
        }
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

    # Need class method to make a tree since we didnt have one to begin with
    @classmethod 
    def from_json(cls, data): 
        """
        Method to convert our dictionary from to_dict into a tree
        """

        node = cls(data['Type'], data.get("Literal"))
        for child in data.get("children", []): 
            node.add_child(cls.from_json(child))

        return node 

    def to_sop(self): 

        if self.node_type == "Literal":
            return self.value

        if self.node_type == "AND":
            return "".join(child.to_sop() for child in self.children)

        if self.node_type == "OR":
            return " + ".join(child.to_sop() for child in self.children)

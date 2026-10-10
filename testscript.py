from Verilog import * 
from tree import tree

test1 = VerilogGen()

print(test1.helper(tree("Literal", "a'")))
print(test1.helper(tree('Literal', "a'")))   
print(test1.helper(tree('Literal', "b")))    
print(test1.gates)                           
print(test1.wires)                           

# Build OR( AND(a', b), c )
a_n = tree('Literal', "a'")
b   = tree('Literal', 'b')
c   = tree('Literal', 'c')
d   = tree('Literal', 'd')

and_node = tree('AND')
and_node.add_child(a_n)
and_node.add_child(b)
and_node.add_child(d)

root = tree('OR')
root.add_child(and_node)
root.add_child(c)

gen = VerilogGen()
result = gen.helper(root)

print("returned:", result)
print("gates:")
for g in gen.gates:
    print("  ", g)
print("wires:", gen.wires)

and_node = tree('AND')
and_node.add_child(tree('Literal', "a'"))
and_node.add_child(tree('Literal', 'b'))

root = tree('OR')
root.add_child(and_node)
root.add_child(tree('Literal', 'c'))

gen = VerilogGen()
gen.write(root, "out.v")
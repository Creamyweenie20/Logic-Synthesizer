from tree import tree
from Logic import *


class VerilogGen:
    def __init__(self):
        self.n = 0
        self.gates = []
        self.wires = []
        self.inverters = {}   
        self.inputs = set()

    def helper(self, node):
        if node.node_type == 'Literal':
            if node.value.endswith("'"):
                base = node.value[:-1]
                self.inputs.add(base)
                if base in self.inverters:
                    return self.inverters[base]
                out = base + '_n'
                gate = f'not g{self.n} ({out}, {base});'
                self.wires.append(out)
                self.inverters[base] = out
                self.n += 1 
                self.gates.append(gate)
                return out

            self.inputs.add(node.value)
            return node.value

        else:
            inputs = []
            for child in node.children:
                wires = self.helper(child)
                inputs.append(wires)

            if node.node_type == "AND":
                out = f'w{self.n}'
                gate = f'and g{self.n} ({out}, {", ".join(inputs)});'
                self.gates.append(gate)
                self.wires.append(out)
                self.n += 1 
                return out

            elif node.node_type == "OR":
                out = f'w{self.n}'
                gate = f'or g{self.n} ({out}, {", ".join(inputs)});'
                self.gates.append(gate)
                self.wires.append(out)
                self.n += 1 
                return out

    def write(self, root, path, module_name="top"):
        result = self.helper(root)
        if result in self.wires: 
            self.wires.remove(result)
        inputs = sorted(self.inputs)

        lines = [f'module {module_name} ({', '.join(inputs + [result])});']
        if inputs: 
            lines.append(f" input {', '.join(inputs)};")
        lines.append(f" output {result};")
        if self.wires:
            lines.append(f" wire {', '.join(self.wires)};")
        lines.append("")
        lines.extend(f" {g}" for g in self.gates)
        lines.append("endmodule")
        with open(path, "w") as f:
            f.write("\n".join(lines) + "\n")
        return result 
            
        

    
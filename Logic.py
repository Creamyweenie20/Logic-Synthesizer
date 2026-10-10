from tree import *
import re
import itertools
from Functions import *
import numpy as np

## Figure out if the prompt is needed because how would the text be displayed otherwise (worst case just put the display outside)
def parse_input(text):
    text = text.replace(' ', '')

    plus = text.split('+')
    OR = tree("OR")
    
    for p in plus: 
        if p == '':
            raise ValueError('Empty')
        AND = tree("AND")
        OR.add_child(AND)
        stripped = p.replace('*', '')
        multiply = re.findall(r"[A-Za-z][0-9]*'?", stripped)
        for m in multiply: 
            if m == '': 
                raise ValueError('Empty')
            node = tree("Literal", m)
            AND.add_child(node)

    return OR

def compute(node, truths):
    '''
    Truths should be a dictionary, we will loop over all possible combinations of literals later
    '''
    if node.node_type == 'Literal':
        if node.value.endswith("'"):
            name = node.value[:-1]
            return not truths[name]
        return truths[node.value]

    children = [compute(child, truths) for child in node.children]

    if node.node_type == "AND":
        return all(children)

    if node.node_type == "OR":
        return any(children)

def get_variables(node): 
    if node.node_type == "Literal": 
        return {node.value.replace("'", '')}
    variables = set()
    for child in node.children: 
        variables.update(get_variables(child))
    return variables

def can_sop(node):
    literals = sorted(get_variables(node))
    num = len(literals) 

    can_sop_terms = []

    for combination in itertools.product(range(2), repeat = num):
        truths = dict(zip(literals, combination)) 
        value = compute(node, truths)

        if value == True:
            term = ''
            for key, values in truths.items(): 
                if values == 0:
                    term += key + "'"
                else: 
                    term += key
            can_sop_terms.append(term)
    if not can_sop_terms: 
        return 'No Minterms' 
    return "+".join(can_sop_terms)

def inverse_can_sop(node): 
    literals = sorted(get_variables(node))
    num = len(literals) 

    can_sop_terms = []

    for combination in itertools.product(range(2), repeat = num):
        truths = dict(zip(literals, combination)) 
        value = compute(node, truths)

        if value == False:
            term = ''
            for key, values in truths.items(): 
                if values == 0:
                    term += key + "'"
                else: 
                    term += key
            can_sop_terms.append(term)
    if not can_sop_terms: 
        return 'No Minterms' 
    return "+".join(can_sop_terms)

def can_pos(node): 
    literals = sorted(get_variables(node))
    num = len(literals) 

    can_pos_terms = []

    for combination in itertools.product(range(2), repeat = num): 
        truths = dict(zip(literals, combination))
        value = compute(node, truths)

        if value == False: 
            term = []
            for key, values in truths.items():
                if values == 1: 
                    term.append(key + "'")
                else: 
                    term.append(key)
            can_pos_terms.append('(' + '+'.join(term) + ')')

    if not can_pos_terms: 
        return 'No Maxterms'
    return '*'.join(can_pos_terms)

def inverse_can_pos(node): 
    literals = sorted(get_variables(node))
    num = len(literals) 

    can_pos_terms = []

    for combination in itertools.product(range(2), repeat = num): 
        truths = dict(zip(literals, combination))
        value = compute(node, truths)

        if value == True: 
            term = []
            for key, values in truths.items():
                if values == 1: 
                    term.append(key + "'")
                else: 
                    term.append(key)
            can_pos_terms.append('(' + '+'.join(term) + ')')

    if not can_pos_terms: 
        return 'No Maxterms'
    return '*'.join(can_pos_terms)

def minimized_SOP(node): 
    literals = sorted(get_variables(node))
    num = len(literals) 
    
    minterms = []

    for combination in itertools.product(range(2), repeat = num):
        truths = dict(zip(literals, combination)) 
        value = compute(node, truths)

        if value == True:
            minterms.append(combination)
    ## Claude For the line below, makes tuples into a string of binary
    minterm_strings = [''.join(str(b) for b in t) for t in minterms]
    prime = getPrimeImplicants(minterm_strings)
    essential, chart = getEssentialPrimeImplicants(prime, minterm_strings) 
    minimized = petrickMethod(prime, minterm_strings)

    terms = []
    for pi in minimized:
        term = ''
        for bit, var in zip(pi, literals):
            if bit == '1':
                term += var
            elif bit == '0':
                term += var + "'"
        terms.append(term or '1')

    return ' + '.join(terms) if terms else '0'


##### BOOKMARK FOR CHANGE ######
def minimized_POS(node):
    literals = sorted(get_variables(node))
    num = len(literals)

    maxterm_strings = []
    for combination in itertools.product(range(2), repeat=num):
        truths = dict(zip(literals, combination))
        if not compute(node, truths):
            maxterm_strings.append(''.join(str(b) for b in combination))

    if not maxterm_strings:          
        return '1'

    prime = getPrimeImplicants(maxterm_strings)
    minimized = petrickMethod(prime, maxterm_strings)   

    sums = []
    for pi in minimized:
        sum_terms = []
        for bit, var in zip(pi, literals):
            if bit == '1':
                sum_terms.append(var + "'")   
            elif bit == '0':
                sum_terms.append(var)
        if not sum_terms:            
            return '0'
        sums.append('(' + ' + '.join(sum_terms) + ')')

    return ''.join(sums)

def prime_implicants(node): 
    literals = sorted(get_variables(node))
    num = len(literals) 
    
    minterms = []

    for combination in itertools.product(range(2), repeat = num):
        truths = dict(zip(literals, combination)) 
        value = compute(node, truths)

        if value == True:
            minterms.append(combination)
    ## Claude For the line below, makes tuples into a string of binary
    minterm_strings = [''.join(str(b) for b in t) for t in minterms]
    prime = getPrimeImplicants(minterm_strings)

    return prime, literals 

def essential_prime_implicants(node): 
    literals = sorted(get_variables(node))
    num = len(literals) 
    
    minterms = []

    for combination in itertools.product(range(2), repeat = num):
        truths = dict(zip(literals, combination)) 
        value = compute(node, truths)

        if value == True:
            minterms.append(combination)
    ## Claude For the line below, makes tuples into a string of binary
    minterm_strings = [''.join(str(b) for b in t) for t in minterms]
    prime = getPrimeImplicants(minterm_strings)
    essential, _ = getEssentialPrimeImplicants(prime, minterm_strings)

    return essential, literals

def on_set(node):
    literals = sorted(get_variables(node))
    num = len(literals) 

    minterms = []

    for combination in itertools.product(range(2), repeat = num):
        truths = dict(zip(literals, combination)) 
        value = compute(node, truths)

        if value == True:
            minterms.append(int(''.join(map(str,combination)), 2))

    return minterms, len(minterms)

def off_set(node):
    literals = sorted(get_variables(node))
    num = len(literals) 

    maxterms = []

    for combination in itertools.product(range(2), repeat = num):
        truths = dict(zip(literals, combination)) 
        value = compute(node, truths)

        if value == False:
            maxterms.append(int(''.join(map(str,combination)), 2))

    return maxterms, len(maxterms)

def truth_table(node):
    literals = sorted(get_variables(node))
    num = len(literals)
    truth_csv = np.array(literals)
    truth_csv = np.append(truth_csv, 'output')
    truth_table = '|'

    for i in literals: 
        truth_table += f' {i} |' 
    truth_table += ' out |'
    width = len(truth_table)
    truth_table += '\n' + '-' * (width + 6)
    truth_table += '\n' 

    for combination in itertools.product(range(2), repeat = num):
        truth_table += "|"
        for c in combination: 
            truth_table += f' {c} |'
        truths = dict(zip(literals, combination))
        value = compute(node, truths)
        row = np.append(combination, value)
        truth_csv = np.vstack([truth_csv, row])
        truth_table +=  f"   {int(value)}   |"
        truth_table += '\n' 
        truth_table += '-' * (width + 6) + "\n"

    np.savetxt("foo.csv", truth_csv, delimiter=',', fmt='%s')

    return truth_table
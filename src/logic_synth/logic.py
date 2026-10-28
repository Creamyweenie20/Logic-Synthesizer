"""
The functions below are used in the GUI's action buttons, i.e. they are related to the logic options that the user would wish to use
"""

from .tree import tree
from .functions import getPrimeImplicants, getEssentialPrimeImplicants, petrickMethod
import re
import itertools
import numpy as np


def parse_input(text):
    """ 
    Function to parse the SOP input and create a tree with operations as nodes, creating bottom up from literals 
    """

    text = text.replace(' ', '')
    plus = text.split('+')
    OR = tree("OR")
    
    for p in plus: 
        if p == '':
            # Will need to handle empty inputs in the future
            raise ValueError('Empty')
        
        AND = tree("AND")
        OR.add_child(AND)

        stripped = p.replace('*', '')
        # Find all inputs that might be in the form of xi: * for any number length put in (x12495), ? for recoginizing ' only once or nonce
        multiply = re.findall(r"[A-Za-z][0-9]*'?", stripped)
        for m in multiply: 
            if m == '': 
                raise ValueError('Empty')
            node = tree("Literal", m)
            AND.add_child(node)

    return OR

def compute(node, truths):
    '''
    Truths should be a dictionary, we will loop over all possible combinations via the itertools library.
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
    """
    Iterate over the nodes to get all the literals
    """

    if node.node_type == "Literal": 
        return {node.value.replace("'", '')}
    
    variables = set()

    for child in node.children: 
        variables.update(get_variables(child))

    return variables

def can_sop(node):
    """
    Computes the canonical SOP form by going through every possible input combination and tracking whether the literal was true or false
    """

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
    """
    Same as can_sop but does the operations based on the inverse truth values
    """

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
    """
    Calculates the canonical POS by the same process as the canonical SOP but with added string manipulation 
    """

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
    """
    Canonical POS but inversed 
    """

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
    """
    Returns the minimized SOP by utilizing the Quine-McCluskey algorithm and the PetrickMethod
    """

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
    # essential, chart = getEssentialPrimeImplicants(prime, minterm_strings) Wasn't used ?
    minimized = petrickMethod(prime, minterm_strings)

    terms = []
    # Loop to return the literals instead of the bit strings
    for pi in minimized:
        term = ''
        for bit, var in zip(pi, literals):
            if bit == '1':
                term += var
            elif bit == '0':
                term += var + "'"
        terms.append(term or '1')

    return ' + '.join(terms) if terms else '0'

def minimized_POS(node):
    """
    Returns the minimized POS form via the same process as the minimized_SOP function
    """

    literals = sorted(get_variables(node))
    num = len(literals)

    maxterm_strings = []
    for combination in itertools.product(range(2), repeat=num):
        truths = dict(zip(literals, combination))
        if not compute(node, truths):
            maxterm_strings.append(''.join(str(b) for b in combination))

    # Edge case for if there are no maxterms
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
        #Joing with to add literal terms while appending that inside parantheses 
        sums.append('(' + ' + '.join(sum_terms) + ')')

    return ''.join(sums)

def prime_implicants(node): 
    """
    Function used in logic to call the getPrimeImplicants function
    """
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
    """
    Funciton used to call getEssentialPrimeImplicants
    """
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
    """
    Returns the on_set in decimal form
    """
   
    literals = sorted(get_variables(node))
    num = len(literals) 

    minterms = []

    for combination in itertools.product(range(2), repeat = num):
        truths = dict(zip(literals, combination)) 
        value = compute(node, truths)

        if value == True:
            # Translates the binary into a decimal number
            minterms.append(int(''.join(map(str,combination)), 2))

    return minterms, len(minterms)

def off_set(node):
    """
    Returns the off_set in decimal form
    """

    literals = sorted(get_variables(node))
    num = len(literals) 

    maxterms = []

    for combination in itertools.product(range(2), repeat = num):
        truths = dict(zip(literals, combination)) 
        value = compute(node, truths)

        if value == False:
            maxterms.append(int(''.join(map(str,combination)), 2))

    return maxterms, len(maxterms)

def truth_table(node, csv_path = None):
    """
    Returns and prints a truth table in a csv and printed on the GUI, respectively
    """
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

    if csv_path:
        np.savetxt(csv_path, truth_csv, delimiter=',', fmt='%s')

    return truth_table
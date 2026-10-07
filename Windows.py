import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QGridLayout
)
from PySide6.QtGui import QGuiApplication
from tree import tree
from Functions import *

import numpy as np

import itertools
import re
import json

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
        QWidget {
            background-color: #222222;
            color: #ffffff;
        }

        QPushButton {
            background-color: #000000;
            color: white; 
            border: 1px solid #ffffff; 
            padding: 5px; 
            border-radius: 5px;
        }
""")
        self.setWindowTitle("Logic Synthesizer")
        (width,height) = QGuiApplication.primaryScreen().size().toTuple()
        self.resize(width, height)
 
        self.prompt = QLabel("Select an option to input your boolean logic")
        self.prompt.setAlignment(Qt.AlignCenter)
 
        self.actions = {
            "Find Text File": 1,
            "Type Text": 2,
        }
        self.mode = None
        self.w = None
        button_row = QHBoxLayout()
        for label in self.actions.keys():
            button = QPushButton(label)
            button.clicked.connect(
                lambda _checked=False, l=label: self.show_new_window(l)
            )
            button_row.addWidget(button)
 
        layout = QVBoxLayout()
        layout.addWidget(self.prompt)
        layout.addLayout(button_row)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


    def show_new_window(self, mode):
        self.mode = mode

        if self.mode == "Find Text File":
            self.w = FileWindow()
            self.w.setAttribute(Qt.WA_DeleteOnClose)
            self.w.destroyed.connect(self.reset_child)

        elif self.mode == "Type Text":
            self.w = TextWindow()
            self.w.setAttribute(Qt.WA_DeleteOnClose)
            self.w.destroyed.connect(self.reset_child)

        self.w.show()

    def reset_child(self):
        self.w = None

class TextWindow(QWidget): 
    def __init__(self): 
        super().__init__()
        self.setStyleSheet("""
                QWidget {
                    background-color: #222222;
                    color: #ffffff;
                }
        """)
        self.prompt = QLabel("""   Valid inputs are: \n """ + "="*80 + """ \n Sum of Product Form \n""" + "="*80 + """ \n Close window to go back""")
        self.prompt.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.text_box = QLineEdit()
        (width,height) = QGuiApplication.primaryScreen().size().toTuple()
        self.resize(width, height)
        self.text_box.setPlaceholderText("Input your Boolean function")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.prompt)
        self.layout.addWidget(self.text_box)
        self.setLayout(self.layout)
        self.text_box.returnPressed.connect(self.show_input)

    def show_input(self):
        self.prompt.setText(f'''Your function is: \n {self.text_box.text()}''')
        self.function_text = self.text_box.text()
        self.layout.removeWidget(self.text_box)
        self.text_box.deleteLater()

        self.button_row = QHBoxLayout()
        self.actions = ['Restart', 'Logic Synthesis', 'Do nothing']
        for action in self.actions: 
            button = QPushButton(action)
            button.clicked.connect(
                            lambda _checked=False, l=action: self.action_buttons(l)
                        )
            self.button_row.addWidget(button)
        self.layout.addLayout(self.button_row)

    def action_buttons(self, action): 
        if action == 'Restart':
            self.prompt.setText("""   Valid inputs are: \n """ + "="*80 + """ \n Sum of Product Form \n""" + "="*80 + """ \nClose window to go back""")
            self.layout.removeItem(self.button_row)
            self.text_box = QLineEdit()
            self.text_box.setPlaceholderText("Input your Boolean function")
            self.layout.addWidget(self.text_box)
            self.text_box.returnPressed.connect(self.show_input)
        elif action == 'Logic Synthesis':
            self.clear_buttons()
            self.button_row = QGridLayout()
            self.actions = ['Canon SOP', 'Canon POS', 'Inverse Canon SOP',
                            'Inverse Canon POS', 'Literal Minimized SOP', 'Literal Minimized POS',
                             'Prime Implicants', 'Essential Prime Implicants', 'ON-Set Minterms', 
                              'OFF-Set Maxterms', 'cus1', 'cus2' ]
            i = 0
            j = 0
            for action in self.actions: 
                if i == 3: 
                    j += 1
                    i = 0 
                button = QPushButton(action)
                button.clicked.connect(
                                lambda _checked=False, l=action: self.logic_synth(l)
                            )
                self.button_row.addWidget(button, 1 + j, i)
                i +=1 
            try: 
                tre = self.parse_input(self.function_text)
            except ValueError as e: 
                self.prompt.setText(f"{e}")
            self.layout.addLayout(self.button_row)
        elif action == 'Do Nothing':
            pass 

    def clear_button_row_actions(self):
        self.clear_buttons()
        self.button_row.deleteLater()
        self.button_row = QHBoxLayout()
        self.actions = ['Restart', 'Do nothing']
        for action in self.actions: 
            button = QPushButton(action)
            button.clicked.connect(
                            lambda _checked=False, l=action: self.action_buttons(l)
                        )
            self.button_row.addWidget(button)
        self.layout.addLayout(self.button_row)

    def logic_synth(self, action): 
        if action == 'Canon SOP':
            tre = self.parse_input(self.function_text)
            canSOP = self.can_sop(tre)
            self.prompt.setText(f"Your CANONICAL SOP is: \n {canSOP}")
            self.clear_button_row_actions()
        if action == 'Canon POS':
            tre = self.parse_input(self.function_text)
            canPOS = self.can_pos(tre)
            self.prompt.setText(f"Your CANONICAL POS is: \n {canPOS}")
            self.clear_button_row_actions()
        if action == 'Inverse Canon SOP':
            tre = self.parse_input(self.function_text)
            invCanSOP = self.inverse_can_sop(tre)
            self.prompt.setText(f"Your INVERSE CANONICAL SOP is: \n {invCanSOP}")
            self.clear_button_row_actions()
        if action == 'Inverse Canon POS':
            tre = self.parse_input(self.function_text)
            invCanPOS = self.inverse_can_pos(tre)
            self.prompt.setText(f"Your INVERSE CANONICAL POS is: \n {invCanPOS}")
            self.clear_button_row_actions()
        if action == 'Literal Minimized SOP':
            tre = self.parse_input(self.function_text)
            minimized_sop = self.minimized_SOP(tre)
            self.prompt.setText(f'Your MINIMIZED SOP is: {minimized_sop}')
            self.clear_button_row_actions()
        if action == "Literal Minimized POS":
            tre = self.parse_input(self.function_text)
            minimized_pos = self.minimized_POS(tre)
            self.prompt.setText(f'Your MINIMIZED POS is: {minimized_pos}')
            self.clear_button_row_actions()
        if action == 'Prime Implicants': 
            tre = self.parse_input(self.function_text)
            prime_Implicants, variables = self.prime_implicants(tre)
            primes = []
            for prime in prime_Implicants:
                term = ''
                for bit, var in zip(prime, variables): 
                    if bit == '1':
                        term += var
                    elif bit == '0':
                        term += var + "'"
                if not term: 
                    term = '1'
                primes.append(term)
            self.prompt.setText(f'Your PRIME IMPLICANTS are: {primes}')
            self.clear_button_row_actions()
        if action == 'Essential Prime Implicants':
            tre = self.parse_input(self.function_text)
            essential_implicants, variables = self.essential_prime_implicants(tre)
            essentials = []
            for essential in essential_implicants: 
                term = ''
                for bit, var in zip(essential, variables):
                    if bit == '1':
                        term += var 
                    elif bit == '0':
                        term += var + "'"
                if not term: 
                    term = '1'
                essentials.append(term)
            self.prompt.setText(f'Your ESSENTIAL PRIME IMPLICANTS are: {essentials}')
            self.clear_button_row_actions()
        if action == 'ON-Set Minterms':
            tre = self.parse_input(self.function_text)
            minterms, num_minterms = self.on_set(tre)
            self.prompt.setText(f"The ON-SET CONSISTS OF: \n {minterms} \n Hence there are {num_minterms} on-set minterms")
            self.clear_button_row_actions()
        if action == 'OFF-Set Maxterms':
            tre = self.parse_input(self.function_text)
            maxterms, num_maxterms = self.off_set(tre)
            self.prompt.setText(f"The OFF-SET CONSISTS OF: \n {maxterms} \n Hence there are {num_maxterms} off-set maxterms")
            self.clear_button_row_actions()
        if action == "cus1":
            tre = self.parse_input(self.function_text)
            truth_table = self.truth_table(tre)
            self.prompt.setText(f'Your TRUTH TABLE is: \n \n {truth_table} \n \n Saved to foo.csv')
            self.clear_button_row_actions()
        if action == 'cus2':
            tre = self.parse_input(self.function_text)
            minimized_sop = self.minimized_SOP(tre)
            processed = self.parse_input(minimized_sop)
            with open('footree.csv', "w") as f:
                json.dump(processed.to_dict(), f, indent=2)
            self.prompt.setText(f"Your data has been processed into a json tree file \n \n Saved to footree.csv")
            self.clear_button_row_actions()

    def clear_buttons(self):
        while self.button_row.count():
            self.button_row.takeAt(0).widget().deleteLater()
        self.layout.removeItem(self.button_row)

    def parse_input(self, text):
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

        display = f"Select an option"
        self.prompt.setText(display)

        return OR

    def compute(self, node, truths):
        '''
        Truths should be a dictionary, we will loop over all possible combinations of literals later
        '''
        if node.node_type == 'Literal':
            if node.value.endswith("'"):
                name = node.value[:-1]
                return not truths[name]
            return truths[node.value]

        children = [self.compute(child, truths) for child in node.children]

        if node.node_type == "AND":
            return all(children)

        if node.node_type == "OR":
            return any(children)

    def get_variables(self, node): 
        if node.node_type == "Literal": 
            return {node.value.replace("'", '')}
        variables = set()
        for child in node.children: 
            variables.update(self.get_variables(child))
        return variables

    def can_sop(self, node):
        literals = sorted(self.get_variables(node))
        num = len(literals) 

        can_sop_terms = []

        for combination in itertools.product(range(2), repeat = num):
            truths = dict(zip(literals, combination)) 
            value = self.compute(node, truths)

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

    def inverse_can_sop(self, node): 
        literals = sorted(self.get_variables(node))
        num = len(literals) 

        can_sop_terms = []

        for combination in itertools.product(range(2), repeat = num):
            truths = dict(zip(literals, combination)) 
            value = self.compute(node, truths)

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

    def can_pos(self,node): 
        literals = sorted(self.get_variables(node))
        num = len(literals) 

        can_pos_terms = []

        for combination in itertools.product(range(2), repeat = num): 
            truths = dict(zip(literals, combination))
            value = self.compute(node, truths)

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

    def inverse_can_pos(self,node): 
        literals = sorted(self.get_variables(node))
        num = len(literals) 

        can_pos_terms = []

        for combination in itertools.product(range(2), repeat = num): 
            truths = dict(zip(literals, combination))
            value = self.compute(node, truths)

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



    def minimized_SOP(self, node): 
        literals = sorted(self.get_variables(node))
        num = len(literals) 
        
        minterms = []

        for combination in itertools.product(range(2), repeat = num):
            truths = dict(zip(literals, combination)) 
            value = self.compute(node, truths)

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

    def minimized_POS(self, node):
        literals = sorted(self.get_variables(node))
        num = len(literals)

        maxterm_strings = []
        for combination in itertools.product(range(2), repeat=num):
            truths = dict(zip(literals, combination))
            if not self.compute(node, truths):
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

    def prime_implicants(self, node): 
        literals = sorted(self.get_variables(node))
        num = len(literals) 
        
        minterms = []

        for combination in itertools.product(range(2), repeat = num):
            truths = dict(zip(literals, combination)) 
            value = self.compute(node, truths)

            if value == True:
                minterms.append(combination)
        ## Claude For the line below, makes tuples into a string of binary
        minterm_strings = [''.join(str(b) for b in t) for t in minterms]
        prime = getPrimeImplicants(minterm_strings)

        return prime, literals 

    def essential_prime_implicants(self, node): 
        literals = sorted(self.get_variables(node))
        num = len(literals) 
        
        minterms = []

        for combination in itertools.product(range(2), repeat = num):
            truths = dict(zip(literals, combination)) 
            value = self.compute(node, truths)

            if value == True:
                minterms.append(combination)
        ## Claude For the line below, makes tuples into a string of binary
        minterm_strings = [''.join(str(b) for b in t) for t in minterms]
        prime = getPrimeImplicants(minterm_strings)
        essential, _ = getEssentialPrimeImplicants(prime, minterm_strings)

        return essential, literals

    def on_set(self, node):
        literals = sorted(self.get_variables(node))
        num = len(literals) 

        minterms = []

        for combination in itertools.product(range(2), repeat = num):
            truths = dict(zip(literals, combination)) 
            value = self.compute(node, truths)

            if value == True:
                minterms.append(int(''.join(map(str,combination)), 2))

        return minterms, len(minterms)

    def off_set(self, node):
        literals = sorted(self.get_variables(node))
        num = len(literals) 

        maxterms = []

        for combination in itertools.product(range(2), repeat = num):
            truths = dict(zip(literals, combination)) 
            value = self.compute(node, truths)

            if value == False:
                maxterms.append(int(''.join(map(str,combination)), 2))

        return maxterms, len(maxterms)

    def truth_table(self, node):
        literals = sorted(self.get_variables(node))
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
            value = self.compute(node, truths)
            row = np.append(combination, value)
            truth_csv = np.vstack([truth_csv, row])
            truth_table +=  f"   {int(value)}   |"
            truth_table += '\n' 
            truth_table += '-' * (width + 6) + "\n"

        np.savetxt("foo.csv", truth_csv, delimiter=',', fmt='%s')

        return truth_table

class FileWindow(TextWindow):
    def __init__(self):
        super().__init__()   
        self.text_box.returnPressed.disconnect(self.show_input)
        self.layout.removeWidget(self.text_box)
        self.text_box.deleteLater()
        self.text_box = None
        self.show_browse_button()

    def show_browse_button(self):
        self.browse_button = QPushButton("Find file")
        self.browse_button.clicked.connect(self.find_file)
        self.layout.addWidget(self.browse_button)

    def find_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select a file containing your Boolean function",
            os.getcwd(),
            "Text files (*.txt)",
        )
        if not path:         
            return

        try:
            with open(path, 'r', encoding='utf-8') as r:
                text = r.read().strip()
        except OSError as e:
            self.prompt.setText(f"Could not open file:\n{e}")
            return

        self.function_text = text      
        self.prompt.setText(f'Your function is: \n {text}')

        self.layout.removeWidget(self.browse_button)
        self.browse_button.deleteLater()

        self.button_row = QHBoxLayout()
        self.actions = ['Restart', 'Logic Synthesis', 'Do nothing']
        for action in self.actions:
            button = QPushButton(action)
            button.clicked.connect(
                lambda _checked=False, l=action: self.action_buttons(l)
            )
            self.button_row.addWidget(button)
        self.layout.addLayout(self.button_row)

    def action_buttons(self, action):
        if action == 'Restart':
            self.clear_buttons()
            self.button_row.deleteLater()
            self.prompt.setText("""   Valid inputs are: \n """ + "="*80 + """ \n Sum of Product Form \n""" + "="*80 + """ \nClose window to go back""")
            self.show_browse_button()
        else:
            super().action_buttons(action)


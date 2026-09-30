import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QStackedLayout,
    QGridLayout
)
from PySide6.QtGui import QGuiApplication

import itertools
import re

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

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
                # can_sop = self.can_pos(tre)
                # self.prompt.setText(f""" Your CANONICAL SOP is: \n {can_sop}""")
            except ValueError as e: 
                self.prompt.setText(f"{e}")
            self.layout.addLayout(self.button_row)
        elif action == 'Do Nothing':
            pass 

    def logic_synth(self, action): 
        if action == 'Canon SOP':
            tre = self.parse_input(self.function_text)
            canSOP = self.can_sop(tre)
            self.prompt.setText(f"Your CANONICAL SOP is: \n {canSOP}")

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
        if action == 'Canon POS':
            tre = self.parse_input(self.function_text)
            canPOS = self.can_pos(tre)
            self.prompt.setText(f"Your CANONICAL POS is: \n {canPOS}")

            self.clear_buttons()
            self.button_row = QHBoxLayout()
            self.actions = ['Restart', 'Do nothing']
            for action in self.actions: 
                button = QPushButton(action)
                button.clicked.connect(
                                lambda _checked=False, l=action: self.action_buttons(l)
                            )
                self.button_row.addWidget(button)
            self.layout.addLayout(self.button_row)
        if action == 'Inverse Canon SOP':
            tre = self.parse_input(self.function_text)
            invCanSOP = self.inverse_can_sop(tre)
            self.prompt.setText(f"Your INVERSE CANONICAL SOP is: \n {invCanSOP}")

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
        if action == 'Inverse Canon POS':
            tre = self.parse_input(self.function_text)
            invCanPOS = self.inverse_can_pos(tre)
            self.prompt.setText(f"Your INVERSE CANONICAL POS is: \n {invCanPOS}")

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

        ## OTHER ACTIONS GO HERE ##

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

        if action == 'ON-Set Minterms':
            tre = self.parse_input(self.function_text)
            minterms, num_minterms = self.on_set(tre)
            self.prompt.setText(f"The ON-SET CONSISTS OF: \n {minterms} \n Hence there are {num_minterms} on-set minterms")

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

        if action == 'OFF-Set Maxterms':
            tre = self.parse_input(self.function_text)
            maxterms, num_maxterms = self.off_set(tre)
            self.prompt.setText(f"The OFF-SET CONSISTS OF: \n {maxterms} \n Hence there are {num_maxterms} off-set maxterms")

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


        ## OTHER FUNCTIONS GO HERE ##

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
                            

        

        
class FileWindow(QWidget): 
    def __init__(self): 
        super().__init__()
        self.setStyleSheet("""
                QWidget {
                    background-color: #222222;
                    color: #ffffff;
                }
        """)
        self.prompt = QLabel("""   Valid inputs are: \n """ + "="*80 + """ \n Sum of Product Form \n""" + "="*80 + """ \nClose window to go back""")
        self.prompt.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.text_box = QLineEdit()
        (width,height) = QGuiApplication.primaryScreen().size().toTuple()
        self.resize(width, height)
        self.text_box.setPlaceholderText("""Type the path to the file you want to open (relative to where this script is)""")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.prompt)
        self.layout.addWidget(self.text_box)
        self.setLayout(self.layout)

        self.text_box.returnPressed.connect(self.find_file)

    def find_file(self):
        path = self.text_box.text()

        with open(f'{path}', 'r', encoding='utf-8') as r: 
            self.prompt.setText(f'Your function is: \n {r.read()}')

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
            self.text_box.setPlaceholderText("""Type the path to the file you want to open (relative to where this script is)""")
            self.layout.addWidget(self.text_box)
            self.text_box.returnPressed.connect(self.find_file)
        elif action == 'Logic Synthesis':
            self.layout.removeItem(self.button_row)
            self.prompt.setText('Work In progress')
        elif action == 'Do Nothing':
            pass 

 
 
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


class tree(): 
    def __init__(self, node_type, value = None ):
        self.node_type = node_type 
        self.value = value 
        self.children = []

    def add_child(self, child):
        self.children.append(child)

def getPrimeImplicants(minterms):  # psuedo code on wikipedia 
    primeImplicants = []
    num_min = len(minterms)
    merges = [False] * num_min
    numberOfMergers = 0 
    mergedMinterm, minterm1, minterm2 = '','',''
    for i in range(num_min): 
        for c in range(i + 1, num_min): 
            minterm1 = minterms[i]
            minterm2 = minterms[c]

            if checkDashesAlign(minterm1, minterm2) and checkMintermDifference(minterm1, minterm2): 
                mergedMinterm = mergeMinterms(minterm1, minterm2)
                if mergedMinterm not in primeImplicants: 
                    primeImplicants.append(mergedMinterm)

                numberOfMergers += 1
                merges[i] = True 
                merges[c] = True 
    for j in range(num_min): 
        if merges[j] == False and minterms[j] not in primeImplicants: 
            primeImplicants.append(minterms[j])
    if numberOfMergers == 0:
        return primeImplicants
    else: 
        return getPrimeImplicants(primeImplicants)


def mergeMinterms(minterm1, minterm2): 
    mergedMinterm = ''
    for i in range(len(minterm1)): 
        if minterm1[i] != minterm2[i]:
            mergedMinterm += '-'
        else: 
            mergedMinterm += minterm1[i]

    return mergedMinterm


def checkDashesAlign(minterm1, minterm2): 
    for i in range(len(minterm1)): 
        if minterm1[i] != '-' and minterm2[i] == '-':
            return False 
    return True 

def checkMintermDifference(minterm1, minterm2): 
    m1 = int(minterm1.replace('-','0'), 2)
    m2 = int(minterm2.replace('-','0'), 2)

    result = m1 ^ m2

    return result != 0 and (result & (result - 1)) == 0 
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
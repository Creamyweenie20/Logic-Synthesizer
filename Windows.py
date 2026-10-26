"""
Code for GUI 
"""

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
    QGridLayout,
    QScrollArea,
)
from PySide6.QtGui import QGuiApplication
from tree import tree
from Functions import *
from Logic import *

import numpy as np

import itertools
import re
import json

from Verilog import VerilogGen

import os

# Setting path to the one currently opened
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # CSS style for setting aesthetic of the GUI
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

        # Set GUI to cover whole window
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
            # Lambda needed to open new window once pressed, gets ride of the clicked boolean
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
            # Needs the Delete on Close to actually close the window
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
        """
        Method to show the user input once enter or return is pressed
        """

        self.prompt.setText(f'''Your function is: \n {self.text_box.text()}''')
        self.function_text = self.text_box.text()
        self.layout.removeWidget(self.text_box)
        # Deletes text_box data once event loop is done, i.e. once the action of your pressed button is done
        self.text_box.deleteLater()

        self.button_row = QHBoxLayout()
        self.actions = ['Restart', 'Logic Synthesis', 'Verilog']
        for action in self.actions: 
            button = QPushButton(action)
            button.clicked.connect(
                            lambda _checked=False, l=action: self.action_buttons(l)
                        )
            self.button_row.addWidget(button)
        self.layout.addLayout(self.button_row)

    def action_buttons(self, action): 
        """
        Method to change window into a certain stage of logic synthesis 
        """

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
                              'OFF-Set Maxterms', 'Truth Table', 'JSON Tree' ]
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
                # tre = parse_input(self.function_text) Useless call of parse_input
                display = f"Select an option"
                self.prompt.setText(display)

            except ValueError as e: 
                self.prompt.setText(f"{e}")

            self.layout.addLayout(self.button_row)


        elif action == 'Verilog':
            try:
                tre = parse_input(self.function_text)
                minimized = minimized_SOP(tre)
                self.prompt.setText(f"The minimized SOP is used to generate a Verilog file \n {minimized}")
                tre = parse_input(minimized)
                path, _ = QFileDialog.getSaveFileName(
                    self,
                    "Save Verilog File",
                    "top.v",
                    "Verilog Files (*.v);;All Files (*)"
                )

                if not path:
                    return  

                gen = VerilogGen()
                # Module and wrapper module names are independent of the file names
                gen.write(tre, path, module_name="top")
                path = path.replace(".v", "_wrapper.v")
                gen.write_wrapper(path, module = "top", wrapper = "wrapper")

            except Exception as e:
                self.prompt.setText(f"Verilog synthesis failed:\n{e}") 

    def clear_button_row_actions(self):
        """
        Helper function for repeated use of clearing the row buttons and replacing it with only Restart
        """

        self.clear_buttons()
        self.button_row.deleteLater()
        self.button_row = QHBoxLayout()
        self.actions = ['Restart']
        for action in self.actions: 
            button = QPushButton(action)
            button.clicked.connect(
                            lambda _checked=False, l=action: self.action_buttons(l)
                        )
            self.button_row.addWidget(button)
        self.layout.addLayout(self.button_row)

    def logic_synth(self, action): 
        """
        Large if statements that calls all of the logic funcitons depending on the button pressed
        """

        if action == 'Canon SOP':
            tre = parse_input(self.function_text)
            display = f"Select an option"
            self.prompt.setText(display)
            canSOP = can_sop(tre)
            self.prompt.setText(f"Your CANONICAL SOP is: \n {canSOP}")
            self.clear_button_row_actions()

        if action == 'Canon POS':
            tre = parse_input(self.function_text)
            display = f"Select an option"
            self.prompt.setText(display)
            canPOS = can_pos(tre)
            self.prompt.setText(f"Your CANONICAL POS is: \n {canPOS}")
            self.clear_button_row_actions()

        if action == 'Inverse Canon SOP':
            tre = parse_input(self.function_text)
            display = f"Select an option"
            self.prompt.setText(display)
            invCanSOP = inverse_can_sop(tre)
            self.prompt.setText(f"Your INVERSE CANONICAL SOP is: \n {invCanSOP}")
            self.clear_button_row_actions()

        if action == 'Inverse Canon POS':
            tre = parse_input(self.function_text)
            display = f"Select an option"
            self.prompt.setText(display)
            invCanPOS = inverse_can_pos(tre)
            self.prompt.setText(f"Your INVERSE CANONICAL POS is: \n {invCanPOS}")
            self.clear_button_row_actions()

        if action == 'Literal Minimized SOP':
            tre = parse_input(self.function_text)
            display = f"Select an option"
            self.prompt.setText(display)
            minimized_sop = minimized_SOP(tre)
            self.prompt.setText(f'Your MINIMIZED SOP is: {minimized_sop}')
            self.clear_button_row_actions()

        if action == "Literal Minimized POS":
            tre = parse_input(self.function_text)
            display = f"Select an option"
            self.prompt.setText(display)
            minimized_pos = minimized_POS(tre)
            self.prompt.setText(f'Your MINIMIZED POS is: {minimized_pos}')
            self.clear_button_row_actions()

        if action == 'Prime Implicants': 
            tre = parse_input(self.function_text)
            display = f"Select an option"
            self.prompt.setText(display)
            prime_Implicants, variables = prime_implicants(tre)
            primes = []
            for prime in prime_Implicants:
                term = ''
                # Need to translate into literals
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
            tre = parse_input(self.function_text)
            display = f"Select an option"
            self.prompt.setText(display)
            essential_implicants, variables = essential_prime_implicants(tre)
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
            tre = parse_input(self.function_text)
            display = f"Select an option"
            self.prompt.setText(display)
            minterms, num_minterms = on_set(tre)
            self.prompt.setText(f"The ON-SET CONSISTS OF: \n {minterms} \n Hence there are {num_minterms} on-set minterms")
            self.clear_button_row_actions()

        if action == 'OFF-Set Maxterms':
            tre = parse_input(self.function_text)
            display = f"Select an option"
            self.prompt.setText(display)
            maxterms, num_maxterms = off_set(tre)
            self.prompt.setText(f"The OFF-SET CONSISTS OF: \n {maxterms} \n Hence there are {num_maxterms} off-set maxterms")
            self.clear_button_row_actions()

        if action == "Truth Table":
            tre = parse_input(self.function_text)
            display = f"Select an option"
            self.prompt.setText(display)
            truth_tab = truth_table(tre)
            scrollArea = QScrollArea()
            scrollArea.setWidget(self.prompt)
            self.layout.addWidget(scrollArea)
            self.prompt.setText(f'Your TRUTH TABLE is: \n \n {truth_tab} \n \n Saved to foo.csv')
            self.prompt.adjustSize()
            scrollArea.setAlignment(Qt.AlignCenter)
            self.clear_button_row_actions()

        if action == 'JSON Tree':
            tre = parse_input(self.function_text)
            display = f"Select an option"
            self.prompt.setText(display)
            minimized_sop = minimized_SOP(tre)
            processed = parse_input(minimized_sop)
            with open('footree.json', "w") as f:
                json.dump(processed.to_dict(), f, indent=2)
            self.prompt.setText(f"Your data has been processed into a json tree file \n \n Saved to footree.json")
            self.clear_button_row_actions()

    def clear_buttons(self):
        while self.button_row.count():
            self.button_row.takeAt(0).widget().deleteLater()
        # Removes the row full of empty buttons
        self.layout.removeItem(self.button_row)

class FileWindow(TextWindow):
    """
    Gui window for you finding a text file in your directories instead of typing it out
    """
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
            "Text files (*.txt *.json)",
        )
        if not path:         
            return

        try:
            if path.lower().endswith(".json"):
                with open(path, 'r', encoding='utf-8') as r: 
                    data = json.load(r)
                text = tree.from_json(data).to_sop()
            else:
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
        self.actions = ['Restart', 'Logic Synthesis', 'Verilog']
        for action in self.actions:
            button = QPushButton(action)
            button.clicked.connect(
                lambda _checked=False, l=action: self.action_buttons(l)
            )
            self.button_row.addWidget(button)
        self.layout.addLayout(self.button_row)

    def action_buttons(self, action):
        """
        Different from Text Window because we dont type input here
        """
        if action == 'Restart':
            self.clear_buttons()
            self.button_row.deleteLater()
            self.prompt.setText("""   Valid inputs are: \n """ + "="*80 + """ \n Sum of Product Form \n""" + "="*80 + """ \nClose window to go back""")
            self.show_browse_button()
        else:
            # calls the parent method instead
            super().action_buttons(action)


# Logic-Synthesizer
Have you ever wanted to play around with a custom Logic Synthesis Engine? No? Well okay, here is one anyways. At the highest level, you give this engine your custom made boolean function and then it processes it. What you want it to do depends on the buttons you press, how interactive! We present the FLSE (Finite logic synthesis engine), all programmed in Python. 

## Graphical User Interface
The FLSE is a graphical interface program utilizing the Pyside 6 library. It accepts file and direct command line inputs, limited to 16 literals. The inputs, however, are currently restricted to being in the sum of products form as of Beta 0.1. In the future, FLSE will take product of sums form and a JSON file with a graph based circuit representation. To run FLSE, run the main.py python file. The Windows.py file has all the code pertaining to the graphical user interface. As a note, FLSE uses a n-ary tree to process and simplify inputs. The class file for these trees are the tree.py file.  

When opening the program, the user is directed to select either a text file or directly enter a boolean function. The functionalities of FLSE does not depend on what choice the user decides to use. Once entered, the user is prompted with three options: process the boolean function with built in logic functionalities, compile verilog files, or to go back and enter a different boolean function. 

## Logic Synthesis Engine Features
The FSLE has 12 built in operations. It can return the canonical SOP, the canonical POS, inverse canonical SOP, inverse canonical POS, literal minimized SOP, literal minimized POS, prime implicants, essential prime implicatns, on-set minterms, off-set maxterms, truth table in the form of a csv file, and a graphical tree representation of the minmized SOP form in a JSON file. All functions pertaining to these features are either in the Functions.py or Logic.py files. 

The literal minimized SOP is found via the Quine-McCluskey algorithm in conjunction with Petrick's method. 

## Verilog Generation
The FLSE generates a valid structural Verilog.v file by instatiating gates and wiring them together. The verilog file implemets the minimized SOP circuit that is found via the same way as in the previous section does. It would also create a wrapper file for ease of deploying on an FPGA. The constraint file is restricted to 16 switches, which is reasonable for demonstrations. The Verilog.py file contains all of the code for this feature. 

## External Outputs and Other Files
In this repository, there are two additional files not needed to run FLSE. These files were used for testing and has some form of the word test in the file name. The external outputs from all of the features include foo.csv, footree.json, top_wrapper.v, and top.v which are the truth table CSV, the tree representation, the wrapper function for the verilog, and the verilog module. The last two files are the test.txt which acts as a demonstration file for the file input functionality and the constraint file for the FPGA deployment. 

## Dependencies 
The FLSE needs the following dependencies to run: 
Pyside

## Future Directions: 
As mentioned previously, this is only the first beta release of FLSE. Along with increasing the input forms, FLSE will have more logic processing features in the future, such as tree repsentation visualization among other things. 

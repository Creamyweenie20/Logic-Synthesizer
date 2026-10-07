# Logic-Synthesizer
This is our submission for program assignment 1 for BU's EC551 (F'2026) taught by Doctor Densmore. The goal of this program is to accept a Boolean algebraic function or digital combinational circuit, optimize/manipulate it, report logic metric, and generate a structural Verilog file and/or netlist. This will then be synthesized and implemented on a FPGA board. As of September 29th, this is a work in progress. 

## Inputs
We implemented a gui using Python and the pyside6 library. With this gui (as of 9/29/2026), you could both type in your Boolean function or extract the Boolean function from a text file. The Boolean function is input in its Sum-of-Products representation, where we will hopefully add other input forms in the future. Also, we hope allow for a graph-based circuit representation input, which should not prove too challenging for we process the Boolean expression using n-ary trees. The gui itself has multiple functionalities, however we have not yet implemented all of the functionalities working sequentially or in parallel. The user would need to reset, effectively, the program for each function. We will hopefully streamline this in the future. 

## Logic Synthesis Engine Features
As of 9/29/2026, the following operations are supported by our program: 
Canonical SOP, Canonical POS, Inverse Canonical SOP, Inverse Canonical POS, Prime Implicants, On-set Minterms, Off-set Maxterms. All outputs are, so far, in the GUI pane. 

## Future Steps
We will finish the engine's features (Minimized SOP/POS, essential primes, exporting truth table, and visualizing the minimized boolean function as a graph). Streamline the engine for better user-interface. We will also work on increasing the amount of ways we can input a Boolean function and the forms/representations these inputs could take. 

## Updates: 
All of the above descriptions are defunct as of 10/7/2026. I have finished the functionality, all I need to do is fix organization and such. This commit has done that slightly and will need to work on it more. 
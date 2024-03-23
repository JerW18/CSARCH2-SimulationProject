# IEEE-754 Binary-32 floating-point operation
## Overview
This Python project implements IEEE-754 binary-32 floating point arithmetic operations, specifically focusing on addition. The operation allows two rounding formats - with Guard, Round, Sticky (GRS) and without (GRS) which uses Round To Nearest, Ties to Even(RTN-TE) to round to the required number of bits for the operands. It has support for positive and negative binary values, a maximum of up to 24 digits, and exponent values ranging from -126 to 127. The step-by-step output is shown in normalized 1.f binary format, with an additional option to export said steps as a text file.

## Features
- Expected Input: Positive and Negative binary inputs
- Exponent Constraints: -126 to 127 exponent values
- Digit Constraints: 24 digits
- Operations: Addition and Subtraction (via negative inputs)
- Rounding Modes: RTNE and GRS rounding, Normalization
- Input Checking
- Step-by-step output displayed in the GUI
- Option for file export as a .txt file

## Usage
### Running the code
Download the GitHub files into your local machine.
Open the file IEEE_754_Binary_32_operation.py
Compile and run the Python file (IEEE_754_Binary_32_operation.py)

### GUI Input
The program will ask the user for two floating point binary inputs and their exponents. 
Following this they will be prompted to choose which rounding mode they would like to use.
Then lastly they need to input the number of digits that is going to be used for the operation.


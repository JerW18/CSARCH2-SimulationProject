from decimal import *
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

# Float to Binary Conversion
def float_to_binary(float_num, precision):
    negative = False
    if float_num < 0:
        float_num = abs(float_num)
        negative = True
    integer_part = int(float_num)
    fractional_part = float_num - integer_part

    binary_integer = bin(integer_part).replace("0b", "")

    binary_fractional = ""
    while fractional_part > 0 and len(binary_fractional) < precision:
        fractional_part *= 2
        bit = int(fractional_part)
        binary_fractional += str(bit)
        fractional_part -= bit

    if negative:
        binary_integer = "-" + binary_integer
    if len(binary_fractional) == 0:
        return binary_integer
    else:
        return binary_integer + "." + binary_fractional

# Move Decimal Point of a Number given the Shift
# Positive shift: moves the decimal point to the left
# Negative shift: moves the decimal point to the right
def move_decimal_point(binary_str, shift):

    if shift == 0:
        return binary_str

    integer_part, fractional_part = binary_str.split('.')
    
    shifted_integer = ''
    shifted_fractional = ''
    
    if '1' not in integer_part and '1' in fractional_part:
        if shift < 0 and fractional_part[0] != '1':
            shifted_integer = '0'
            shifted_fractional = fractional_part[1:] 
            return shifted_integer + '.' + shifted_fractional
        elif shift < 0 and fractional_part[0] == '1':
            shifted_integer = '1'
            shifted_fractional = fractional_part[1:]
            return shifted_integer + '.' + shifted_fractional
        

    # Shift the decimal point to the right
    if shift < 0:
        if len(fractional_part) < abs(shift):
            shifted_integer += integer_part + fractional_part
            shifted_integer += '0' * (abs(shift) - len(fractional_part))
            shifted_fractional = fractional_part[abs(shift):]
            
        elif len(fractional_part) >= abs(shift):
            shifted_integer = integer_part + fractional_part[:abs(shift)]
            shifted_fractional = fractional_part[abs(shift):]
            
        if len(shifted_fractional) == 0:
            shifted_fractional = '0'
        if len(shifted_integer) == 0:
            shifted_integer = '0'
        
        return shifted_integer + '.' + shifted_fractional
    
    # Shift the decimal point to the left    
    elif shift >= 0:
        if '-' not in integer_part:
            if len(integer_part) < abs(shift):
                shifted_fractional = '0' * (abs(shift) - len(integer_part)) + integer_part + fractional_part
                shifted_integer = '0'
                
            elif len(integer_part) >= abs(shift):
                shifted_fractional = integer_part[-abs(shift):] + fractional_part
                shifted_integer = integer_part[:-abs(shift)]

            if len(shifted_integer) == 0:
                shifted_integer = '0'
                
            return shifted_integer + '.' + shifted_fractional
        
        elif '-' in integer_part:
            negative = integer_part[:1]
            integer_part = integer_part[1:]
            
            if len(integer_part) < abs(shift):
                shifted_fractional = '0' * (abs(shift) - len(integer_part)) + integer_part + fractional_part
                shifted_integer = '0'
                
            elif len(integer_part) >= abs(shift):
                shifted_fractional = integer_part[-abs(shift):] + fractional_part
                shifted_integer = integer_part[:-abs(shift)]

            if len(shifted_integer) == 0:
                shifted_integer = '0'
            
            return negative + shifted_integer + '.' + shifted_fractional

# Add Two Binary Numbers
def add_binary_numbers(binary_num1, binary_num2):
    int_part1, frac_part1 = binary_num1.split('.')
    int_part2, frac_part2 = binary_num2.split('.')
    int_neg1 = False
    int_neg2 = False
    
    if '-' in int_part1:
        int_neg1 = True
        int_part1 = int_part1[1:]
        
    if '-' in int_part2:
        int_neg2 = True
        int_part2 = int_part2[1:]
    
    dec_num1 = Decimal(int(int_part1, 2))
    dec_num2 = Decimal(int(int_part2, 2))
    
    frac_num1 = Decimal(int(frac_part1, 2)) / Decimal(2 ** len(frac_part1))
    frac_num2 = Decimal(int(frac_part2, 2)) / Decimal(2 ** len(frac_part2)) 
    
    num1 = dec_num1 + frac_num1
    num2 = dec_num2 + frac_num2
    
    if int_neg1:
        num1 = -num1
    if int_neg2:
        num2 = -num2
    
    sum_dec = num1 + num2

    sum_binary = float_to_binary(sum_dec, precision=len(frac_part1))

    return sum_binary

# Round to the Nearest Even (RTNTE) Rounding
def rtnte_rounding(binary_str, num_bits):
    is_negative = False
    if binary_str[0] == '-':
        binary_str = binary_str[1:]
        is_negative = True

    integer_part, fractional_part = binary_str.split('.')
    
    if num_bits == 1:
        return integer_part

    num_bits = num_bits - 1
    if len(fractional_part) > num_bits:
        round_bits, extra_bits = fractional_part[:num_bits], fractional_part[num_bits:]
        
        if extra_bits[0] == '1' and not any(bit in '1' for bit in extra_bits[1:]):
            if round_bits[-1] == '1':
                binary_str = add_binary_numbers(integer_part + '.' + round_bits, '0.' + '0' * (num_bits - 1) + '1')
            else:
                binary_str = integer_part + '.' + round_bits
                
        elif extra_bits[0] == '1' and any(bit in '1' for bit in extra_bits[1:]):
            binary_str = add_binary_numbers(integer_part + '.' + round_bits, '0.' + '0' * (num_bits - 1) + '1')
            
        else:
            binary_str = integer_part + '.' + round_bits

    if is_negative:
        binary_str = '-' + binary_str

    if '.' not in binary_str:
            binary_str += '.0'
            return binary_str
    integer_part, fractional_part = binary_str.split('.')
    if len(fractional_part) < num_bits:
        fractional_part += '0' * (num_bits - len(fractional_part))
        return integer_part + '.' + fractional_part
    else:
        return binary_str

# GRS Rounding
def grs_rounding(binary_str, num_bits):
    integer_part, fractional_part = binary_str.split('.')
    
    num_bits = num_bits + 1
    if len(fractional_part) > num_bits:
        round_bits = fractional_part[:num_bits]
        extra_bits = fractional_part[num_bits:]
        #messagebox.showinfo("Rounded Binary Numbers", f"Binary 1: {round_bits}\nBinary 2: {extra_bits}")
        if '1' in extra_bits:
            #append 1 to the last bit
            round_bits = round_bits + '1'
        else:
            #append 0 to the last bit
            round_bits = round_bits + '0'
    else:
        round_bits = fractional_part
        #append 0's
        round_bits += '0' * (num_bits - len(fractional_part))
        round_bits += '0'
    
    return integer_part + '.' + round_bits

# Normalize Binary to 1.f
def normalize_binary(binary_str, exponent):
    integer_part, fractional_part = binary_str.split('.')
    negative = ''
    
    if '-' in integer_part:
        integer_part = integer_part[1:]
        negative = '-'

    one_pos = integer_part.find('1')
    if(one_pos != -1):
        integer_part = integer_part[one_pos:]
        binary_str = integer_part + '.' + fractional_part
    integer_part, fractional_part = binary_str.split('.')
    
    while '1' not in integer_part and '1' in fractional_part:
        exponent -= 1
        binary_str = integer_part + '.' + fractional_part
        binary_str = move_decimal_point(binary_str, -1)
        integer_part, fractional_part = binary_str.split('.')

    #while number of 1's in integer part is greater than 1, shift
    while integer_part.count('1') > 1 and len(integer_part) > 1:
        exponent += 1
        binary_str = integer_part + '.' + fractional_part
        binary_str = move_decimal_point(binary_str, 1)
        integer_part, fractional_part = binary_str.split('.')

    while len(integer_part) > 1:
        exponent += 1
        binary_str = integer_part + '.' + fractional_part
        binary_str = move_decimal_point(binary_str, 1)
        integer_part, fractional_part = binary_str.split('.')
        
    if '-' not in binary_str and negative == '-':
        binary_str = negative + binary_str
    if '.' not in binary_str:
        binary_str += '.0'
    if binary_str[-1] == '.':
        binary_str = binary_str + '0'
    return binary_str, exponent

def save_output():
    try:
        output_text = text_output.get(1.0, tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(output_text)
            messagebox.showinfo("File Saved", "Output has been successfully saved to the text file.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving the file: {e}")


def perform_addition():
    try:
        text_output.delete(1.0, tk.END)

        #checking null inputs
        if len(entry_binary1.get()) == 0 or len(entry_exponent1.get()) == 0 or len(entry_binary2.get()) == 0 or len(entry_exponent2.get()) == 0 or len(entry_num_digits.get()) == 0:
            text_output.insert(tk.END, "Error: Please fill in all input fields.")
            return
        for char in entry_exponent1.get():
            if char not in '0123456789-':
                text_output.insert(tk.END, "Error: Incorrect input format for exponent 1. \nPlease input numericals only.")
                return
        for char in entry_exponent2.get():
            if char not in '0123456789-':
                text_output.insert(tk.END, "Error: Incorrect input format for exponent 2. \nPlease input numericals only.")
                return
        for char in entry_num_digits.get():
            if char not in '0123456789':
                text_output.insert(tk.END, "Error: Incorrect input format for number of digits. \nPlease input numericals only.")
                return

        binary1 = entry_binary1.get()
        exponent1 = int(entry_exponent1.get())
        binary2 = entry_binary2.get()
        exponent2 = int(entry_exponent2.get())
        rounding_mode = var_rounding_mode.get()
        num_digits = int(entry_num_digits.get())


        #check input validity
        if binary1.count('.') > 1 or binary2.count('.') > 1:
            text_output.insert(tk.END, "Error: Incorrect input format. \nPlease input binary numbers.")
            return
        if len(binary1) == 0 or len(binary2) == 0 or len(entry_exponent1.get()) == 0 or len(entry_exponent2.get()) == 0 or len(entry_num_digits.get()) == 0:
            text_output.insert(tk.END, "Error: Please input both binary numbers and exponents.")
            return
        
        for char in binary1:
            if char not in '01.-':
                text_output.insert(tk.END, "Error: Incorrect input format for binary 1. \nPlease input binary numbers.")
                return
        for char in binary2:
            if char not in '01.-':
                text_output.insert(tk.END, "Error: Incorrect input format for binary 2. \nPlease input binary numbers.")
                return

        if num_digits > 24 or num_digits < 1:
            text_output.insert(tk.END, "Error: Number of digits must be between 1 and 24.")
            return
        
        if binary1.count('-') > 1:
            text_output.insert(tk.END, "Error: Incorrect input format for binary 1. \nPlease input binary numbers.")
            return
        if binary2.count('-') > 1:
            text_output.insert(tk.END, "Error: Incorrect input format for binary 2. \nPlease input binary numbers.")
            return
        
        if binary1.find('-') != 0 and binary1.find('-') != -1:
            text_output.insert(tk.END, "Error: Incorrect input format for binary 1. \nPlease input binary numbers.")
            return
        if binary2.find('-') != 0 and binary2.find('-') != -1:
            text_output.insert(tk.END, "Error: Incorrect input format for binary 2. \nPlease input binary numbers.")
            return
        
        if(exponent1 < -126 or exponent1 > 127):
            text_output.insert(tk.END, "Error: Exponent 1 must be between -126 and 127.")
            return
        if(exponent2 < -126 or exponent2 > 127):
            text_output.insert(tk.END, "Error: Exponent 2 must be between -126 and 127.")
            return
        
        #normalizing
        if '.' not in binary1:
            binary1 += '.0'
        if '.' not in binary2:
            binary2 += '.0'
        
        normalize_binary1, exponent1 = normalize_binary(binary1, exponent1)
        normalize_binary2, exponent2 = normalize_binary(binary2, exponent2)

        text_output.insert(tk.END, "Normalized Binary Numbers:\n")
        text_output.insert(tk.END, f"Binary 1: [{normalize_binary1}] x 2^{exponent1}\n")
        text_output.insert(tk.END, f"Binary 2: [{normalize_binary2}] x 2^{exponent2}\n\n")

        #normalizing the binary numbers to the larger exponent
        if exponent1 > exponent2:
            normalize_binary2 = move_decimal_point(normalize_binary2, exponent1 - exponent2)
            exponent2 = exponent1
        elif exponent2 > exponent1:
            normalize_binary1 = move_decimal_point(normalize_binary1, exponent2 - exponent1)
            exponent1 = exponent2
        result_exponent = max(exponent1, exponent2)

        text_output.insert(tk.END, "Same Exponent Binary Numbers:\n")
        text_output.insert(tk.END, f"Binary 1: [{normalize_binary1}] x 2^{exponent1}\n")
        text_output.insert(tk.END, f"Binary 2: [{normalize_binary2}] x 2^{exponent2}\n\n")

        #rounding
        if rounding_mode == "RTNTE":
            round_binary1 = rtnte_rounding(normalize_binary1, num_digits)
            round_binary2 = rtnte_rounding(normalize_binary2, num_digits)
        elif rounding_mode == "GRS":
            round_binary1 = grs_rounding(normalize_binary1, num_digits)
            round_binary2 = grs_rounding(normalize_binary2, num_digits)

        text_output.insert(tk.END, "Rounded Binary Numbers:\n")
        text_output.insert(tk.END, f"Binary 1: [{round_binary1}] x 2^{exponent1}\n")
        text_output.insert(tk.END, f"Binary 2: [{round_binary2}] x 2^{exponent2}\n")

        #adding the binary numbers
        
        length1 = -10101010
        if '.' not in round_binary1:
            length1 = 0
            round_binary1 += '.0'
        if '.' not in round_binary2:
            round_binary2 += '.0'
        
        result_binary = add_binary_numbers(round_binary1, round_binary2)
        result_exponent = max(exponent1, exponent2)
        text_output.insert(tk.END, "-------------------------------------------------\n")
        #if num_digits > 1:
        if '.' not in result_binary:
           result_binary += '.0'
        fractional_part_round = round_binary1.split('.')[1]
        integer_part_result, fractional_part_result = result_binary.split('.')
        if len(fractional_part_round) > len(fractional_part_result):
            result_binary += '0' * (len(fractional_part_round) - len(fractional_part_result))
        if length1 == 0:
            result_binary = integer_part_result
        text_output.insert(tk.END, f"     Sum: [{result_binary}] x 2^{result_exponent}\n\n")

        #normalizing answer
        if '.' not in result_binary:
            result_binary += '.0'
        result_binary, result_exponent = normalize_binary(result_binary, result_exponent)
        result_binary = rtnte_rounding(result_binary, num_digits) 

        if num_digits > 1:
            result_integer, result_fractional = result_binary.split('.')
            if '1' not in result_integer and '1' not in result_fractional:
                result_exponent = 0

        text_output.insert(tk.END, "Final Answer:\n")
        text_output.insert(tk.END, f"[{result_binary}] x 2^{result_exponent}\n")

    except Exception as e:
        text_output.insert(tk.END, f"Error: An error occurred: {e}")


#GUI
root = tk.Tk()
root.title("Binary Addition")

#binary 1
label_binary1 = tk.Label(root, text="Input First Binary:")
label_binary1.grid(row=0, column=0, padx=5, pady=5)
entry_binary1 = tk.Entry(root)
entry_binary1.grid(row=0, column=1, padx=5, pady=5)

label_exponent1 = tk.Label(root, text="Input First Exponent:")
label_exponent1.grid(row=1, column=0, padx=5, pady=5)
entry_exponent1 = tk.Entry(root)
entry_exponent1.grid(row=1, column=1, padx=5, pady=5)

#binary 2
label_binary2 = tk.Label(root, text="Input Second Binary:")
label_binary2.grid(row=2, column=0, padx=5, pady=5)
entry_binary2 = tk.Entry(root)
entry_binary2.grid(row=2, column=1, padx=5, pady=5)

label_exponent2 = tk.Label(root, text="Input Second Exponent:")
label_exponent2.grid(row=3, column=0, padx=5, pady=5)
entry_exponent2 = tk.Entry(root)
entry_exponent2.grid(row=3, column=1, padx=5, pady=5)

#rounding mode selection
label_rounding_mode = tk.Label(root, text="Rounding Mode:")
label_rounding_mode.grid(row=4, column=0, padx=5, pady=5)
var_rounding_mode = tk.StringVar(value="GRS")
radio_grs = tk.Radiobutton(root, text="With GRS (Guard, Round, Sticky)", variable=var_rounding_mode, value="GRS")
radio_grs.grid(row=4, column=1, padx=5, pady=5)
radio_rtnte = tk.Radiobutton(root, text="Without GRS (uses RTNTE)", variable=var_rounding_mode, value="RTNTE")
radio_rtnte.grid(row=5, column=1, padx=5, pady=5)

#number of digits
label_num_digits = tk.Label(root, text="Number of Digits Supported:")
label_num_digits.grid(row=6, column=0, padx=5, pady=5)
entry_num_digits = tk.Entry(root)
entry_num_digits.grid(row=6, column=1, padx=5, pady=5)

button_add = tk.Button(root, text="Perform Addition", command=perform_addition)
button_add.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

text_output = tk.Text(root, width=50, height=17)
text_output.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

button_save_output = tk.Button(root, text="Save Output", command=save_output)
button_save_output.grid(row=9, column=0, columnspan=2, padx=5, pady=5)


def test(test_num,
         entry_binary_input_1,
         entry_exponent_input_1,
         entry_binary_input_2,
         entry_exponent_input_2,
         var_rounding_mode_input,
         entry_num_digits_input,
         normal_binary_1,
         normal_expo_1,
         normal_binary_2,
         normal_expo_2,
         same_binary_1,
         same_expo_1,
         same_binary_2,
         same_expo_2,
         round_binary_1,
         round_expo_1,
         round_binary_2,
         round_expo_2,
         sum_binary,
         sum_expo,
         final_binary,
         final_expo):
    entry_binary1.delete(0, tk.END)
    entry_binary2.delete(0, tk.END)
    entry_exponent1.delete(0, tk.END)
    entry_exponent2.delete(0, tk.END)
    entry_num_digits.delete(0, tk.END)
    entry_binary1.insert(0, entry_binary_input_1)
    entry_binary2.insert(0, entry_binary_input_2)
    entry_exponent1.insert(0, entry_exponent_input_1)
    entry_exponent2.insert(0, entry_exponent_input_2)
    entry_num_digits.insert(0, entry_num_digits_input)
    var_rounding_mode.set(var_rounding_mode_input)
    perform_addition()
    res = text_output.get(1.0, tk.END)
    print("Test #" + str(test_num) + ": " + str(res == 
        f"""Normalized Binary Numbers:
Binary 1: [{normal_binary_1}] x 2^{normal_expo_1}
Binary 2: [{normal_binary_2}] x 2^{normal_expo_2}

Same Exponent Binary Numbers:
Binary 1: [{same_binary_1}] x 2^{same_expo_1}
Binary 2: [{same_binary_2}] x 2^{same_expo_2}

Rounded Binary Numbers:
Binary 1: [{round_binary_1}] x 2^{round_expo_1}
Binary 2: [{round_binary_2}] x 2^{round_expo_2}
-------------------------------------------------
     Sum: [{sum_binary}] x 2^{sum_expo}

Final Answer:
[{final_binary}] x 2^{final_expo}

"""))
    entry_binary1.delete(0, tk.END)
    entry_binary2.delete(0, tk.END)
    entry_exponent1.delete(0, tk.END)
    entry_exponent2.delete(0, tk.END)
    entry_num_digits.delete(0, tk.END)
    #text_output.delete(1.0, tk.END)

test(1, "-1.0", "3", "1.0", "3", "GRS", "3", "-1.0", "3", "1.0", "3", "-1.0", "3", "1.0", "3", "-1.00000", "3", "1.00000", "3", "0.00000", "3", "0.00", "0")
test(2, "1.0", "3", "-1.0", "3", "GRS", "3", "1.0", "3", "-1.0", "3", "1.0", "3", "-1.0", "3", "1.00000", "3", "-1.00000", "3", "0.00000", "3", "0.00", "0")
test(3, "-1.0", "3", "-1.0", "3", "GRS", "3", "-1.0", "3", "-1.0", "3", "-1.0", "3", "-1.0", "3", "-1.00000", "3", "-1.00000", "3", "-10.00000", "3", "-1.00", "4")
test(4, "1.0", "3", "1.0", "3", "GRS", "3", "1.0", "3", "1.0", "3", "1.0", "3", "1.0", "3", "1.00000", "3", "1.00000", "3", "10.00000", "3", "1.00", "4")
test(5, "100.1110111001001", "5", "0.01101111101010001", "7", "RTNTE", "10", "1.001110111001001", "7", "1.101111101010001", "5", "1.001110111001001", "7", "0.01101111101010001", "7", "1.001110111", "7", "0.011011111", "7", "1.101010110", "7", "1.101010110", "7")
test(6, "1.0111110010011", "5", "1.00111111100011", "3", "GRS", "9", "1.0111110010011", "5", "1.00111111100011", "3", "1.0111110010011", "5", "0.0100111111100011", "5", "1.01111100101", "5", "0.01001111111", "5", "1.11001100100", "5", "1.11001100", "5")
test(7, "1.0111110010011", "5", "1.00111111100011", "3", "RTNTE", "9", "1.0111110010011", "5", "1.00111111100011", "3", "1.0111110010011", "5", "0.0100111111100011", "5", "1.01111101", "5", "0.01010000", "5", "1.11001101", "5", "1.11001101", "5")
test(8, "100.1110111001001", "5",     "0.0110111110101", "7",     "GRS", "8",      "1.001110111001001", "7",      "1.10111110101", "5",      "1.001110111001001", "7",      "0.0110111110101", "7",      "1.0011101111", "7",      "0.0110111111", "7",      "1.1010101110", "7",      "1.1010110", "7")
test(9, "1.0111110010", "5",     "1.0011111110", "3",     "RTNTE", "7",      "1.0111110010", "5",      "1.0011111110", "3",      "1.0111110010", "5",      "0.010011111110", "5",      "1.011111", "5",      "0.010100", "5",      "1.110011", "5",      "1.110011", "5")
test(10, "100.1110111001001", "5",     "0.0110111110101", "7",     "GRS", "8",      "1.001110111001001", "7",      "1.10111110101", "5",      "1.001110111001001", "7",      "0.0110111110101", "7",      "1.0011101111", "7",      "0.0110111111", "7",      "1.1010101110", "7",      "1.1010110", "7")
test(11, "1.011111001", "5",     "1.0011111110", "3",     "RTNTE", "7",      "1.011111001", "5",      "1.0011111110", "3",      "1.011111001", "5",      "0.010011111110", "5",      "1.011111", "5",      "0.010100", "5",      "1.110011", "5",      "1.110011", "5")
test(12, "100.1110111001001", "5",     "-0.01101111101010001", "7",     "RTNTE", "10",      "1.001110111001001", "7",      "-1.101111101010001", "5",      "1.001110111001001", "7",      "-0.01101111101010001", "7",      "1.001110111", "7",      "-0.011011111", "7",    "0.110011000", "7",     "1.100110000", "6")
test(13, "100.1110111001001", "5",     "-0.01101111101010001", "7",     "GRS", "10",      "1.001110111001001", "7",      "-1.101111101010001", "5",      "1.001110111001001", "7",      "-0.01101111101010001", "7",      "1.001110111001", "7",      "-0.011011111011", "7",    "0.110010111110", "7",     "1.100110000", "6")
test(14, "1.0010", "3",     "-1.0001", "3",     "GRS", "3",      "1.0010", "3",      "-1.0001", "3",      "1.0010", "3",      "-1.0001", "3",      "1.00100", "3",      "-1.00010", "3",    "0.00010", "3",     "1.00", "-1")
test(15, "100.1110111001001", "5",     "0.01101111101010001", "7",     "GRS", "7",      "1.001110111001001", "7",      "1.101111101010001", "5",      "1.001110111001001", "7",      "0.01101111101010001", "7",      "1.001110111", "7",      "0.011011111", "7",    "1.101010110", "7",     "1.101011", "7")
test(16, "1.1111110010", "6", "1.1111100011", "4", "GRS", "5", "1.1111110010", "6", "1.1111100011", "4", "1.1111110010", "6", "0.011111100011", "6", "1.1111111", "6", "0.0111111", "6", "10.0111110", "6", "1.0100", "7")
test(17, "-1.1010", "-2", "-0.101", '-4', "RTNTE", "3", "-1.1010", "-2", "-1.01", "-5", "-1.1010", "-2", "-0.00101", "-2", "-1.10", "-2", "-0.01", "-2", "-1.11", "-2", "-1.11", "-2")
test(18, "-1.1010", "-2", "-0.101", '-4', "GRS", "3", "-1.1010", "-2", "-1.01", "-5", "-1.1010", "-2", "-0.00101", "-2", "-1.10100", "-2", "-0.00101", "-2", "-1.11001", "-2", "-1.11", "-2")
test(19, "-100.1110111001001", "5",     "0.01101111101010001", "7",     "GRS", "10",      "-1.001110111001001", "7",      "1.101111101010001", "5",      "-1.001110111001001", "7",      "0.01101111101010001", "7",      "-1.001110111001", "7",      "0.011011111011", "7",    "-0.110010111110", "7",     "-1.100110000", "6")
test(20, "-1.011111001", "5",     "-1.0011111110", "3",     "RTNTE", "7",      "-1.011111001", "5",      "-1.0011111110", "3",      "-1.011111001", "5",      "-0.010011111110", "5",      "-1.011111", "5",      "-0.010100", "5",      "-1.110011", "5",      "-1.110011", "5")
test(21, "1", "0", "1", "0", "RTNTE", "2", "1.0", "0", "1.0", "0", "1.0", "0", "1.0", "0", "1.0", "0", "1.0", "0", "10.0", "0", "1.0", "1")
test(22, "1", "-3", "1", "-3", "RTNTE", "2", "1.0", "-3", "1.0", "-3", "1.0", "-3", "1.0", "-3", "1.0", "-3", "1.0", "-3", "10.0", "-3", "1.0", "-2")
test(23, "0", "-3", "0", "-3", "RTNTE", "2", "0.0", "-3", "0.0", "-3", "0.0", "-3", "0.0", "-3", "0.0", "-3", "0.0", "-3", "0.0", "-3", "0.0", "0")
test(24, "00.0", "-3", "00.0", "-3", "RTNTE", "2", "0.00", "-2", "0.00", "-2", "0.00", "-2", "0.00", "-2", "0.0", "-2", "0.0", "-2", "0.0", "-2", "0.0", "0")
test(25, "0.1", "0", "0.1", "0", "RTNTE", "2", "1.0", "-1", "1.0", "-1", "1.0", "-1", "1.0", "-1", "1.0", "-1", "1.0", "-1", "10.0", "-1", "1.0", "0",)
test(26, "001.1", "5", "0.000000001", "5", "GRS", "3", "1.1", "5", "1.0", '-4', "1.1", "5", "0.0000000010", "5", "1.10000", "5", "0.00001", "5", "1.10001", "5", "1.10", "5")
test(27, "1100.10", "-4", "0.110010", "5", "GRS", "4", "1.10010", "-1", "1.10010", '4', "0.0000110010", "4", "1.10010", '4', "0.000011", "4", "1.100100", '4', "1.100111", "4", "1.101", "4")


def test_validation(test_num,
         entry_binary_input_1,
         entry_exponent_input_1,
         entry_binary_input_2,
         entry_exponent_input_2,
         var_rounding_mode_input,
         entry_num_digits_input,
         error_message):
    entry_binary1.delete(0, tk.END)
    entry_binary2.delete(0, tk.END)
    entry_exponent1.delete(0, tk.END)
    entry_exponent2.delete(0, tk.END)
    entry_num_digits.delete(0, tk.END)
    entry_binary1.insert(0, entry_binary_input_1)
    entry_binary2.insert(0, entry_binary_input_2)
    entry_exponent1.insert(0, entry_exponent_input_1)
    entry_exponent2.insert(0, entry_exponent_input_2)
    entry_num_digits.insert(0, entry_num_digits_input)
    var_rounding_mode.set(var_rounding_mode_input)
    perform_addition()
    res = text_output.get(1.0, tk.END)
    error_message = error_message + "\n"
    print("Test #V" + str(test_num) + ": " + str(res == error_message))
    entry_binary1.delete(0, tk.END)
    entry_binary2.delete(0, tk.END)
    entry_exponent1.delete(0, tk.END)
    entry_exponent2.delete(0, tk.END)
    entry_num_digits.delete(0, tk.END)
    # text_output.delete(1.0, tk.END)

print()
# Disallow empty inputs for all fields.
test_validation(1, "", "", "", "", "GRS", "", "Error: Please fill in all input fields.")
# Disallow non-binary inputs for binary numbers.
test_validation(2, "2", "3", "1", "3", "GRS", "3", "Error: Incorrect input format for binary 1. \nPlease input binary numbers.")
test_validation(3, "jsdfo", "3", "1", "3", "GRS", "3", "Error: Incorrect input format for binary 1. \nPlease input binary numbers.")
test_validation(4, "1", "3", "sdfb", "3", "GRS", "3", "Error: Incorrect input format for binary 2. \nPlease input binary numbers.")
# Disallow non-integer inputs for exponents.
test_validation(5, "1", "1.1", "1", "3", "GRS", "3", "Error: Incorrect input format for exponent 1. \nPlease input numericals only.")
test_validation(5, "1", "abds", "1", "3", "GRS", "3", "Error: Incorrect input format for exponent 1. \nPlease input numericals only.")
test_validation(5, "1", "3", "1", "1.1", "GRS", "3", "Error: Incorrect input format for exponent 2. \nPlease input numericals only.")
test_validation(5, "1", "3", "1", "abds", "GRS", "3", "Error: Incorrect input format for exponent 2. \nPlease input numericals only.")
# Disallow negative signs not at the start.
test_validation(6, "1-", "3", "1", "3", "GRS", "3", "Error: Incorrect input format for binary 1. \nPlease input binary numbers.")
test_validation(7, "1", "3", "1-", "3", "GRS", "3", "Error: Incorrect input format for binary 2. \nPlease input binary numbers.")
# Disallow multiple negative signs.
test_validation(8, "--1", "3", "1", "3", "GRS", "3", "Error: Incorrect input format for binary 1. \nPlease input binary numbers.")
test_validation(9, "1", "3", "--1", "3", "GRS", "3", "Error: Incorrect input format for binary 2. \nPlease input binary numbers.")
# Disallow multiple binary points.
test_validation(10, "1.1.1", "3", "1", "3", "GRS", "3", "Error: Incorrect input format. \nPlease input binary numbers.")
test_validation(11, "1", "3", "1.1.1", "3", "GRS", "3", "Error: Incorrect input format. \nPlease input binary numbers.")
# Disallow greater than 24 for number of digits supported.
test_validation(12, "1", "3", "1", "3", "GRS", "25", "Error: Number of digits must be between 1 and 24.")
# Disallow exponent greater than 127.
test_validation(13, "1", "128", "1", "3", "GRS", "3", "Error: Exponent 1 must be between -126 and 127.")
# Disallow exponent below -126.
test_validation(14, "1", "-127", "1", "3", "GRS", "3", "Error: Exponent 1 must be between -126 and 127.")

root.mainloop()
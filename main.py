from decimal import *
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

# Float to Binary Conversion
def float_to_binary(float_num, precision):
    integer_part = int(float_num)
    fractional_part = float_num - integer_part

    # Convert integer part to binary
    binary_integer = bin(integer_part).replace("0b", "")

    # Convert fractional part to binary
    binary_fractional = ""
    while fractional_part > 0 and len(binary_fractional) < precision:
        fractional_part *= 2
        bit = int(fractional_part)
        binary_fractional += str(bit)
        fractional_part -= bit

    if len(binary_fractional) == 0:
        return binary_integer
    else:
        return binary_integer + "." + binary_fractional

# Move Decimal Point of a Number given the Shift
# Positive shift: moves the decimal point to the left
# Negative shift: moves the decimal point to the right
def move_decimal_point(binary_str, shift):
    integer_part, fractional_part = binary_str.split('.')
    
    shifted_integer = ''
    shifted_fractional = ''
    
    if '1' not in integer_part and '1' in fractional_part:
        #shift fractional part to the left
        if shift < 0 and fractional_part[0] != '1':
            shifted_integer = '0'
            shifted_fractional = fractional_part[1:] 
            print("shifted_fractional", shifted_fractional)
            return shifted_integer + '.' + shifted_fractional
        elif shift < 0 and fractional_part[0] == '1':
            shifted_integer = '1'
            shifted_fractional = fractional_part[1:]
            return shifted_integer + '.' + shifted_fractional
        

    # Shift the decimal point to the right
    if shift < 0:
        # Pad with zeros if the fractional part is shorter than the shift
        if len(fractional_part) < abs(shift):
            shifted_integer += integer_part + fractional_part
            shifted_integer += '0' * (abs(shift) - len(fractional_part))
            shifted_fractional = fractional_part[abs(shift):]
            
        # Normal shift
        elif len(fractional_part) > abs(shift):
            shifted_integer = integer_part + fractional_part[:abs(shift)]
            shifted_fractional = fractional_part[abs(shift):]
            
        # If the shifted fractional part is empty make it 0
        if len(shifted_fractional) == 0:
            shifted_fractional = '0'
        if len(shifted_integer) == 0:
            shifted_integer = '0'
        
        return shifted_integer + '.' + shifted_fractional
    
    # Shift the decimal point to the left    
    elif shift >= 0:
        if '-' not in integer_part:
            # Pad with zeros if the integer part is shorter than the shift
            if len(integer_part) < abs(shift):
                shifted_fractional = '0' * (abs(shift) - len(integer_part)) + integer_part + fractional_part
                shifted_integer = '0'
                
            # Normal shift
            elif len(integer_part) >= abs(shift):
                shifted_fractional = integer_part[-abs(shift):] + fractional_part
                shifted_integer = integer_part[:-abs(shift)]

            # If the shifted integer part is empty make it 0
            if len(shifted_integer) == 0:
                shifted_integer = '0'
                
            return shifted_integer + '.' + shifted_fractional
        
        elif '-' in integer_part:
            negative = integer_part[:1]
            integer_part = integer_part[1:]
            
            # Pad with zeros if the integer part is shorter than the shift
            if len(integer_part) < abs(shift):
                shifted_fractional = '0' * (abs(shift) - len(integer_part)) + integer_part + fractional_part
                shifted_integer = '0'
                
            # Normal shift
            elif len(integer_part) >= abs(shift):
                shifted_fractional = integer_part[-abs(shift):] + fractional_part
                shifted_integer = integer_part[:-abs(shift)]

            # If the shifted integer part is empty make it 0
            if len(shifted_integer) == 0:
                shifted_integer = '0'
            
            return negative + shifted_integer + '.' + shifted_fractional

# Add Two Binary Numbers
def add_binary_numbers(binary_num1, binary_num2):
    # Split the numbers into integer and fractional parts
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
    
    # Convert the integer parts to decimal
    dec_num1 = Decimal(int(int_part1, 2))
    dec_num2 = Decimal(int(int_part2, 2))
    
    # Convert the fractional parts to decimal
    frac_num1 = Decimal(int(frac_part1, 2)) / Decimal(2 ** len(frac_part1))
    frac_num2 = Decimal(int(frac_part2, 2)) / Decimal(2 ** len(frac_part2)) 
    
    num1 = dec_num1 + frac_num1
    num2 = dec_num2 + frac_num2
    
    if int_neg1:
        num1 = -num1
    if int_neg2:
        num2 = -num2
    
    sum_dec = num1 + num2
    
    # Convert the sum of fractional parts to binary
    sum_binary = float_to_binary(sum_dec, precision=len(frac_part1))
    
    return sum_binary

# Round to the Nearest Even (RTNE) Rounding
def rtne_rounding(binary_str, num_bits):
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
    #truncate to num_bits -1
    #if remaining bits has 1, append 1 to the last bit
    #else, append 0
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
    
    # Shift the decimal point to the right until the first '1' is encountered in the integer part

    if integer_part == '0' and fractional_part == '1':
        return '1.0', exponent - 1
    if integer_part == '0' and fractional_part == '0':
        return '0.0', 0
    
    while '1' not in integer_part and '1' in fractional_part:
        exponent -= 1
        binary_str = integer_part + '.' + fractional_part
        binary_str = move_decimal_point(binary_str, -1)
        print("cc", binary_str)
        #if fractional part is empty, pad 0
        #if integer_part == '0' and fractional_part == '1':
            #return '1.0', exponent - 1
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
        
    return binary_str, exponent

# Normalize Result
def normalize_result(result_binary, result_exponent, num_digits):
    if '.' not in result_binary:
        result_binary += '.0'
    integer_part, fractional_part = result_binary.split('.')
        
        #1.f <- need to check for this
    while integer_part[-1] != '1' and len(integer_part) > 1:
        result_exponent += 1
        result_binary = integer_part + '.' + fractional_part
        result_binary = move_decimal_point(result_binary, 1)
        integer_part, fractional_part = result_binary.split('.')
    while integer_part[-1] != '1' and len(integer_part) > 1:
        result_exponent -= 1
        result_binary = integer_part + '.' + fractional_part
        result_binary = move_decimal_point(result_binary, -1)
        integer_part, fractional_part = result_binary.split('.')   
        
    while len(integer_part) > 1 and '-' not in integer_part:
        result_exponent += 1
        result_binary = integer_part + '.' + fractional_part
        result_binary = move_decimal_point(result_binary, 1)
        integer_part, fractional_part = result_binary.split('.')
    while len(integer_part) > 1 and '-' not in integer_part:
        result_exponent += 1
        result_binary = integer_part + '.' + fractional_part
        result_binary = move_decimal_point(result_binary, 1)
        integer_part, fractional_part = result_binary.split('.')
    result_binary = rtne_rounding(result_binary, num_digits) 
    return result_binary, result_exponent

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

# Perform Addition
def perform_addition():
    try:
        binary1 = entry_binary1.get()
        exponent1 = int(entry_exponent1.get())
        binary2 = entry_binary2.get()
        exponent2 = int(entry_exponent2.get())
        rounding_mode = var_rounding_mode.get()
        num_digits = int(entry_num_digits.get())

        # Clear previous text from the output Text widget
        text_output.delete(1.0, tk.END)

        # Check input validity
        if binary1.count('.') > 1 or binary2.count('.') > 1:
            text_output.insert(tk.END, "Error: Incorrect input format. Please input binary numbers.")
            return
        if len(binary1) == 0 or len(binary2) == 0 or len(entry_exponent1.get()) == 0 or len(entry_exponent2.get()) == 0 or len(entry_num_digits.get()) == 0:
            text_output.insert(tk.END, "Error: Please input both binary numbers and exponents.")
            return

        # Normalize input values
        if '.' not in binary1:
            binary1 += '.0'
        if '.' not in binary2:
            binary2 += '.0'
        
        # Shift the decimal point to make it n.f
        normalize_binary1, exponent1 = normalize_binary(binary1, exponent1)
        normalize_binary2, exponent2 = normalize_binary(binary2, exponent2)

        text_output.insert(tk.END, "Normalized Binary Numbers:\n")
        text_output.insert(tk.END, f"Binary 1: [{normalize_binary1}] x 2^{exponent1}\n")
        text_output.insert(tk.END, f"Binary 2: [{normalize_binary2}] x 2^{exponent2}\n\n")

        # Normalize the binary numbers to the larger exponent
        if exponent1 > exponent2:
            normalize_binary2 = move_decimal_point(normalize_binary2, exponent1 - exponent2)
            exponent2 = exponent1
        elif exponent2 > exponent1:
            normalize_binary1 = move_decimal_point(normalize_binary1, exponent2 - exponent1)
            exponent1 = exponent2
        result_exponent = max(exponent1, exponent2)

        # Display normalized binary numbers
        text_output.insert(tk.END, "Same Exponent Binary Numbers:\n")
        text_output.insert(tk.END, f"Binary 1: [{normalize_binary1}] x 2^{exponent1}\n")
        text_output.insert(tk.END, f"Binary 2: [{normalize_binary2}] x 2^{exponent2}\n\n")

        # Perform rounding based on selected rounding mode
        if rounding_mode == "RTNE":
            round_binary1 = rtne_rounding(normalize_binary1, num_digits)
            round_binary2 = rtne_rounding(normalize_binary2, num_digits)
        elif rounding_mode == "GRS":
            round_binary1 = grs_rounding(normalize_binary1, num_digits)
            round_binary2 = grs_rounding(normalize_binary2, num_digits)

        # Display rounded binary numbers
        text_output.insert(tk.END, "Rounded Binary Numbers:\n")
        text_output.insert(tk.END, f"Binary 1: [{round_binary1}] x 2^{exponent1}\n")
        text_output.insert(tk.END, f"Binary 2: [{round_binary2}] x 2^{exponent2}\n")

        # Perform addition
        if '.' not in round_binary1:
            round_binary1 += '.0'
        if '.' not in round_binary2:
            round_binary2 += '.0'
        result_binary = add_binary_numbers(round_binary1, round_binary2)
        result_exponent = max(exponent1, exponent2)
        text_output.insert(tk.END, "-------------------------------------------------\n")
        if num_digits > 1:
            if '.' not in result_binary:
                result_binary += '.0'
            if len(result_binary) < num_digits+4 and rounding_mode == "GRS":
                result_binary += '0' * (num_digits+4 - len(result_binary))
            elif len(result_binary) < num_digits+1 and rounding_mode == "RTNE":
                result_binary += '0' * (num_digits+1 - len(result_binary))
        text_output.insert(tk.END, f"     Sum: [{result_binary}] x 2^{result_exponent}\n\n")

        # Normalize the result
        
        
        result_binary, result_exponent = normalize_result(result_binary, result_exponent, num_digits)

        # Display final result
        text_output.insert(tk.END, "Final Answer:\n")
        text_output.insert(tk.END, f"[{result_binary}] x 2^{result_exponent}\n")

        #save_output(text_output.get(1.0, tk.END))

    except Exception as e:
        text_output.insert(tk.END, f"Error: An error occurred: {e}")


# GUI setup
root = tk.Tk()
root.title("Binary Addition")

# Operand 1 inputs
label_binary1 = tk.Label(root, text="Input First Binary:")
label_binary1.grid(row=0, column=0, padx=5, pady=5)
entry_binary1 = tk.Entry(root)
entry_binary1.grid(row=0, column=1, padx=5, pady=5)

label_exponent1 = tk.Label(root, text="Input First Exponent:")
label_exponent1.grid(row=1, column=0, padx=5, pady=5)
entry_exponent1 = tk.Entry(root)
entry_exponent1.grid(row=1, column=1, padx=5, pady=5)

# Operand 2 inputs
label_binary2 = tk.Label(root, text="Input Second Binary:")
label_binary2.grid(row=2, column=0, padx=5, pady=5)
entry_binary2 = tk.Entry(root)
entry_binary2.grid(row=2, column=1, padx=5, pady=5)

label_exponent2 = tk.Label(root, text="Input Second Exponent:")
label_exponent2.grid(row=3, column=0, padx=5, pady=5)
entry_exponent2 = tk.Entry(root)
entry_exponent2.grid(row=3, column=1, padx=5, pady=5)

# Rounding mode selection
label_rounding_mode = tk.Label(root, text="Rounding Mode:")
label_rounding_mode.grid(row=4, column=0, padx=5, pady=5)
var_rounding_mode = tk.StringVar(value="GRS")  # Default to GRS rounding
radio_grs = tk.Radiobutton(root, text="GRS (Guard, Round, Sticky)", variable=var_rounding_mode, value="GRS")
radio_grs.grid(row=4, column=1, padx=5, pady=5)
radio_rtne = tk.Radiobutton(root, text="RTNE (Round to Nearest Even)", variable=var_rounding_mode, value="RTNE")
radio_rtne.grid(row=5, column=1, padx=5, pady=5)

# Number of digits supported
label_num_digits = tk.Label(root, text="Number of Digits Supported:")
label_num_digits.grid(row=6, column=0, padx=5, pady=5)
entry_num_digits = tk.Entry(root)
entry_num_digits.grid(row=6, column=1, padx=5, pady=5)

# Perform addition button
button_add = tk.Button(root, text="Perform Addition", command=perform_addition)
button_add.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

# Output Text widget
text_output = tk.Text(root, width=50, height=15)
text_output.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

button_save_output = tk.Button(root, text="Save Output", command=save_output)
button_save_output.grid(row=9, column=0, columnspan=2, padx=5, pady=5)


root.mainloop()

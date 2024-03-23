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
    

    if integer_part == '0' and fractional_part == '1':
        return '1.0', exponent - 1
    if integer_part == '0' and fractional_part == '0':
        return '0.0', 0
    
    while '1' not in integer_part and '1' in fractional_part:
        exponent -= 1
        binary_str = integer_part + '.' + fractional_part
        binary_str = move_decimal_point(binary_str, -1)
        print("cc", binary_str)
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

        binary1 = entry_binary1.get()
        exponent1 = int(entry_exponent1.get())
        binary2 = entry_binary2.get()
        exponent2 = int(entry_exponent2.get())
        rounding_mode = var_rounding_mode.get()
        num_digits = int(entry_num_digits.get())


        #check input validity
        if binary1.count('.') > 1 or binary2.count('.') > 1:
            text_output.insert(tk.END, "Error: Incorrect input format. Please input binary numbers.")
            return
        if len(binary1) == 0 or len(binary2) == 0 or len(entry_exponent1.get()) == 0 or len(entry_exponent2.get()) == 0 or len(entry_num_digits.get()) == 0:
            text_output.insert(tk.END, "Error: Please input both binary numbers and exponents.")
            return
        
        for char in binary1:
            if char not in '01.-':
                text_output.insert(tk.END, "Error: Incorrect input format. Please input binary numbers.")
                return
        for char in binary2:
            if char not in '01.-':
                text_output.insert(tk.END, "Error: Incorrect input format. Please input binary numbers.")
                return

        if num_digits > 24 or num_digits < 1:
            text_output.insert(tk.END, "Error: Number of digits must be between 1 and 24.")
            return
        
        if binary1.count('-') > 1:
            print("binary1", binary1)
            text_output.insert(tk.END, "Error: Incorrect input format. Please input binary numbers.")
            return
        if binary2.count('-') > 1:
            print("binary2", binary2)
            text_output.insert(tk.END, "Error: Incorrect input format. Please input binary numbers.")
            return
        
        if binary1.find('-') != 0 and binary1.find('-') != -1:
            print(binary1.find('-'))
            print("binary1-", binary1)
            text_output.insert(tk.END, "Error: Incorrect input format. Please input binary numbers.")
            return
        if binary2.find('-') != 0 and binary2.find('-') != -1:
            print("binary2-", binary2)
            text_output.insert(tk.END, "Error: Incorrect input format. Please input binary numbers.")
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
        if rounding_mode == "RTNE":
            round_binary1 = rtne_rounding(normalize_binary1, num_digits)
            round_binary2 = rtne_rounding(normalize_binary2, num_digits)
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
        print( len(fractional_part_round))
        text_output.insert(tk.END, f"     Sum: [{result_binary}] x 2^{result_exponent}\n\n")

        #normalizing answer
        if '.' not in result_binary:
            result_binary += '.0'
        result_binary, result_exponent = normalize_binary(result_binary, result_exponent)
        result_binary = rtne_rounding(result_binary, num_digits) 

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
radio_grs = tk.Radiobutton(root, text="GRS (Guard, Round, Sticky)", variable=var_rounding_mode, value="GRS")
radio_grs.grid(row=4, column=1, padx=5, pady=5)
radio_rtne = tk.Radiobutton(root, text="RTNE (Round to Nearest Even)", variable=var_rounding_mode, value="RTNE")
radio_rtne.grid(row=5, column=1, padx=5, pady=5)

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

root.mainloop()

print(move_decimal_point('101.101', 0))

# Tests for functions...
print()
print("Test for move_decimal_point")
print("1. " + move_decimal_point('101.101', -4) + " == 1011010.0 is " + str(move_decimal_point('101.101', -4) == '1011010.0'))
print("2. " + move_decimal_point('101.101', -3) + " == 101101.0 is " + str(move_decimal_point('101.101', -3) == '101101.0'))
print("3. " + move_decimal_point('101.101', -2) + " == 10110.1 is " + str(move_decimal_point('101.101', -2) == '10110.1'))
print("4. " + move_decimal_point('101.101', -1) + " == 1011.01 is " + str(move_decimal_point('101.101', -1) == '1011.01'))
print("5. " + move_decimal_point('101.101', 0) + " == 101.101 is " + str(move_decimal_point('101.101', 0) == '101.101'))
print("6. " + move_decimal_point('101.101', 1) + " == 10.1101 is " + str(move_decimal_point('101.101', 1) == '10.1101'))
print("7. " + move_decimal_point('101.101', 2) + " == 1.01101 is " + str(move_decimal_point('101.101', 2) == '1.01101'))
print("8. " + move_decimal_point('101.101', 3) + " == 0.101101 is " + str(move_decimal_point('101.101', 3) == '0.101101'))
print("9. " + move_decimal_point('101.101', 4) + " == 0.0101101 is " + str(move_decimal_point('101.101', 4) == '0.0101101'))
print("10. " + move_decimal_point('0.0101', -4) + " == 101.0 is " + str(move_decimal_point('0.0101', -4) == '101.0'))
print("11. " + move_decimal_point('0.0101', -3) + " == 10.1 is " + str(move_decimal_point('0.0101', -3) == '10.1'))
print("12. " + move_decimal_point('0.0101', -2) + " == 1.01 is " + str(move_decimal_point('0.0101', -2) == '1.01'))
print("13. " + move_decimal_point('0.0101', -1) + " == 0.101 is " + str(move_decimal_point('0.0101', -1) == '0.101'))
print("14. " + move_decimal_point('0.0101', 0) + " == 0.0101 is " + str(move_decimal_point('0.0101', 0) == '0.0101'))
print("15. " + move_decimal_point('0.0101', 1) + " == 0.00101 is " + str(move_decimal_point('0.0101', 1) == '0.00101'))
print("16. " + move_decimal_point('0.0101', 2) + " == 0.000101 is " + str(move_decimal_point('0.0101', 2) == '0.000101'))
print("17. " + move_decimal_point('0.0101', 3) + " == 0.0000101 is " + str(move_decimal_point('0.0101', 3) == '0.0000101'))
print("18. " + move_decimal_point('0.0101', 4) + " == 0.00000101 is " + str(move_decimal_point('0.0101', 4) == '0.00000101'))

print()
print("Test for add_binary_numbers")
print("1. " + add_binary_numbers('101.101', '110.011') + " == 1100.000 is " + str(add_binary_numbers('101.101', '110.011') == '1100.000'))
print("2. " + add_binary_numbers('0.101', '0.011') + " == 1.000 is " + str(add_binary_numbers('0.101', '0.011') == '1.000'))
print("3. " + add_binary_numbers('101.101', '0.011') + " == 101.000 is " + str(add_binary_numbers('101.101', '0.011') == '101.000'))



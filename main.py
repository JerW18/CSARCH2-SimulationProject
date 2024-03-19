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
    
    # Shift the decimal point to the right
    if shift < 0:
        # Pad with zeros if the fractional part is shorter than the shift
        if len(fractional_part) < shift:
            shifted_integer += integer_part + fractional_part
            shifted_integer += '0' * (shift - len(fractional_part))
            shifted_fractional = fractional_part[shift:]
            
        # Normal shift
        elif len(fractional_part) > shift:
            shifted_integer += fractional_part[:shift]
            shifted_fractional = fractional_part[shift:]
            
        # If the shifted fractional part is empty make it 0
        if len(shifted_fractional) == 0:
            shifted_fractional = '0'
    
    # Shift the decimal point to the left    
    elif shift >= 0:
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

# Add Two Binary Numbers
def add_binary_numbers(binary_num1, binary_num2):
    # Split the numbers into integer and fractional parts
    int_part1, frac_part1 = binary_num1.split('.')
    int_part2, frac_part2 = binary_num2.split('.')
    
    # Convert the integer parts to decimal
    dec_num1 = int(int_part1, 2)
    dec_num2 = int(int_part2, 2)
    
    # Convert the fractional parts to decimal
    frac_num1 = int(frac_part1, 2) / (2 ** len(frac_part1))
    frac_num2 = int(frac_part2, 2) / (2 ** len(frac_part2))
    
    sum_dec = dec_num1 + dec_num2 + frac_num1 + frac_num2
    
    # Convert the sum of fractional parts to binary
    sum_binary = float_to_binary(sum_dec, precision=len(frac_part1))
    
    return sum_binary

# Round to the Nearest Even (RTNE) Rounding
def rtne_rounding(binary_str, num_bits):
    integer_part, fractional_part = binary_str.split('.')
    
    num_bits = num_bits - 1
    print("workinga")
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
        
    integer_part, fractional_part = binary_str.split('.')
    print("workingb")
    if len(fractional_part) < num_bits:
        fractional_part += '0' * (num_bits - len(fractional_part))
        return integer_part + '.' + fractional_part
    else:
        return binary_str

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
            round_bits + '1'
        else:
            #append 0 to the last bit
            round_bits + '0'
    else:
        round_bits = fractional_part
        #append 0's
        round_bits += '0' * (num_bits - len(fractional_part))
        round_bits += '0'
    
    return integer_part + '.' + round_bits
    # if len(fractional_part) > num_bits:
    #     round_bits, extra_bits = fractional_part[:num_bits], fractional_part[num_bits:]
        
    #     if extra_bits[0] == '1' and not any(bit in '1' for bit in extra_bits[1:]):
    #         if round_bits[-1] == '1':
    #             binary_str = add_binary_numbers(integer_part + '.' + round_bits, '0.' + '0' * (num_bits - 1) + '1')
    #         else:
    #             binary_str = integer_part + '.' + round_bits
                
    #     elif extra_bits[0] == '1' and any(bit in '1' for bit in extra_bits[1:]):
    #         binary_str = add_binary_numbers(integer_part + '.' + round_bits, '0.' + '0' * (num_bits - 1) + '1')
            
    #     else:
    #         binary_str = integer_part + '.' + round_bits


    

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

def perform_addition():
    try:
        binary1 = entry_binary1.get()
        exponent1 = int(entry_exponent1.get())
        binary2 = entry_binary2.get()
        exponent2 = int(entry_exponent2.get())
        rounding_mode = var_rounding_mode.get()
        num_digits = int(entry_num_digits.get())

        #messagebox.showinfo("Converted Binary Numbers", f"Binary 1: {binary1}\nBinary 2: {binary2}")

        # check which exponent is larger
        if exponent1 > exponent2:
            binary2 = move_decimal_point(binary2, exponent1 - exponent2)
            exponent2 = exponent1
        elif exponent2 > exponent1:
            binary1 = move_decimal_point(binary1, exponent2 - exponent1)
            exponent1 = exponent2
        result_exponent = max(exponent1, exponent2)

        result_binary1 = f"[{binary1}] × 2^[{result_exponent}]"
        result_binary2 = f"[{binary2}] × 2^[{result_exponent}]"
        messagebox.showinfo("Normalized Binary Numbers", f"Binary 1: {result_binary1}\nBinary 2: {result_binary2}")


        
        
        if(rounding_mode == "RTNE"):
            binary1 = rtne_rounding(binary1, num_digits)
            binary2 = rtne_rounding(binary2, num_digits)
        elif(rounding_mode == "GRS"):
            binary1 = grs_rounding(binary1, num_digits)
            binary2 = grs_rounding(binary2, num_digits)

        # show converted binary numbers
        result_binary1 = f"[{binary1}] × 2^[{result_exponent}]"
        result_binary2 = f"[{binary2}] × 2^[{result_exponent}]"
        messagebox.showinfo("Rounded Binary Numbers", f"Binary 1: {result_binary1}\nBinary 2: {result_binary2}")

        # Perform addition
        #result_binary = float(binary1) + float(binary2)

        result_binary = add_binary_numbers(binary1, binary2)
        if '.' not in result_binary:
            result_binary += '.0'
        result_binary = f"[{result_binary}] × 2^[{result_exponent}]"
        messagebox.showinfo("Operation", f"Binary 1: {result_binary1}\nBinary 2: {result_binary2}\n--------------------------\nSUM: {result_binary}")
        print("working outside")

        # normalize the result

        print(result_binary)
        #if result_binary has no decimal, pad 0
        if '.' not in result_binary:
            result_binary += '.0'
        integer_part, fractional_part = result_binary.split('.')
        
        #1.f <- need to check for this
        #print(integer_part)
        while integer_part[-1] != '1' and len(integer_part) > 1:
            result_exponent += 1
            result_binary = integer_part + '.' + fractional_part
            result_binary = move_decimal_point(result_binary, 1)
            integer_part, fractional_part = result_binary.split('.')

        while integer_part[-1] != '1':
            result_exponent -= 1
            result_binary = integer_part + '.' + fractional_part
            result_binary = move_decimal_point(result_binary, -1)
            integer_part, fractional_part = result_binary.split('.')   
        
        
        result_binary = rtne_rounding(result_binary, num_digits) 
        # Display the result
        result_str = f"[{result_binary}] × 2^[{result_exponent}]"
        messagebox.showinfo("Result", f"The result is: {result_str}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

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

root.mainloop()
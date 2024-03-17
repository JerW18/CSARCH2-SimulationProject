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
# Positive shift: moves the decimal point to the right
# Negative shift: moves the decimal point to the left
def move_decimal_point(binary_str, shift):
    integer_part, fractional_part = binary_str.split('.')
    
    shifted_integer = ''
    shifted_fractional = ''
    
    # Shift the decimal point to the right
    if shift >= 0:
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
    elif shift < 0:
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
    
    if len(fractional_part) > num_bits:
        round_bits, extra_bits = fractional_part[:num_bits], fractional_part[num_bits:]
        
        if extra_bits[0] == '1':
            if round_bits[-1] == '1':
                binary_str = add_binary_numbers(integer_part + '.' + round_bits, '0.' + '0' * (num_bits - 1) + '1')
            else:
                binary_str = integer_part + '.' + round_bits
        else:
            binary_str = integer_part + '.' + round_bits
        
    integer_part, fractional_part = binary_str.split('.')
    
    if len(fractional_part) < num_bits:
        fractional_part += '0' * (num_bits - len(fractional_part))
        return integer_part + '.' + fractional_part
    else:
        return binary_str
    
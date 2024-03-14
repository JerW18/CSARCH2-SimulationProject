# Float to Binary Conversion
def float_to_binary(float_num, precision = 8):
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
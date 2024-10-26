import random

# Step 1: Generate a random 56-bit key
def generate_key():
    return ''.join(random.choice('01') for _ in range(56))

# Initial and Final Permutation tables (placeholders)
INITIAL_PERMUTATION = list(range(64))
FINAL_PERMUTATION = list(range(64))

# Expansion Table, S-Box placeholders, Permutation (P-Table), etc.
EXPANSION_TABLE = list(range(48))
S_BOXES = [[list(range(16)) for _ in range(4)] for _ in range(8)]
PERMUTATION_P = list(range(32))

# Initial Permutation
def initial_permutation(block):
    return ''.join(block[i] for i in INITIAL_PERMUTATION)

# Final Permutation
def final_permutation(block):
    return ''.join(block[i] for i in FINAL_PERMUTATION)

# Expansion function for 32-bit to 48-bit
def expansion(half_block):
    return ''.join(half_block[i % len(half_block)] for i in EXPANSION_TABLE)

# S-Box substitution placeholder
def s_box_substitution(expanded_half_block):
    # Substitute 48-bit expanded block with S-box transformation
    return expanded_half_block[:32]  # Placeholder

# P-Permutation placeholder
def permutation_p(substituted_block):
    return ''.join(substituted_block[i] for i in PERMUTATION_P)

# DES Feistel function
def feistel_function(right_half, subkey):
    expanded_half = expansion(right_half)
    # XOR with subkey (assuming subkey is 48-bit)
    xored = ''.join(str(int(a) ^ int(b)) for a, b in zip(expanded_half, subkey))
    substituted = s_box_substitution(xored)
    return permutation_p(substituted)

# Generate 16 subkeys (56-bit key to 48-bit subkeys)
def generate_subkeys(key):
    return [key[:48] for _ in range(16)]  # Placeholder for real key scheduling

# DES Encoding
def encode_block(block, key):
    block = initial_permutation(block)
    left, right = block[:32], block[32:]
    subkeys = generate_subkeys(key)
    for i in range(16):
        temp_right = feistel_function(right, subkeys[i])
        new_right = ''.join(str(int(a) ^ int(b)) for a, b in zip(left, temp_right))
        left, right = right, new_right
    return final_permutation(right + left)

# DES Decoding (reversed subkeys)
def decode_block(block, key):
    block = initial_permutation(block)
    left, right = block[:32], block[32:]
    subkeys = generate_subkeys(key)[::-1]
    for i in range(16):
        temp_right = feistel_function(right, subkeys[i])
        new_right = ''.join(str(int(a) ^ int(b)) for a, b in zip(left, temp_right))
        left, right = right, new_right
    return final_permutation(right + left)

# Convert text to binary representation (simplified)
def text_to_bin(text):
    binary_text = ''.join(f"{ord(c):08b}" for c in text)
    # Pad binary string to ensure it is a multiple of 64 bits
    if len(binary_text) % 64 != 0:
        padding_length = 64 - (len(binary_text) % 64)
        binary_text += '0' * padding_length
    return binary_text
# Convert binary back to text
def bin_to_text(binary_data):
    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    text = ''.join(chr(int(char, 2)) for char in chars)
    # Strip any trailing null characters that might have been padding
    return text.rstrip('\x00')

# Encode and decode text
def encode_text(text, key):
    binary_text = text_to_bin(text)
    encoded_blocks = [encode_block(binary_text[i:i+64], key) for i in range(0, len(binary_text), 64)]
    return ''.join(encoded_blocks)

def decode_text(encoded_binary, key):
    decoded_blocks = [decode_block(encoded_binary[i:i+64], key) for i in range(0, len(encoded_binary), 64)]
    return bin_to_text(''.join(decoded_blocks))

# Save encoded and decoded results to files
def save_to_file(filename, content):
    with open(filename, 'w') as f:
        f.write(content)

# Main processing
text = ("From fairest creatures we desire increase, That thereby beauty's rose might never die, "
        "But as the riper should by time decease, His tender heir might bear his memory: "
        "But thou contracted to thine own bright eyes, Feed'st thy light's flame with self-substantial fuel, "
        "Making a famine where abundance lies, Thy self thy foe, to thy sweet self too cruel: "
        "Thou that art now the world's fresh ornament, And only herald to the gaudy spring, "
        "Within thine own bud buriest thy content, And tender churl mak'st waste in niggarding: "
        "Pity the world, or else this glutton be, To eat the world's due, by the grave and thee. "
        "When forty winters shall besiege thy brow, And dig deep trenches in thy beauty's field, "
        "Thy youth's proud livery so gazed on now, Will be a tattered weed of small worth held: "
        "Then being asked, where all thy beauty lies, Where all the treasure of thy lusty days; "
        "To say within thine own deep sunken eyes, Were an all-eating shame, and thriftless praise.")

key = generate_key()
encoded_text = encode_text(text, key)
decoded_text = decode_text(encoded_text, key)

# Save results
save_to_file("encoded_text.txt", encoded_text)
save_to_file("decoded_text.txt", decoded_text)


import bitarray
import math

def build_dictionary(text):
    # Сбор статистики частот символов
    freq = {}
    for char in text:
        if char in freq:
            freq[char] += 1
        else:
            freq[char] = 1

    # Определение фиксированной длины кода
    n = len(freq)
    code_length = math.ceil(math.log2(n))

    # Построение кодовой таблицы
    huffman_codes = {}
    binary_format = '{:0' + str(code_length) + 'b}'
    for i, char in enumerate(freq):
        huffman_codes[char] = binary_format.format(i)

    return huffman_codes

def huffman_encode(string):
    huffman_dict = build_dictionary(string)
    compressed = ''.join(huffman_dict[symbol] for symbol in string)
    return compressed, huffman_dict
"""
def huffman_decode(compressed, huffman_dict):
    reverse_dict = {code: symbol for symbol, code in huffman_dict.items()}
    temp = ''
    decompressed = ''
    for bit in compressed:
        temp += bit
        for code, symbol in reverse_dict.items():
            if temp == code:
                decompressed += str(symbol)
                temp = ''
                break
    return decompressed
"""
def huffman_decode(encoded_data, codes):
    reverse_codes = {v: k for k, v in codes.items()}
    decoded_data = ""
    temp = ""
    for bit in encoded_data:
        temp += bit
        if temp in reverse_codes:
            decoded_data += reverse_codes[temp]
            temp = ""
    return decoded_data

def compress_file_huffman(file_path):
    with open(file_path, 'r') as file:
        string = file.read()
    compressed, huffman_dict = huffman_encode(string)
    bit_array = bitarray.bitarray()
    for code in compressed:
        bit_array.append(int(code))
    with open(file_path.replace('.txt', '.bin'), 'wb') as file:
        bit_array.tofile(file)
    return huffman_dict

def decompress_file_huffman(file_path, huffman_dict):
    with open(file_path, 'rb') as file:
        bit_array = bitarray.bitarray()
        bit_array.fromfile(file)
        compressed = ''.join(str(bit) for bit in bit_array)
    print(huffman_dict)
    decompressed = huffman_decode(compressed, huffman_dict)
    with open(file_path.replace('.bin', '.decompressed'), 'w') as file:
        file.write(decompressed)

huffman_dict = compress_file_huffman('test.txt')
decompress_file_huffman('test.bin', huffman_dict)
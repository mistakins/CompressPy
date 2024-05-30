import bitarray
import math

class LZ77:
    def __init__(self, window_size=20):
        self.window_size = window_size

    def compress(self, input_data):
        i = 0
        output = []
        while i < len(input_data):
            match = self._find_longest_match(input_data, i)
            if match:
                (best_match_distance, best_match_length) = match
                next_symbol = input_data[i + best_match_length]
                output.append((best_match_distance, best_match_length, next_symbol))
                i += best_match_length + 1
            else:
                output.append((0, 0, input_data[i]))
                i += 1
        return output

    def decompress(self, compressed_data):
        decompressed_data = []
        for item in compressed_data:
            (distance, length, symbol) = item
            if distance > 0:
                start = len(decompressed_data) - distance
                for j in range(length):
                    decompressed_data.append(decompressed_data[start + j])
            decompressed_data.append(symbol)
        return ''.join(decompressed_data)

    def _find_longest_match(self, data, current_position):
        end_of_buffer = min(current_position + self.window_size, len(data))
        best_match_distance = -1
        best_match_length = -1
        for j in range(current_position + 1, end_of_buffer):
            start_index = max(0, current_position - self.window_size)
            substring = data[current_position:j]
            for i in range(start_index, current_position):
                match_length = 0
                while match_length < len(substring) and data[i + match_length] == substring[match_length]:
                    match_length += 1
                if match_length > best_match_length:
                    best_match_distance = current_position - i
                    best_match_length = match_length
        if best_match_distance > 0 and best_match_length > 0:
            return best_match_distance, best_match_length
        return None

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

def huffman_decode(compressed, huffman_dict):
    reverse_dict = {code: symbol for symbol, code in huffman_dict.items()}
    temp = ''
    decompressed = []
    for bit in compressed:
        temp += bit
        for code, symbol in reverse_dict.items():
            if temp == code:
                decompressed.append(symbol)
                temp = ''
                break
    return decompressed

def read_from_file(filename):
    with open(filename, 'r') as file:
        return file.read()

def write_to_file(filename, text):
    with open(filename, 'w') as file:
        file.write(str(text))

def compress_file_huffman(file_path):
    lz77 = LZ77(window_size=100)
    compressed, huffman_dict = huffman_encode(lz77.compress(read_from_file(file_path)))
    bit_array = bitarray.bitarray()
    for code in compressed:
        bit_array.append(int(code))
    with open(file_path + '.bin', 'wb') as file:
        bit_array.tofile(file)
    return huffman_dict, lz77

def decompress_file_huffman(file_path, huffman_dict, lz77):
    with open(file_path, 'rb') as file:
        bit_array = bitarray.bitarray()
        bit_array.fromfile(file)
        compressed = ''.join(str(bit) for bit in bit_array)
    write_to_file(file_path, lz77.decompress(huffman_decode(compressed, huffman_dict)))



huffman_dict, lz77 = compress_file_huffman('/home/gautama/LAB_AASD/MYLABPY/test.txt')
decompress_file_huffman('/home/gautama/LAB_AASD/MYLABPY/test.txt.bin', huffman_dict, lz77)
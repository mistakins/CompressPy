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

def read_from_file(filename):
    with open(filename, 'r') as file:
        return file.read()

def write_to_file(filename, text):
    with open(filename, 'w') as file:
        file.write(str(text))

lz77 = LZ77(window_size=200)
input_data = read_from_file('test.txt')
compressed_data = lz77.compress(input_data)

with open('test.lz77', 'wb') as file:
    for item in compressed_data:
        byte_distance = item[0].to_bytes(1, byteorder='big')
        byte_length = item[1].to_bytes(1, byteorder='big')
        byte_symbol = item[2].encode('utf-8')
        file.write(byte_distance + byte_length + byte_symbol)

loaded_compressed_data = []

with open('test.lz77', 'rb') as file:
    while True:
        byte_distance = file.read(1)
        byte_length = file.read(1)
        byte_symbol = file.read(1)
        
        if not byte_symbol:
            break
        
        distance = int.from_bytes(byte_distance, byteorder='big')
        length = int.from_bytes(byte_length, byteorder='big')
        symbol = byte_symbol.decode('utf-8')
        
        loaded_compressed_data.append((distance, length, symbol))

decompressed_data = lz77.decompress(loaded_compressed_data)

write_to_file('test.decompressed', decompressed_data)
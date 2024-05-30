def rle_encoding(data):
    encoded_data = ''
    i = 0
    while i < len(data):
        count = 1
        while i + 1 < len(data) and data[i] == data[i + 1]:
            i += 1
            count += 1
        if count == 1:
            encoded_data += data[i]
        else:
            encoded_data += str(count) + data[i]
        i += 1
    return encoded_data

def rle_decoding(encoded):
    decoded = ''
    count = ''
    for char in encoded:
        if char.isdigit():
            count += char
        else:
            if count == '':
                decoded += char
            else:
                decoded += char * int(count)
                count = ''
    return decoded

def compress_file_rle(file_path):
    with open(file_path, 'r') as file:
        string = file.read()
    encoded = rle_encoding(string)
    with open(file_path.replace('.txt', '.rle'), 'w') as file:
        file.write(encoded)

def decompress_file_rle(file_path):
    with open(file_path, 'r') as file:
        encoded = file.read()
    decoded = rle_decoding(encoded)
    with open(file_path.replace('.rle', '.decompressed'), 'w') as file:
        file.write(decoded)

compress_file_rle('test.txt')
decompress_file_rle('test.rle')
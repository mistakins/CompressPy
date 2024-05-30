import bitarray
import math

def compute_suffix_array(input_text, len_text):
    # Создание массива суффиксов: для каждой позиции i в тексте сохраняется кортеж (i, input_text[i:])
    suff = [(i, input_text[i:]) for i in range(len_text)] 
    # Сортировка суффиксов по их значению (лексикографически)
    suff.sort(key=lambda x: x[1]) 
    # Создание массива индексов отсортированных суффиксов
    suffix_arr = [i for i, _ in suff]   
    return suffix_arr

def find_last_char(input_text, suffix_arr, n):
    # Поиск последнего символа каждого циклического вращения
    bwt_arr = ""
    for i in range(n):
        j = suffix_arr[i] - 1
        if j < 0:
            j = j + n
        bwt_arr += input_text[j]
    return bwt_arr
 
def inverse_burrows_wheeler_transform(bwt_arr):
    len_bwt = len(bwt_arr)
    i = 0
    # Находим индекс символа "$", который указывает на начало строки в преобразованном тексте
    while bwt_arr[i] != "$":
         i+=1 
    x = i
    # Сортировка символов в BWT для построения таблицы сдвигов
    sorted_bwt = sorted(bwt_arr)
    l_shift = [0] * len_bwt
 
    # Создание списка списков для хранения индексов символов в BWT
    arr = [[] for i in range(128)]

    # Наполнение arr индексами символов в BWT
    for i in range(len_bwt):
        arr[ord(bwt_arr[i])].append(i)
 
    # Создание таблицы сдвигов
    for i in range(len_bwt):
        l_shift[i] = arr[ord(sorted_bwt[i])].pop(0)
 
    # Декодирование BWT с использованием таблицы сдвигов
    decoded = [''] * len_bwt
    for i in range(len_bwt):
        x = l_shift[x]
        decoded[len_bwt-1-i] = bwt_arr[x]
    decoded_str = ''.join(decoded)
    # Инвертирование полученной строки и удаление символа "$" в конце
    decoded_str = decoded_str[::-1]
    return decoded_str[:-1]

def burrows_wheeler_transform(input_text):
    # Добавление символа "$" в конец входного текста
    input_text += "$"
    len_text = len(input_text)
    # Вычисление массива суффиксов для входного текста
    suffix_arr = compute_suffix_array(input_text, len_text)
    # Поиск последнего символа каждого циклического вращения (построение BWT)
    bwt_arr = find_last_char(input_text, suffix_arr, len_text)
    return bwt_arr

def mtf(text):
    alphabet = [chr(i) for i in range(256)]  # Создаем алфавит ASCII-символов
    result = []
    for char in text:
        index = alphabet.index(char)  # Находим индекс символа в алфавите
        result.append(index)  # Добавляем индекс в результат
        alphabet.pop(index)  # Удаляем символ из алфавита
        alphabet.insert(0, char)  # Перемещаем символ в начало алфавита
    return result

def inverse_mtf(indices):
    alphabet = [chr(i) for i in range(256)]  # Создаем алфавит ASCII-символов
    result = []
    for index in indices:
        char = alphabet[index]  # Получаем символ по индексу из алфавита
        result.append(char)  # Добавляем символ в результат
        alphabet.pop(index)  # Удаляем символ из алфавита
        alphabet.insert(0, char)  # Перемещаем символ в начало алфавита
    return ''.join(result)


def encode_rle(pixels):
    encoded = []
    i = 0
    while i < len(pixels) - 1:
        count = 1
        while pixels[i] == pixels[i+1]:
            i += 1
            count += 1
        if count == 1:
            encoded.append((pixels[i]))
        else:
            encoded.append((pixels[i], count))
        i += 1
    return encoded

def decode_rle(encoded):
    decoded = []
    for pixel in encoded:
        if isinstance(pixel, tuple) and len(pixel) == 2:
            decoded.extend([pixel[0]] * pixel[1])
        else:
            decoded.append(pixel)
    return decoded

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

def huffman_encode(list):
    huffman_dict = build_dictionary(list)
    compressed = ''.join(huffman_dict[symbol] for symbol in list)
    bit_array = bitarray.bitarray()
    for code in compressed:
        bit_array.append(int(code))
    return bit_array, huffman_dict

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

def compress_file_bwt_mtf_ha(file_path):
    with open(file_path, 'r') as file:
        string = file.read()
    compressed, huffman_dict = huffman_encode(mtf(burrows_wheeler_transform(string)))
    with open(file_path.replace('.txt', '.bin'), 'wb') as file:
        compressed.tofile(file)
    return huffman_dict

def decompress_file_bwt_mtf_ha(file_path, huffman_dict):
    with open(file_path, 'rb') as file:
        bit_array = bitarray.bitarray()
        bit_array.fromfile(file)
        compressed = ''.join(str(bit) for bit in bit_array)
    decoded = inverse_burrows_wheeler_transform(inverse_mtf(huffman_decode(compressed, huffman_dict)))
    with open(file_path.replace('.bin', '.decompressed'), 'w') as file:
        file.write(decoded)

huffman_dict = compress_file_bwt_mtf_ha('test.txt')
decompress_file_bwt_mtf_ha('test.bin', huffman_dict)
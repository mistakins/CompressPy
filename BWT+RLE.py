import numpy as np

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

def compress_file_bwt_rle(file_path):
    with open(file_path, 'r') as file:
        string = file.read()
    transformed = burrows_wheeler_transform(string)
    encoded = rle_encoding(transformed)
    with open(file_path.replace('.txt', '.bwt_rle'), 'w') as file:
        file.write(encoded)

def decompress_file_bwt_rle(file_path):
    with open(file_path, 'r') as file:
        encoded = file.read()
    transformed = rle_decoding(encoded)
    decompressed = inverse_burrows_wheeler_transform(transformed)
    with open(file_path.replace('.bwt_rle', '.decompressed'), 'w') as file:
        file.write(decompressed)

compress_file_bwt_rle('test.txt')
decompress_file_bwt_rle('test.bwt_rle')
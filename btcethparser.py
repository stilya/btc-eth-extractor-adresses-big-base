import re
import os

bitcoin_pattern = r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b'
ethereum_pattern = r'\b0x[a-fA-F0-9]{40}\b'
input_file = 'bitcointrash.txt'
bitcoin_file = 'bitcoin.txt'
ethereum_file = 'ethereum.txt'
num_threads = 14

# функция для чтения файла в несколько потоков
def read_file_chunks(filename, chunk_size=1024*1024, num_threads=1):
    with open(filename, 'r') as f:
        while True:
            data = f.read(chunk_size*num_threads)
            if not data:
                break
            for i in range(num_threads):
                chunk = data[i*chunk_size:(i+1)*chunk_size]
                if not chunk:
                    break
                yield chunk

# функция для извлечения адресов из текста
def extract_addresses(text, pattern):
    return re.findall(pattern, text)

# создаем списки для адресов биткоин и эфириум
bitcoin_addresses = []
ethereum_addresses = []

# читаем файл в несколько потоков и извлекаем адреса
for chunk in read_file_chunks(input_file, num_threads=num_threads):
    bitcoin_addresses.extend(extract_addresses(chunk, bitcoin_pattern))
    ethereum_addresses.extend(extract_addresses(chunk, ethereum_pattern))

# сохраняем адреса в текстовые файлы
with open(bitcoin_file, 'w') as f:
    f.write('\n'.join(bitcoin_addresses))
with open(ethereum_file, 'w') as f:
    f.write('\n'.join(ethereum_addresses))

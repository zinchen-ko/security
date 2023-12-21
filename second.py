def tea_encrypt(block, key):
    delta = 0x9e3779b9
    v0, v1 = int.from_bytes(block[:4], byteorder='little'), int.from_bytes(block[4:], byteorder='little')
    k0, k1, k2, k3 = key[0], key[1], key[2], key[3]
    sum_ = 0
    for i in range(32):
        sum_ += delta
        v0 += ((v1 << 4) + k0) ^ (v1 + sum_) ^ ((v1 >> 5) + k1)
        v1 += ((v0 << 4) + k2) ^ (v0 + sum_) ^ ((v0 >> 5) + k3)
    return v0.to_bytes(4, byteorder='little') + v1.to_bytes(4, byteorder='little')

def tea_decrypt(block, key):
    delta = 0x9e3779b9
    v0, v1 = int.from_bytes(block[:4], byteorder='little'), int.from_bytes(block[4:], byteorder='little')
    k0, k1, k2, k3 = key[0], key[1], key[2], key[3]
    sum_ = delta << 5
    for i in range(32):
        v1 -= ((v0 << 4) + k2) ^ (v0 + sum_) ^ ((v0 >> 5) + k3)
        v0 -= ((v1 << 4) + k0) ^ (v1 + sum_) ^ ((v1 >> 5) + k1)
        sum_ -= delta
    return v0.to_bytes(4, byteorder='little') + v1.to_bytes(4, byteorder='little')

def encrypt_file(input_file, output_file, key):
    with open(input_file, 'rb') as f:
        data = f.read()
    padded_data = data.ljust(((len(data) + 7) // 8) * 8, b'\0')  # Дополнение данных до размера кратного 8
    encrypted_data = b''
    for i in range(0, len(padded_data), 8):
        block = padded_data[i:i+8]
        encrypted_block = tea_encrypt(block, key)
        encrypted_data += encrypted_block
    with open(output_file, 'wb') as f:
        f.write(encrypted_data)

def decrypt_file(input_file, output_file, key):
    with open(input_file, 'rb') as f:
        encrypted_data = f.read()
    decrypted_data = b''
    for i in range(0, len(encrypted_data), 8):
        block = encrypted_data[i:i+8]
        decrypted_block = tea_decrypt(block, key)
        decrypted_data += decrypted_block
    with open(output_file, 'wb') as f:
        f.write(decrypted_data)

# Пример использования
key = b'\x00\x01\x02\x03\x04\x05\x06\x07'
encrypt_file('input_file.txt', 'encrypted_file.enc', key)
decrypt_file('encrypted_file.enc', 'decrypted_file.txt', key)
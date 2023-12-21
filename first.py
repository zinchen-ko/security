def read_file():
    text = []
    with open('file.txt', 'r') as f:
        while 1:
            char = f.read(1)
            if not char:
                break
            text.append(char)

        f.close()
    return text


def ord_all(text):
    ord_text = []
    for i in text:
        ord_text.append(ord(i))
    return ord_text


def get_replace(key_ord):
    replace = []
    sorted_key_ord = key_ord.copy()
    sorted_key_ord.sort()
    for i in sorted_key_ord:
        if key_ord.index(i) in replace:
            replace.append(key_ord.index(i) + 1)
            continue
        replace.append(key_ord.index(i))
    return replace


def encrypte(text_ord, replace):
    length = len(replace)
    blink = 0
    replace_i = 0
    if len(text_ord) % length > 0:
        result = [32] * (len(text_ord) + 1)
    else:
        result = [32] * len(text_ord)
    for i in text_ord:
        result[blink * length + replace[replace_i]] = i
        if replace_i == length - 1:
            blink = blink + 1
            replace_i = 0
        else:
            replace_i = replace_i + 1
    return result


def decrypte(enc_result, replace):
    result = [32] * len(enc_result)
    length = len(replace)
    blink = 0
    for k, i in enumerate(enc_result):
        result[blink * length + replace.index(k - blink * length)] = i
        if (k+1) % length == 0:
            blink = blink + 1
    return result


def list_to_text(list):
    result = ''
    for i in list:
        result = result + chr(i)
    return result


def main():
    text = read_file()
    key = input("Введите ключевое слово: ")

    text_ord = ord_all(text)
    key_ord = ord_all(key)

    replace = get_replace(key_ord)

    enc_result = encrypte(text_ord, replace)
    dec_result = decrypte(enc_result, replace)

    print(fr'Изначальный текст: {list_to_text(text_ord)}')
    print(fr'Шифрованный текст: {list_to_text(enc_result)}')
    print(fr'Дешифрованный текст: {list_to_text(dec_result)}')


if "__main__" == __name__:
    main()

import rsaAlg

def text_to_blocks_num(text,len_keys):
    len_block = (len_keys // 4) -1
    blocks = [text[i:i + len_block] for i in range(0, len(text), len_block)]
    for i in range(len(blocks)):
        blocks[i] = text_in_numb(blocks[i])
    return blocks

def block_num_to_text(block,len_keys):
    block = block.rjust((((len_keys//4)-1)*4),'0')
    result = ''.join(block)
    result_text = ''
    for i in range(len(result) // 4):
        var = int(result[i * 4:(i + 1) * 4])
        if var != 0:
            result_text += chr(var)
    return result_text

def text_in_numb(text):
    result = ''
    for ch in text:
        var = str(ord(ch)).rjust(4, '0')
        result += var
    return result

def generation_c_and_d(p):
    while True:
        c = ib2_4.generation_of_a_prime_number_for_diff()
        if egcd(c, p-1)[0] == 1 and c < p:
            break
    d = invert(c, p - 1)
    return c,d
    
def egcd(a, b):
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
        gcd = b
    return gcd, x

def invert(x, p):
    inv = egcd(x, p)[1]
    if inv < 0:
        return inv+p
    else:
        return inv
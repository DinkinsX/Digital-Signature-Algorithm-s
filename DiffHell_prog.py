class DH_Endpoint():
    def __init__(self, public_key1, public_key2, private_key):
        self.public_key1 = public_key1
        self.public_key2 = public_key2
        self.private_key = private_key
        self.full_key = None

    def modular_pow(self):
        x = self.private_key
        a = self.public_key1
        p = self.public_key2
        return modular_pow(a,x,p)

def modular_pow(a, x, p):
    x = list(reversed(bin(x)))[:-2]
    s = a
    y = 1
    for i in range(len(x)):
        if int(x[i]) == 1:
            y = (y * s) % p
        s = (s * s) % p
    return y
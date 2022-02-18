class Caesar:
    def encrypt(p, k):
        return "".join(map(lambda c: chr((ord(c) - ord('A') + k) % 26 + ord('A')), p))
    def decrypt(c, k):
        return Caesar.encrypt(c, 26-k)

class Multiplicative:
    def encrypt(p, k):
        # k has to have multiplicative inverse
        assert gcd(k, 26) == 1
        return "".join(map(lambda c: chr(((ord(c) - ord('A')) * k) % 26 + ord('A')), p))
    def decrypt(c, k):
        # k has to have multiplicative inverse
        assert gcd(k, 26) == 1
        return Multiplicative.encrypt(c, pow(k, -1, 26))

class Affine:
    def encrypt(p, k):
        s, t = k
        # s has to have multiplicative inverse
        assert gcd(s, 26) == 1
        return "".join(map(lambda c: chr((t + (ord(c) - ord('A')) * s) % 26 + ord('A')), p))
    def decrypt(c, k):
        s, t = k
        # s has to have multiplicative inverse
        assert gcd(s, 26) == 1
        return Affine.encrypt(c, (pow(s, -1, 26), 26-t))

print(Caesar.encrypt("KARLSRUHE", 13))
print(Caesar.decrypt("UPWGGPS", ord("G")-ord("R")))

def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a%b)

print(Multiplicative.encrypt("KARLSRUHE", 7))
print(Multiplicative.decrypt(Multiplicative.encrypt("KARLSRUHE", 7), 7))
#print(dec_mult("FYRRSF", 
for i in range(26):
    if gcd(i, 26) == 1 and Multiplicative.encrypt("Y", i) == "O":
        print(Multiplicative.encrypt("FYRRSF", i))
        break

print(Affine.decrypt("ZPCZPALLCP", (5, 8)))
print(Affine.encrypt("KARLSRUHE", (11, 17)))

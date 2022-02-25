lfsr = [1, 1, 0, 1]

def get(lfsr, n):
    return (lfsr[n-1] + lfsr[n-4]) % 2

def get(lfsr, n):
    return sum(lfsr[n-4:n]) % 2

for i in range(20):
    lfsr.append(get(lfsr, i+4))

print(lfsr)
print(f"Periode=1110100")
print(f"Periode=0100111")


def encrypt(initial, plain):
    out = []
    for i, c in enumerate(plain):
        initial.append(get(initial, i + 4))
        out.append(initial[-5] ^ c)
    return out

cipher = encrypt([1,1,1,1], [1,1,0,0,1,0,1,0])
print(cipher)
print(encrypt([1,1,1,1], cipher))

# 0010 0110
# 0 0100 110
# 00 1001 10
# 001 0011 0

# c_2 = 0
# c_1 = 1
# c_0 + c_3 = 1 -> c_0 = 1
# c_2 + c_3 = 0 -> c_3 = 0

# c = [1, 1, 0, 0]

# 14 40

# c_0 + 4*c_1 = 4
# c_0 = 4*(1 - c_1)
# 4*c_0 + 4*c_1 = 0
# 16 - 16c_1 + 4*c_1 = 0
# 16 - 12c_1 = 0
# 12c_1 = 16
# 2c_1 = 1
# c_1 = 3
# c_0 + 12 = 4 -> c_0 + 2 = 4 -> c_0 = 2

# c = [2, 3]


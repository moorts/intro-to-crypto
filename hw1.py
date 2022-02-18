from time import sleep
from collections import defaultdict
import enchant

from ciphers import *

# German dictionary
d = enchant.Dict("de_DE")

##### 1. #####

# a) Und Cäsar sprach : SBKF SFAF SFZF. Bestimmen Sie den Verschiebeparameter t sowie den sich ergebenden Klartext.

cipher = "SBKF SFAF SFZF"

for t in range(26):
    p = Caesar.decrypt(cipher, t)
    if "VENI" in p:
        print(f"1a) t={t}, plaintext={p}")
        break

# b) Die folgende Nachricht wurde mit einer Verschiebe-Chiffre verschl¨usselt :
# MRNBNA CNGC RBC WRLQC VNQA PNQNRV. Wie lauten Verschiebeparameter t und Klartext?

def caesar_brute_force(c):
    m = 0
    best = 0
    for t in range(26):
        p = Caesar.decrypt(c, t)
        word_count = 0
        for w in p.split(" "):
            if d.check(w.lower()) or d.check(w.lower().capitalize()):
                word_count += 1
        if word_count > m:
            m = word_count
            best = t
    return best, Caesar.decrypt(c, best)


cipher = "MRNBNA CNGC RBC WRLQC VNQA PNQNRV"

t, p = caesar_brute_force(cipher)
print(f"1b) t={t}, plaintext={p}")

##### 2. #####

# a) Lpulu nhuglu kbtwmlu, kburslu buk zapsslu Olyizaahn shun dhy pjo bualy ilkybljrluk uplkypnly Dvsrlukljrl kbyjo lpul lpnluabltspjo vlkl Shukzjohma nlypaalu, ipz pjo. hsz kpl Zjohaalu klz Hilukz olyhizhurlu, khz zjodlytblapnl Ohbz Bzoly cvy tpy splnlu zho.

cipher = "Lpulu nhuglu kbtwmlu, kburslu buk zapsslu Olyizaahn shun dhy pjo bualy ilkybljrluk uplkypnly Dvsrlukljrl kbyjo lpul lpnluabltspjo vlkl Shukzjohma nlypaalu, ipz pjo. hsz kpl Zjohaalu klz Hilukz olyhizhurlu, khz zjodlytblapnl Ohbz Bzoly cvy tpy splnlu zho."

t, p = caesar_brute_force(cipher)
print(f"2a) t={t}, plaintext={p}")

##### 3. #####

# a) Erstellen Sie eine Tabelle, in der jedem s ∈ {1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25} sein
#    entsprechender s'−Wert zugeordnet wird, fuer den gilt s · s 0 = 1 mod 26.

inverses = {s: pow(s, -1, 26) for s in [1,3,5,7,9,11,15,17,19,21,23,25]}
print(f"3a) {inverses}")

##### 4. #####

# a) Zeigen Sie, dass bei einer multiplikativen Chiffre auf der Basis des normalen Alphabets mit 26 Buchstaben a auf a und n auf n abgebildet werden.

# 1. Zeigen sie das a auf a abgebildet wird:
#    -> a codiert zum Zahlenwert 0
#    -> Multiplikation lässt diesen unverändert
# 2. Zeigen sie das n auf n abgebildet wird:
#    -> n codiert zum Zahlenwert 13
#    -> Nur ungerade Faktoren sind zulässig (da gerade nie coprime sind)
#    -> 13 * (2n-1) = 26*n - 13
#    -> 26*n == 0 % 26 -> 26*n -13 (mod 26) = -13 (mod 26) = 13 q.e.d


# b) Wieviele multiplikative Chiffren sind auf einem Alphabet mit 10 bzw. 30 bzw. 75
#    Buchstaben theoretisch moeglich ? Wieviele gibt es jeweils tatsaechlich ?

# Es gibt theoretisch bei n Buchstaben im Alphabet n-1 mögliche Schlüssel und damit Chiffren, aber nur die Schlüssel, die coprime zu n sind, haben ein modulares multiplikatives Invers.
# Euler's Totient Funktion berechnet die Anzahl an Zahlen in einer multiplikativen Gruppe modolu n, die coprim zu n sind.

def totient(n):
    phi = 0
    for i in range(n):
        if gcd(n, i) == 1:
            phi += 1
    return phi

candidates = [10, 30, 75]
print(f"4b) {list(zip(candidates, map(totient, candidates)))}")

# c) Multiplicative Cipher: LO BIMIN ONT LO RXJIMIN KIQ PIVIQZ TAK SAEBKIN OIPIVJAKK TIV LIQZ

from collections import Counter

cipher = "LO BIMIN ONT LO RXJIMIN KIQ PIVIQZ TAK SAEBKIN OIPIVJAKK TIV LIQZ"

freqs = Counter(cipher)

mfl = max(freqs, key=lambda x: freqs[x])

emaps = [(Multiplicative.encrypt("E", k), k) for k in inverses.values()]

KEY = next(filter(lambda x: x[0] == mfl, emaps))[1]

print(f"4c) s={KEY}, plaintext={Multiplicative.decrypt(cipher, KEY)}")

##### 5. #####

# a) Durch 2 Klartext-Geheimtext-Zuordnungen ist eine Tausch-Chiffre eindeutig festgelegt. Bestimmen Sie das Parameterpaar (s, t), wenn vorgegeben ist
# 1. Klartextbuchstabe b −→ Geheimtextbuchstabe g und
#    Klartextbuchstabe t −→ Geheimtextbuchstabe o
#
# 2. Klartextbuchstabe b −→ Geheimtextbuchstabe g und
#    Klartextbuchstabe t −→ Geheimtextbuchstabe w
#
# 3. Klartextbuchstabe b −→ Geheimtextbuchstabe c und
#    Klartextbuchstabe t −→ Geheimtextbuchstabe z


# Alle Zuordnungen wären 26*25=650 Kombinationen, es sind jedoch nur 12*26=312 Kombinationen möglich
# (da gcd(s, 26) == 1 gelten muss)

coprimes = [1,3,5,7,9,11,15,17,19,21,23,25]

def gen_enc_matrix(c):
    return [[Affine.encrypt(c, (s, t)) for s in coprimes] for t in range(26)]

def calc_affine_params(map1: tuple[int, int], map2: tuple[int, int]):
    p1, c1 = map1
    p2, c2 = map2

    m = gen_enc_matrix(p1)
    for s in coprimes:
        for t in range(26):
            if Affine.encrypt(p1, (s, t)) == c1:
                if Affine.encrypt(p2, (s, t)) == c2:
                    return s, t

assert calc_affine_params(('B', 'G'), ('T', 'O')) == (25, 7)
print(f"5a) b->g, t->o: {calc_affine_params(('B', 'G'), ('T', 'O'))}")
assert calc_affine_params(('B', 'G'), ('T', 'W')) == (11, 21)
print(f"5a) b->g, t->w: {calc_affine_params(('B', 'G'), ('T', 'W'))}")
assert calc_affine_params(('B', 'C'), ('T', 'Z')) == None
print(f"5a) b->c, t->z: {calc_affine_params(('B', 'C'), ('T', 'Z'))}")

# b) Dechiffrieren Sie SRSF VCHWFI. Benutzen Sie die Tatsache, dass mit der TauschChiffre (7,t) verschl¨usselt wurde. Bestimmen Sie t.
# (Tipp : t ∈ {0, 1, 2, ..., 25} ist durch 6 teilbar)

cipher = "SRSF VCHWFI"

for t in range(26):
    plain = Affine.decrypt(cipher, (7, t))
    if d.check(plain.split(" ")[0]):
        print(f"5b) s=7, t={t}, plaintext={plain}")

# c) Decrypt BQZNXD

cipher = "BQZNXD"

for s in coprimes:
    plain = Affine.decrypt(cipher, (s, 3))
    if d.check(plain):
        print(f"5c) s={s}, t=3, plaintext={plain}")


##### 6. #####

def freqs(s):
    return Counter(s)

assert freqs("AAAABBBCCD") == {'A': 4, 'B': 3, 'C': 2, 'D': 1}

def bigrams(s):
    s = s.replace(" ", "")
    out = defaultdict(int)
    for i in range(len(s)-1):
        out[s[i:i+2]] += 1
    return out

assert bigrams("ththe") == {'th': 2, 'ht': 1, 'he': 1}


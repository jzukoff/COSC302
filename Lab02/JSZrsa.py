import random
import math
# Josh Zukoff

def is_prime(n, iterations=1):
    for i in range(iterations):
        randomint = random.randint(0,n-1)
        if pow(randomint, n-1, n) != 1:
            return False


    return True
def generate_prime(bits):
    if bits<2:
        return None
    while True:
        randomint = random.randint(2**(bits-1), 2**(bits)-1)
        if is_prime(randomint):
            break
    return randomint

def gcd(a,b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

def extendedGcd(a,b):
    if b == 0:
        return (1, 0, a)
    result = extendedGcd(b, a % b)
    x = result[0]
    y = result[1]
    d = result[2]
    return (y, x-(a//b)*y,d)

def rsa_public_key(p,q):
    e = 5
    N = p*q
    M = (p-1)*(q-1)
    while gcd(e, M) != 1:
        e += 1
    return (N, e)

def rsa_private_key(p, q, e):
    result = extendedGcd((p-1)*(q-1), e)
    d = result[1] % ((p-1)*(q-1))
    return d

def rsa_encrypt(infile, outfile, N, e):
    file = open(infile, 'rb')
    out = open(outfile, 'wb')
    k = int(math.ceil((math.log(N,2)/8)-1))
    finalMessage = []
    while True:
        unpacked = []
        plainInt = 0
        text = list(file.read(k))
        if text == []:
            break
        multiply = 0
        for i in range(len(text)-1, -1, -1):
            element = text[i]*(256**multiply)
            plainInt += element
            multiply += 1
        encryptedInt = (pow(plainInt, e, N))
        while (encryptedInt > 0):
            nextByte = encryptedInt % 256
            unpacked = [nextByte] + unpacked
            encryptedInt = (encryptedInt - nextByte)//256
        while (len(unpacked) < (k+1)):
               unpacked = [0] + unpacked
        finalMessage += unpacked
    out.write(bytes(finalMessage))
            


def rsa_decrypt(infile, outfile, N, d):
    file = open(infile, 'rb')
    out = open(outfile, 'wb')
    k = int(math.ceil((math.log(N,2)/8)-1))
    finalMessage = []
    while True:
        plainInt = 0
        unpacked = []
        text = list(file.read(k+1))
        if text == []:
            break
        multiply = 0
        for i in range(len(text)-1, -1, -1):
            element = text[i]*(256**multiply)
            plainInt += element
            multiply += 1
        decryptedInt = (pow(plainInt, d, N))
        while (decryptedInt > 0):
            nextByte = decryptedInt % 256
            unpacked = [nextByte] + unpacked
            decryptedInt = (decryptedInt - nextByte)//256
        finalMessage += unpacked
    out.write(bytes(finalMessage))

    

def main():
    bits = int(input("How many bits would you like p and q to be? "))
    p = generate_prime(bits)
    q = generate_prime(bits)
    key = rsa_public_key(p,q)
    N = key[0]
    e = key[1]
    d = rsa_private_key(p,q,e)
    infile = input("What is the name of the file to be encrypted? ")
    outfile2 = input("What is the name of the file you would like to decrypt to? ")
    rsa_encrypt(infile,'encrypted.txt',N,e)
    print ("File encrypted")
    rsa_decrypt('encrypted.txt', outfile2, N, d)
    print ("File decrypted")

if __name__ == '__main__':
    main()    

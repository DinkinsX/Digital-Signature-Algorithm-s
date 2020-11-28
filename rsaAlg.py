import random
import math
from time import *
import sys

def toFixed(numObj, digits=4):
    return f"{numObj:.{digits}f}"

def SECONDTESTFORP(p):
	p=int(p)	
	if TEST2(p) == True:
		return p

def SECONDTESTFORQ(p,q):
	p=int(p)
	q=int(q)
	if TEST2(q) == True:
		q=int(q)
		return q


def generation_of_a_prime_number():
	while True:
		p = random.randint (1000000000, 1000000000000000000000000000000000)
		if TEST(p, 50) == True:
			return p

def generation_of_a_prime_number_for_diff():
	while True:
		p = random.randint (10000000000000000000000000000000000000000000000000, 90000000000000000000000000000000000000000000000000)
		if TEST(p, 50) == True:
			return p

def generate_second_number(p):
	len_p = len(str(p))
	len_q = 50 - len_p
	while True:
		q = random.randint (10**len_q, 3*10**(len_q))
		if TEST(q, 50) == True and len(str(p*q)) == 50:
			return q


def calculating_a_mutually_prime_number(b):
	b2 = b
	for i in range(2, b):
		a = i
		b = b2
		while a != 0 and b != 0:
		    if a > b:
		        a = a % b
		    else:
		        b = b % a
		if a == 1 or b == 1:
			return i

def bezout(a, b):
    x, xx, y, yy = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a % b
        x, xx = xx, x - xx*q
        y, yy = yy, y - yy*q
    return (x, y, a)

def evklid(s,d):
	x,y,z = bezout(s,d)
	#print(x,y,a)
	xx = x
	if x < 0:
		while x < 0:
			x = xx+(2*d)
	#print(x,y,a)
	return x

def findReverseToE(a, b):
    phi_n = b
    x, x1, y, y1 = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a % b
        x, x1 = x1, x - x1*q
        y, y1 = y1, y - y1*q
    if x < 0:
        x += phi_n
    return x

def TEST(n, k): # miller-rabin
    from random import randint
    if n < 2: return False
    for p in [2,3,5,7,11,13,17,19,23,29]:
        if n % p == 0: return n == p
    s, d = 0, n-1
    while d % 2 == 0:
        s, d = s+1, d//2
    for i in range(k):
        x = pow(randint(2, n-1), d, n)
        if x == 1 or x == n-1: continue
        for r in range(1, s):
            x = (x * x) % n
            if x == 1: return False
            if x == n-1: break
        else: return False
    return True

def primeFactors(n):
    factors = []
    if n%2 == 0:
            factors.append(2)
            while n%2 == 0:
                    n = n/2

    f = math.sqrt(n)
    i = 3
    while (i <= f) :
            if n%i == 0:
                    factors.append(i) 
                    while n%i == 0:
                            n = n/i
            i = i + 1
    if n>2:
            factors.append(n)
    return factors

def TEST2(N):
    if N%2 == 0:
            return False
    
    factors = primeFactors(N-1)

    for i in range(100):
            a = random.randint(2, N-1)
            if pow(a, N-1, N) != 1:
                    return False
            else:
                    check = True
                    for j in factors:
                            if pow(a, int((N-1)/j), N) == 1:
                                    check = False
                                    break
                    if check == True :
                            return True

    return False

def formkod(text2):
	kod = []
	for i in range(len(text2)):
		text2[i] = ord(text2[i])
		tmp = [x for x in str(text2[i])]
		if len(tmp) == 3:
			tmp.insert(0,'0')
		if len(tmp) == 2:
			tmp.insert(0,'0')
			tmp.insert(0,'0')
		kod.extend(tmp)
	#print('Текст: ', text2, '\n')
	#print('Код текста:',kod, '\n')
	return kod

def kod2(kod,N):
	tmp = ''
	tmp2 = ''
	kod2 = []
	for i in range(len(kod)):
		tmp += kod[i]
		tmp2 = tmp
		if i == len(kod)-1:
			kod2 += [tmp]
			break
		tmp2 += kod[i+1]
		if int(tmp2) >= N or int(tmp) == 0:
			kod2 += [tmp]
			tmp = ''
			tmp2 = ''
	return kod2

def decode(kod2, e, N):
	for i in range(len(kod2)):
		kod2[i] = pow(int(kod2[i]), e, N)
	print('Расшифрованное сообщение:', kod2, '\n')
	#print(len(kod2))
	kod = []
	for i in range(len(kod2)):
		kod += str(kod2[i])
	#print(kod)
	pr = []
	for i in range(0,len(kod),4):
		tmp = ''
		for j in range(i,i+4):
			tmp += str(kod[j])
		pr += [tmp]
	#print(pr)
	return pr

	
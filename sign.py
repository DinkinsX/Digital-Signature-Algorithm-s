from miller import *
import sys
import hashlib
import math


def computeInverse (in1,in2):
    aL = [in1]
    bL = [in2]
    tL = [0]
    t = 1
    sL = [1]
    s = 0
    q = math.floor((aL[0]/bL[0]))
    r = (aL[0] - (q*bL[0]))

    while r > 0 :
        temp = (tL[0] - (q*bL[0]))
        tL[0] = t
        t = temp
        temp = (sL[0] - (q*s))
        sL[0] = s
        s = temp
        aL[0] = bL[0]
        bL[0] = r
        q = math.floor(aL[0]/bL[0])
        r = (aL[0] - (q*bL[0]))

    r = bL[0]

    inverse = s % in2
    return inverse


def squareAndMultiply(x,c,n):
	z=1
	c="{0:b}".format(c)[::-1]
	
	l=len(c)
	for i in range(l-1,-1,-1):
		z=pow(z,2)
		z=z%n
		if(c[i] == '1'):
			z=(z*x)%n
	return z	

def shaHash(fileName):
	BLOCKSIZE = 65536
	hasher = hashlib.sha1()
	with open(fileName, 'rb') as afile:
		buf = afile.read(BLOCKSIZE)
		while len(buf) > 0:
			hasher.update(buf)
			buf = afile.read(BLOCKSIZE)
	hasher = hasher.hexdigest()
	
	return hasher
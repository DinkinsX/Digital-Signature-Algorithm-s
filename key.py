from miller import *
from math import gcd

def loopIsPrime(number):
	isNumberPrime = True
	for i in range(0,20):
		isNumberPrime*=isPrime(number)
		if(isNumberPrime == False):
			return isNumberPrime
	return isNumberPrime	


def modexp( base, exp, modulus ):
        return pow(base, exp, modulus)

		
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
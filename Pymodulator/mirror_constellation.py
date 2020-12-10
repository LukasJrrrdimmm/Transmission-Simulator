import numpy as np


def noiseAdjust(s, l):
	lim = np.floor(l/2)
	a = []
	for n in s:
		if n <= lim:
			a.append(n - lim)
		else:
			a.append(1 + n - lim)
	return np.array(a)
			
		

def setConstellation(msg, M):
	l = np.log2(M)
	v = []
	for i in range(0, msg, l):
		aux = msg[i:i+l]
		aux_2 = ""
		for n in aux:
			aux_2 += str(n)
		d = int(aux_2, 2)
		if i > l/2:
			v.append((d - (l/2 + 1)))
		else:
			v.append(d - l/2)
	return v

def setDirectConstellation(msg, l):
	v = []
	for i in range(0, msg, l):
		aux = msg[i:i+l]
		aux_2 = ""
		for n in aux:
			aux_2 += str(n)
		d = int(aux_2, 2)
		if i > l/2:
			v.append((d - (l/2 + 1)))
		else:
			v.append(d - l/2)
	return v

def removeDirectConstellation(s, l):
	rec = []
	for n in s:
		if n > 0:
			rec.append(n + (l/2 + 1))
		else:
			rec.append(n + l/2)
	return bin(np.array(rec))

def removeConstellation(s, M):
	l = np.log2(M)
	rec = []
	for n in s:
		if n > 0:
			rec.append(n + (l/2 + 1))
		else:
			rec.append(n + l/2)
	return bin(np.array(rec))

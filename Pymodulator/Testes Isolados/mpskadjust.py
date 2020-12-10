import numpy as np
import carrier as crr

def sinAdjust(y, T):
	f, t = crr.Generic_Carrier(T)
	s = []
	for n in y:
		s += list(np.sin(np.pi/n)*np.sin(np.pi*f*t))
	#print(s)
	return np.array(s)

def cosAdjust(x, T):
	f, t = crr.Generic_Carrier(T)
	g = []
	for s in x:
		if s > 0:
			g += list(np.cos((np.pi/(4*abs(s))))*np.cos(np.pi*f*t))
		elif s == 0:
			g += list(np.cos(s)*np.cos(np.pi*f*t))
		else:
			g += list(np.cos((np.pi/(4*abs(s))))*np.cos(np.pi*f*t))
	#print(g)
	return np.array(g)

def sinFilter(y, c_flag):
	res = []
	for s in y:
		if abs(s) < (10**(-8)):
			if s > 0.0:
				res.append(1)
			else:
				res.append(-1)
		else:
			res.append((s)/np.pi)**(-1)
	if c_flag is True:
		return np.array(res)*1j
	else:
		return np.array(res)

def cosFilter(x, flag):
	f = []
	for s in x:
		if s < 0:
			f.append((((s-np.pi)/np.pi)**-1)/4)
		elif s == 0:
			f.append(s)
		else:
			f.append(((s/np.pi)**-1)/4)
	if flag == True:
		return np.array(f)*1j
	else:
		return np.array(f)

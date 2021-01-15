import numpy as np
import carrier as crr

def sinAdjust(y, T, M):
	f, t = crr.Generic_Carrier(T, period=False)
	s = []
	for n in y:
		s += list(np.sin(2*np.pi*f*t + (2*n - 1)*(np.pi/M)))
	#print(s)
	return np.array(s)

def cosAdjust(x, T, M):
	f, t = crr.Generic_Carrier(T, period=False)
	g = []
	for s in x:
		if(s > 0):
			g += list(np.cos(2*np.pi*f*t + s*(np.pi/M)))
		if(s < 0):
			g += list(-np.cos(2*np.pi*f*t + s*(np.pi/M)))
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

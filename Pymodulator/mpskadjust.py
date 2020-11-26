import numpy as np

def sinAdjust(y):
	return np.sin(np.pi/y)

def cosAdjust(x):
	f = []
	for s in x:
		if s > 0:
			f.append(np.cos(np.pi/(4*abs(s))))
		elif s == 0:
			f.append(np.cos(s))
		else:
			f.append(np.cos((np.pi/(4*abs(s)) + np.pi)))
	return np.array(f)

def sinFilter(y, c_flag):
	res = []
	for s in y:
		if abs(s) < (10**(-8)):
			if s > 0.0:
				res.append(1)
			else:
				res.append(-1)
		else:
			res.append((np.arcsin(s)/np.pi)**(-1))
	if c_flag is True:
		res = np.array(res)*1j
	else:
		res = np.array(res)
	return res

def cosFilter(x, flag):
	f = []
	for s in x:
		if s < 0:
			f.append((((np.arccos(s)-np.pi)/np.pi)**-1)/4)
		elif s == 0:
			f.append(np.arccos(s))
		else:
			f.append(((np.arccos(s)/np.pi)**-1)/4)
	if flag == True:
		return np.array(f)*1j
	else:
		return np.array(f)

import numpy as np

def sinAdjust(y):
	f = []
	for s in y:
		f.append(np.sin(np.pi/s))
	return np.array(f)

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
		if s < 10**-5:
			if s > 0:
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

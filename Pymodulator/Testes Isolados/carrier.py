import numpy as np
def Generic_Carrier(T):
	bp=0.01
	sp=bp*2    #symbol period for M-array QAM
	sr=1/sp    #symbol rate
	f=sr*2     #carry frequency 
	t=np.arange(0, sp, sp/T)
	return t, f

def CarrierDemodeQAM(signal, T):
	f, t = Generic_Carrier(T)
	xgm = []
	c1 = np.cos(2*np.pi*f*t)
	c2 = np.sin(2*np.pi*f*t)
	for i in range(0, len(signal), len(c1)):
		g = (signal[i:i+len(c1)].real)/c1
		g1 = []
		for n in g:
			if str(n) != 'nan':
				g1.append(n)
		h = (signal[i:i+len(c1)].imag)/c2
		h1 = []
		for n in h:
			if str(n) != 'nan':
				h1.append(n)
		print("============{}A |{}| ".format((i/len(c1)), np.mean(g1) + 1j*np.mean(h1)))
		xgm.append(np.mean(g1) + 1j*np.mean(h1))
	return xgm

def CarrierDemodePSK(signal, T):
	f, t = Generic_Carrier(T)
	xgm = []
	c1 = np.cos(np.pi*f*t)
	c2 = np.sin(np.pi*f*t)
	for i in range(0, len(signal), len(c1)):
		g = (np.arccos(signal[i:i+len(c1)].real/c1))**(-1)
		g1 = []
		for n in g:
			if str(n) != 'nan':
				g1.append(n)
		h = (np.arcsin(signal[i:i+len(c2)].imag/c2))**(-1)
		h1 = []
		for n in h:
			if str(n) != 'nan':
				h1.append(n)
		print("============{}A |{}| ".format((i/len(c1)), np.mean(g1) + 1j*np.mean(h1)))
		xgm.append(np.mean(g1) + 1j*np.mean(h1))
	return np.array(xgm)

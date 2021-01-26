import numpy as np
import scipy as sp
def Generic_Carrier(T, period):
	bp=0.01
	sp=bp*2    #symbol period for M-array QAM
	sr=1/sp    #symbol rate
	f=sr*2     #carry frequency 
	t=np.arange(0, sp, sp/T)
	if period == False:
		return t, f
	else:
		return t, f, sp

def CarrierDemodeQAM(signal, T):
	t, f, sp = Generic_Carrier(T, period = True)
	xgm = []
	c1 = np.cos(2*np.pi*f*t)
	c2 = np.sin(2*np.pi*f*t)
	g1 = []
	h1 = []
	for i in range(0, len(signal), len(c1)):
		g = np.trapz((signal[[j for j in range(i , (i + len(c1)))]]*c1), t)
		g1 = round(2*g/sp)
		h = np.trapz((signal[[j for j in range(i , (i + len(c1)))]]*c2), t)
		h1 = round(2*h/sp)
		print(g1)
		print(h1)
		print("============{}B |{}| ".format((i/len(c1)), (np.array(g1) + 1j*np.array(h1))))
		xgm += [np.array(g1) + 1j*np.array(h1)]
	return np.array(xgm)

def CarrierDemodePSK(signal, T, M):
	f, t = Generic_Carrier(T, period = False)
	xgm = []
	c1 = np.cos(2*np.pi*f*t)
	for i in range(0, len(signal), len(c1)):
		gs = signal[i:i+len(c1)].real
		if(gs[0] >= 0):
			g = (np.arccos(gs) - 2*np.pi*f*t)*(M/np.pi)
		else:
			g = (np.arccos(gs) - 2*np.pi*f*t)*(M/np.pi) - M
		g1 = []
		for n in g:
			if str(n) != 'nan':
				g1.append(n)
		h = (((np.arcsin(signal[i:i+len(c1)].imag) - 2*np.pi*f*t)*M/np.pi) + 1)/2
		h1 = []
		for n in h:
			if str(n) != 'nan':
				h1.append(n)
		print(np.array(g1))
		print(np.array(h1))
		print("============{}A |{}| ".format((i/len(c1)), g1[0]+ h1[0]*1j))
		xgm.append(g1[0] + 1j*h1[0])
		
	return np.array(xgm)

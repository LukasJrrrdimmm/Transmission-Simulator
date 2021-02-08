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

def CarrierDemodeQAMEntrelac(signal, T):
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

def CarrierDemodeQAM(signal, T, modcpy):
	
	t, f, sp = Generic_Carrier(T, period = True)
	sig1 = []
	sig2 = []
	c1 = np.cos(2*np.pi*f*t)
	c2 = np.sin(2*np.pi*f*t)
	g1 = []
	h1 = []
	for i in range(0, len(signal), len(c1)):
		g = np.trapz((signal[[j for j in range(i , (i + len(c1)))]]*c1), t)
		g1 = round(2*g/sp)
		h = np.trapz((signal[[j for j in range(i , (i + len(c1)))]]*c2), t)
		h1 = round(2*h/sp)
		print("============{}B |{}| ".format((i/len(c1)), (np.array(g1) + 1j*np.array(h1))))
		sig1.append(g1)
		sig2.append(h1)
	print(sig1)
	print(sig2)
	# esse vetor é complexo
	localiza = np.array(sig1) + 1j*np.array(sig2)

	#usar o mapeamento  com compy (essa função não existe, use o compy para fazer esse mapeamento)
	msg = modcpy.demodulate(localiza, demod_type="hard")
	print(localiza)
	return msg
	#

def CarrierDemodeMPSK(signal, T, modcpy):
	t, f, sp = Generic_Carrier(T, period = True)
	sig1 = []
	sig2 = []
	c1 = np.cos(2*np.pi*f*t)
	c2 = np.sin(2*np.pi*f*t)
	g1 = []
	h1 = []
	for i in range(0, len(signal), len(c1)):
		g = np.trapz((signal[[j for j in range(i , (i + len(c1)))]]*c1), t)
		g1 = 2*g/sp
		h = np.trapz((signal[[j for j in range(i , (i + len(c1)))]]*c2), t)
		h1 = 2*h/sp
		print("============{}B |{}| ".format((i/len(c1)), (np.array(g1) + 1j*np.array(h1))))
		sig1.append(g1)
		sig2.append(h1)
	print(sig1)
	print(sig2)
	# esse vetor é complexo
	localiza = np.array(sig1) + 1j*np.array(sig2)

	#usar o mapeamento  com compy (essa função não existe, use o compy para fazer esse mapeamento)
	msg = modcpy.demodulate(localiza, demod_type="hard")
	print("variável localiza:")
	print(localiza)
	return msg



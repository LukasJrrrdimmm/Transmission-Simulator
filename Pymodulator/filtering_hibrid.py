import math as mth
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import commpy.modulation as commod
import mpskadjust as pskf

def binary_generator(s, N):
		return np.random.randint(2, size = s**N)

def max2pow(lim):
	i = 0
	a = 2**i
	while 1:
		if a >= lim:
			break
		else:
			i += 1
			a = 2**i
	return a

def eqalising2pow(l, M):
	i = M
	a = 2**M
	while 1:
		if a % i == 0:
			break
		else:
			i -= 1
			a = 2**i
	return a

def itob_array(v, N):
	bin_vec = []
	for num in v:
		print(num)
		aux = bin(int(num)).split('b')[1]
		g = ''
		if len(aux) < N:
			c = 0
			for i in range(0, mth.ceil(N)):
				g += '0'
				c += 1
				if c + len(aux) == N:
					bin_vec.append(g+aux)
					break
		else:
			bin_vec.append(aux)
	print(bin_vec)
	return bin_vec

def Generic_Carrier(bp):
	sp=bp*2    #symbol period for M-array QAM
	sr=1/sp    #symbol rate
	f=sr*2     #carry frequency 
	t=np.arange(sp/100, sp, sp/100)
	ss=len(t)
	return t, ss, f

def QuadratureDecoder(v, N):
	s = ''
	for i in range(0, N):
		for num in v:
			s += num[i]
	return s
class GRAY:
	def gray_generator_map(N):
		gray_dict = {}
		for i in range (0, N):
			a = (i - N/2)
			n = a
			if a >= 0:
				a = (i - N/2) + 1
				n = a
			if (abs(n)-1) != 0:
				n = (3*(abs(n)-1))*(n/abs(n))
			gray_dict[i] = [bin(i), n]
		return gray_dict
	def gray_mapping(l1):
		a2 = []
		l2 = 0
		lim2 = (2**l1)/2
		c1 = 0
		c2 = 0
		while 1: #Mapeamento de Bits
			if (c1-lim2) < 0: # Execução da 
				if (c2-lim2) < 0:
					a2.append((c1 - lim2) + 1j*(c2 - lim2))
				else:
					a2.append((c1 - lim2) + 1j*(c2 - (lim2 - 1)))
			else:
				if (c2-lim2) < 0:
					a2.append((c1 - (lim2 - 1)) + 1j*(c2 - lim2))
				else:
					a2.append((c1 - (lim2 - 1)) + 1j*(c2 - (lim2 - 1)))
			c1 += 1
			if c1 == lim2*2:
				c1 = 0
				c2 += 1
			if c2 == lim2*2:
				c2 = 0
				break
		n = np.array(a2)
		print("|X0 Y0|")
		print(n.real)
		print(n.imag)
		sns.set_style("whitegrid")
		plt.axis([-lim2-1, lim2+1, -lim2-1, lim2+1])
		plt.plot(n.real, n.imag, "ko")
		plt.show()

class Modulations:
	def NPAM(v, N): #Geração do Sinal NPAM
		i = 0
		dec = ""
		bin_arr = []
		for num in v:
			dec += str(num)
			i += 1
			if i == 4:
				i = 0
				bin_arr.append(dec)
				dec = ""
		return bin_arr
	def MQAM_Entrelac_TH(v, M, T): # Geração do sinal MQAM Entrelaçado tipo A
		dec = ""
		bin_arr_x0 = []
		lim = max2pow(np.log2(M)) # Execução do logarítimo para iteração
		if lim > 64: # (M <= 64)
			lim = 64
		print("M = {}QAM".format(lim))
		for i in range (0, int(lim)): # Divisão do vetor
			bin_arr_x0.append(np.array(v[int(i*(len(v)/lim)):(i+1)*(int(len(v)/lim))]))
		print(np.array(v))
		print(len(v))
		aux = np.transpose(np.array(bin_arr_x0)) # transposição do vetor
		print(aux)
		a2 = []
		modcpy = commod.QAMModem(lim)
		l1 = 0
		# obtenção das partes reiais e imaginárias a partir da divisão da matriz transposta
		for b in aux: # mapeamento dos bits
			d1 = modcpy.modulate(b)
			l1 = len(d1)
			for i in d1:
				a2.append(i)
		print(np.array(a2))
		
		sns.set_style("whitegrid")
		pd.DataFrame({"X":np.array(a2).real, "Y":np.array(a2).imag}).plot(subplots=True)
		plt.title("Pre-Mod Contellated")
		plt.show()
		s = []
		for a in np.array(a2): # modulação : comnversão para a forma de onda representada com o período T = 16
			t = T
			while t > 0:
				s.append(a.real*np.cos((2*np.pi)/t) + 
					a.imag*np.sin((2*np.pi)/t)*1j)
				t -= 1
		return np.array(s), l1, lim, [np.mean(np.array(a2).real), np.std(np.array(a2).real)], [np.mean(np.array(a2).imag), np.std(np.array(a2).imag)]
	def MQAM_Entrelac_TV(v, M, T): # Geração do sinal MQAM Entrelaçado Tipo B
		dec = ""
		bin_arr_x0 = []
		lim = max2pow(np.log2(M)) # Execução do logarítimo para iteração
		if lim > 16: # (M <= 256)
			lim = 16
		print("M = {}QAM".format(lim))
		for i in range(0, len(v), int(lim)): # Divisão do vetor
			bin_arr_x0.append(np.array(v[i:i+int(lim)]))
		print(np.array(v))
		print(len(v))
		aux = np.transpose(np.array(bin_arr_x0)) # transposição do vetor
		print(aux)
		a2 = []
		l1 = 0
		# obtenção das partes reiais e imaginárias a partir da divisão da matriz transposta
		modcpy = commod.QAMModem(lim)
		# obtenção das partes reiais e imaginárias a partir da divisão da matriz transposta
		for b in aux: # mapeamento dos bits
			d1 = modcpy.modulate(b)
			l1 = len(d1)
			for i in d1:
				a2.append(i)
		print(np.array(a2))
		
		sns.set_style("whitegrid")
		pd.DataFrame({"X":np.array(a2).real, "Y":np.array(a2).imag}).plot(subplots=True)
		plt.title("Pre-Mod Constellated")
		plt.show()
		s = []
		for a in np.array(a2): # modulação
			j = T
			while j > 0:
				s.append(a.real*np.cos((2*np.pi)/j) + 
					a.imag*np.sin((2*np.pi)/j)*1j)
				j -= 1
		return np.array(s), l1
	def MQAM(v, M, T): # Geração do sinal MQAM
		dec = ""
		bin_arr_x0 = []
		lim = max2pow(np.log2(M)) # Execução do logarítimo para iteração
		print(f"{lim} | {len(v)}")
		print(np.array(v))
		for i in range(0, len(v), int(lim)): # Divisão do vetor
			bin_arr_x0.append(np.array(v[i : i + int(lim)]))
		aux = np.array(bin_arr_x0) # transposição do vetor
		print(aux)
		a2 = []
		modcpy = commod.QAMModem(lim)
		l1 = 0
		# obtenção das partes reiais e imaginárias a partir da divisão da matriz transposta
		for b in aux: # mapeamento dos bits
			aux = modcpy.modulate(b)
			l1 = len(aux)
			for num in aux:
				a2.append(num)
			
		print(np.array(a2))

		sns.set_style("whitegrid")
		pd.DataFrame({"X":np.array(a2).real, "Y":np.array(a2).imag}).plot(subplots=True)
		plt.title("Pre-Mod Constellated")
		plt.show()
		s = []
		for a in np.array(a2): # modulação
			j = T
			while j > 0:
				s.append(a.real*np.cos(2*np.pi + (2*np.pi)/j) + 
					a.imag*np.sin(2*np.pi + (2*np.pi/j))*1j)
				j -= 1
		print(f"key = {l1}")
		return np.array(s), l1, lim, [np.mean(np.array(a2).real), np.std(np.array(a2).real)], [np.mean(np.array(a2).imag), np.std(np.array(a2).imag)]
	def MQPSK(v, M, T): #Geração do sinal MQAM
		dec = ""
		bin_arr_x0 = []
		lim = max2pow(np.log2(M)) # Execução do logarítimo para iteração
		print(f"{lim} | {len(v)}")
		print(np.array(v))
		for i in range(0, len(v), int(lim)): # Divisão do vetor
			bin_arr_x0.append(np.array(v[i : i + int(lim)]))
		aux = np.array(bin_arr_x0) # transposição do vetor
		a2 = []
		# obtenção das partes reiais e imaginárias a partir da divisão da matriz transposta
		modcpy = commod.QAMModem(lim)
		l1 = 0
		# obtenção das partes reiais e imaginárias a partir da divisão da matriz transposta
		for b in aux: # mapeamento dos bits
			aux = modcpy.modulate(b)
			l1 = len(aux)
			for num in aux:
				a2.append(num)
			
		print(np.array(a2))

		sns.set_style("whitegrid")
		pd.DataFrame({"X":np.array(a2).real, "Y":np.array(a2).imag}).plot(subplots=True)
		plt.title("Pre-Mod Constellated")
		plt.show()
		s = []
		gs = pskf.cosAdjust(np.array(a2).real) - pskf.sinAdjust(np.array(a2).imag)*1j
		for a in gs:
			j = T
			while j > 0:
				s.append(a)
				j -= 1
		return np.array(s), l1, lim, [np.mean(np.array(a2).real), np.std(np.array(a2).real)], [np.mean(np.array(a2).imag), np.std(np.array(a2).imag)]
# signal, key, M, f1, f2
class PassFilters:
	def RcossineFilter(s, f, f1, B):
		f0 = abs(f)
		fLim = 2*B - f1
		sf = []
		if f0 < fLim & f0 > f1:
			for i in range(0, len(s)):
				sf.append(s[i]*(1/4*B)*(1 - np.sin(np.pi*(f0 - B))/(2*B - 2*f1) + 
					sin((i+1)*np.pi*(f0 - B))/(2*B - 2*f1)))
		elif f0 < f1 & f0 >= 0:
			for i in range(0, len(s)):
				sf.append(s[i]*(1/2*B))
		else:
			for i in range(0, len(s)):
				sf.append(0)
		return sf


	def NyquistFilter(s, f, B):
		sf = []
		for i in range(0, len(s)):
			sf.append(np.sin(2*pi*B*(i+1)/(len(s)/4))/(2*pi*B*(i+1)/(len(s)/4)))
		return np.array(sf)

class DePassFilters:
	def RCossineFilter(s, f, f1, B):
		f0 = abs(f)
		fLim = 2*B - f1
		sf = []
		if f0 < fLim & f0 > f1:
			for i in range(0, len(s)):
				sf.append(s[i]/(1/4*B)*(1 - np.sin(np.pi*(f0 - B))/(2*B - 2*f1) + 
					sin((i+1)*np.pi*(f0 - B))/(2*B - 2*f1)))
		elif f0 < f1 & f0 >= 0:
			for i in range(0, len(s)):
				sf.append(s[i]/(1/2*B))
		else:
			for i in range(0, len(s)):
				sf.append(0)
		return sf


	def NyquistFilter(s, f, B):
		sf = []
		for i in range(0, len(s)):
			sf.append((np.arcsin(2*pi*B*(i+1)*(len(s)/4))/(2*pi*B*(i+1)/(len(s)/4))))
		return np.array(sf)

def Decode_vec(v):
	vm = []
	r = []
	n = []
	c = 0
	for e in v:
		if(len(r) != 0):
			if e in r:
				n[r.index(e)] += 1
			else:
				r.append(e)
				n.append(1)
		else:
			r.append(e)
			n.append(1)
		c += 1
		if c == 100:
			vm.append(r[n.index(max(n))])
			r = []
			n = []
			c = 0
	return vm;

class Demodulations:
	def get0signal(x, y, M):
		lim = np.log2(M)
		rs = []
		for i in range(0, len(x)):
			aux_a = bin(x[i])
			aux_b = bin(y[i])
			xa = aux_a.split('b')[1]
			xb = aux_b.split('b')[1]
			la = len(xa.split(''))
			lb = len(xb.split(''))
			c = lim/2
			aux_xa = ""
			for j in range (0, lim/2):
				if(c > la):
					aux_xa += "0"
				else:
					aux_xa += xa
					break
				c -= 1
			c = lim/2
			aux_xb = ""
			for j in range (0, lim/2):
				if(c > lb):
					aux_xb += "0"
				else:
					aux_xb += xa
					break
				c -= 1
			rs.append(aux_xa + aux_xb)
		print(np.array(rs))
	def De_MQAM(signal, key, M, T):
		modcpy = commod.QAMModem(M)
		xdm = []
		xgm = []
		for i in range(0, len(signal)):
			if(i%T == 0) & (i > 0):
				xgm.append(np.mean(xdm))
				xdm = []
			xaux = signal[i].real/np.cos(2*np.pi + 2*np.pi/(T - i%T)) + 1j*signal[i].imag/np.sin(2*np.pi + 2*np.pi/(T - i%T))
			xdm.append(xaux)
		xgm.append(np.mean(xdm))
		print(pd.DataFrame({"Xdm":np.array(xgm).real, "Ydm":np.array(xgm).imag}))
		sns.set_style("whitegrid")
		pd.DataFrame({"X":np.array(xgm).real, "Y":np.array(xgm).imag}).plot(subplots=True)
		plt.title("Sinal Reconstruído")
		plt.show()
		r1 = []
		aux = []
		for i in range(0, len(xgm), key):
			r1.append(modcpy.demodulate(xgm[i: i+key], demod_type="hard"))
		print(np.array(r1))
		rec = []
		r1 = np.array(r1)
		for v in r1:
			for num in v:
				rec.append(num)
		return rec
	
	def De_MQAM_Entrelac_TV(signal, key, M, T):
		modcpy = commod.QAMModem(M)
		xdm = []
		xgm = []
		for i in range(0, len(signal)):
			if(i%T == 0) & (i > 0):
				xgm.append(np.mean(xdm))
				xdm = []
			xaux = signal[i].real/np.cos(2*np.pi/(T - i%T)) + 1j*signal[i].imag/np.sin(2*np.pi/(T - i%T))
			xdm.append(xaux)
		xgm.append(np.mean(xdm))
		print(pd.DataFrame({"Xdm":np.array(xgm).real, "Ydm":np.array(xgm).imag}))
		sns.set_style("whitegrid")
		pd.DataFrame({"X":np.array(xgm).real, "Y":np.array(xgm).imag}).plot(subplots=True)
		plt.title("Sinal Reconstruído")
		plt.show()
		r1 = []
		aux = []
		for i in range(0, len(xgm), key):
			r1.append(modcpy.demodulate(xgm[i: i+key], demod_type="hard"))
		print(np.array(r1))
		rech = np.transpose(np.array(r1))
		rec = []
		for vec in rech:
			for i in vec:
				rec.append(i)
		return rec

	def De_MQAM_Entrelac_TH(signal, key, M, T):
		modcpy = commod.QAMModem(M)
		xdm = []
		xgm = []
		for i in range(0, len(signal)):
			if(i%T == 0) & (i > 0):
				xgm.append(np.mean(xdm))
				xdm = []
			xaux = signal[i].real/np.cos(2*np.pi/(T - i%T)) + 1j*signal[i].imag/np.sin(2*np.pi/(T - i%T))
			xdm.append(xaux)
		xgm.append(np.mean(xdm))
		print(pd.DataFrame({"Xdm":np.array(xgm).real, "Ydm":np.array(xgm).imag}))
		sns.set_style("whitegrid")
		pd.DataFrame({"X":np.array(xgm).real, "Y":np.array(xgm).imag}).plot(subplots=True)
		plt.title("Sinal Reconstruído")
		plt.show()
		r1 = []
		aux = []
		for i in range(0, len(xgm), key):
			r1.append(modcpy.demodulate(xgm[i: i+key], demod_type="hard"))
		print(np.array(r1))
		rec2 = np.transpose(np.array(r1))
		print(rec2)
		recf = []
		for num in rec2:
			for i in num:
				recf.append(i)
		return recf

	def De_MQPSK(signal, M, key, T):
		s = pskf.cosFilter(signal.real, False) - pskf.sinFilter(signal.imag, True)
		#print(pd.DataFrame({'X':x, 'Y':y}))
		ygm = []
		for i in range(0, len(s), T):
			ygm.append(np.mean(s[i:i+key]))
			#print(f"{aux_X} | {aux_Y}")
		print(pd.DataFrame({"Xgm":np.array(ygm).real, "Ygm":np.array(ygm).imag}))
		sns.set_style("whitegrid")
		pd.DataFrame({"X":np.array(ygm).real, "Y":np.array(ygm).imag}).plot(subplots=True)
		plt.title("Sinal Reconstituído")
		plt.show()
		for i in range(0, len(xgm), key):
			r1.append(modcpy.demodulate(xgm[i: i+key], demod_type="hard"))
		print(np.array(r1))
		return np.array(r1)

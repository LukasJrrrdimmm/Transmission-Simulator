import math as mth
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import commpy.modulation as commod
import mpskadjust as pskf
import carrier as crr
import scipy.fft as FFT

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
	def MPAM(v, M, T):
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
	def MQAM_Entrelac_TH(v, sz, M, T): # Geração do sinal MQAM Entrelaçado tipo A
		"""
		v = mensagem de Entrada
		M = nº da modulação
		T = periodo do quadro
		"""
		dec = ""
		bin_arr_x0 = []
		lim = max2pow(np.log2(sz)) # Execução do logarítimo para iteração
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
		modcpy = commod.QAMModem(M)
		l1 = 0
		# obtenção das partes reiais e imaginárias a partir da divisão da matriz transposta
		for b in aux: # mapeamento dos bits
			d1 = modcpy.modulate(b)
			l1 = len(d1)
			for i in d1:
				a2.append(i)
		a2 = np.array(a2)
		qam_real = a2.real
		qam_img = a2.imag
		m = []
		f, t = crr.Generic_Carrier(T, period=False)
		print(f"{f} , {t}")
		sns.set_style("whitegrid")
		pd.DataFrame({"X":qam_real, "Y":qam_img}).plot(subplots=True)
		plt.title("Pre-Mod Constellated")
		plt.show()
		for k in range(0,len(qam_real)):
			yr=qam_real[k]*np.cos(2*np.pi*f*t)
			yim=qam_img[k]*np.sin(2*np.pi*f*t)           
			y=[a + b for a, b in zip(yr, yim*1j)]
			m = m + y
		c1 = np.cos(2*np.pi*f*t)
		return np.array(m), l1, len(c1)
	def MQAM_Entrelac_TV(v, sz, M, T): # Geração do sinal MQAM Entrelaçado Tipo B
		"""
		v = mensagem de Entrada
		M = nº da modulação
		T = periodo do quadro
		"""
		dec = ""
		bin_arr_x0 = []
		lim = max2pow(np.log2(sz)) # Execução do logarítimo para iteração
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
		modcpy = commod.QAMModem(M)
		# obtenção das partes reiais e imaginárias a partir da divisão da matriz transposta
		for b in aux: # mapeamento dos bits
			d1 = modcpy.modulate(b)
			l1 = len(d1)
			for i in d1:
				a2.append(i)
		a2 = np.array(a2)
		qam_real = a2.real
		qam_img = a2.imag
		m = []
		f, t = crr.Generic_Carrier(T, period=False)
		print(f"{f} , {t}")
		sns.set_style("whitegrid")
		pd.DataFrame({"X":qam_real, "Y":qam_img}).plot(subplots=True)
		plt.title("Pre-Mod Constellated")
		plt.show()
		for k in range(0,len(qam_real)):
			yr=qam_real[k]*np.cos(2*np.pi*f*t)
			yim=qam_img[k]*np.sin(2*np.pi*f*t)           
			y=[a + b for a, b in zip(yr, yim*1j)]
			m = m + y
		c1 = np.cos(2*np.pi*f*t)
		return np.array(m), l1, len(c1)

	def MQAM(v, M, T): # Geração do sinal MQAM
		"""
		v = mensagem de Entrada
		M = nº da modulação
		T = periodo do quadro
		"""
		modcpy = commod.QAMModem(M)
		a2 = modcpy.modulate(v)
		qam_real = a2.real
		qam_img = a2.imag
		m = []
		q = []
		i = []
		f, t = crr.Generic_Carrier(T, period=False)
		print(f"{f} , {t}")
		sns.set_style("whitegrid")
		pd.DataFrame({"X":qam_real, "Y":qam_img}).plot(subplots=True)
		plt.title("Pre-Mod Constellated")
		plt.show()
		for k in range(0,len(qam_real)):
			yr=qam_real[k]*np.cos(2*np.pi*f*t)
			yim=qam_img[k]*np.sin(2*np.pi*f*t)           
			y=[a + b for a, b in zip(yr, yim)]
			m = m+y
			q = q + list(yr)
			i = i + list(yim)
		c1 = np.cos(2*np.pi*f*t)
		return np.array(m), np.array(q), np.array(i)# s(t), T
	def MQPSK(v, sz, M, T): #Double-MPSK geração de 2 sinais MPSK: 1 em fase e 1 em quadratura 
		"""
		v = mensagem de Entrada
		sz = tamanho da mensagem
		M = nº da modulação
		T = periodo do quadro
		"""
		dec = ""
		print(np.array(v))
		# obtenção das partes reiais e imaginárias a partir da divisão da matriz transposta
		modcpy = commod.QAMModem(M)
		# obtenção das partes reiais e imaginárias a partir da divisão da matriz transposta
		a2 = modcpy.modulate(v)
		print(np.array(a2))

		sns.set_style("whitegrid")
		pd.DataFrame({"X":np.array(a2).real, "Y":np.array(a2).imag}).plot(subplots=True)
		plt.title("Pre-Mod Constellated")
		plt.show()
		s = []
		gs = pskf.cosAdjust(np.array(a2).real, T, M) + pskf.sinAdjust(np.array(a2).imag, T, M)*1j
		print(np.array(gs))
		f, t = crr.Generic_Carrier(T, period=False)
		c1 = np.cos(2*np.pi*f*t)
		return np.array(gs), len(c1)
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
	def De_MQAM(signal, M, T, flf):
		"""
		signal = sinal modulado
		M = nº da modulação
		key = chave de desentrelaçamento da constelação
		T = período do cada quadro
		"""
		modcpy = commod.QAMModem(M)
		ygm = crr.CarrierDemodeQAM(signal, T, flf)
		print(pd.DataFrame({"Xdm":np.array(ygm).real, "Ydm":np.array(ygm).imag}))
		sns.set_style("whitegrid")
		pd.DataFrame({"X":np.array(ygm).real, "Y":np.array(ygm).imag}).plot(subplots=True)
		plt.title("Sinal Reconstruído")
		plt.show()
		r1 = modcpy.demodulate(ygm, demod_type="hard")
		print(np.array(r1))
		return np.array(r1)
	def De_MQAM_Entrelac_TV(signal, key, M, T):
		"""
		signal = sinal modulado
		M = nº da modulação
		key = chave de desentrelaçamento da constelação
		T = período do cada quadro
		"""
		modcpy = commod.QAMModem(M)
		ygm = crr.CarrierDemodeQAM(signal, T)
		print(pd.DataFrame({"Xdm":np.array(ygm).real, "Ydm":np.array(ygm).imag}))
		sns.set_style("whitegrid")
		pd.DataFrame({"X":np.array(ygm).real, "Y":np.array(ygm).imag}).plot(subplots=True)
		plt.title("Sinal Reconstruído")
		plt.show()
		r1 = []
		aux = []
		for i in range(0, len(ygm), key):
			r1.append(modcpy.demodulate(ygm[i: i+key], demod_type="hard"))
		print(np.array(r1))
		rech = np.transpose(np.array(r1))
		rec = []
		for vec in rech:
			for i in vec:
				rec.append(i)
		return rec
	def De_MQAM_Entrelac_TH(signal, key, M, T):
		"""
		signal = sinal modulado
		M = nº da modulação
		key = chave de desentrelaçamento da constelação
		T = período do cada quadro
		"""
		modcpy = commod.QAMModem(M)
		ygm = crr.CarrierDemodeQAM(signal, T)
		print(pd.DataFrame({"Xdm":np.array(ygm).real, "Ydm":np.array(ygm).imag}))
		sns.set_style("whitegrid")
		pd.DataFrame({"X":np.array(ygm).real, "Y":np.array(ygm).imag}).plot(subplots=True)
		plt.title("Sinal Reconstruído")
		plt.show()
		r1 = []
		aux = []
		for i in range(0, len(ygm), key):
			r1.append(modcpy.demodulate(ygm[i: i+key], demod_type="hard"))
		print(np.array(r1))
		rec2 = np.transpose(np.array(r1))
		print(rec2)
		recf = []
		for num in rec2:
			for i in num:
				recf.append(i)
		return recf
	def De_MQPSK(signal, M, T):# D-MPSK
		"""
		signal = sinal modulado
		M = nº da modulação
		key = chave de desentrelaçamento da constelação
		T = período do cada quadro
		"""
		modcpy = commod.QAMModem(M)
		s = crr.CarrierDemodePSK(signal, T, M)
		#ygm = pskf.cosFilter(s.real, False) - pskf.sinFilter(s.imag, True)
		print(pd.DataFrame({"Xgm":s.real, "Ygm":s.imag}))
		sns.set_style("whitegrid")
		pd.DataFrame({"X":s.real, "Y":s.imag}).plot(subplots=True)
		plt.title("Sinal Reconstituído")
		plt.show()
		r1 = modcpy.demodulate(s, demod_type="hard")
		print(np.array(r1))
		return np.array(r1)

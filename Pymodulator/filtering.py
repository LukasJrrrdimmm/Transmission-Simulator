import math as mth
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def binary_generator(s, N):
		return np.random.randint(2, size = s**N)

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
	def MQAM_Entrelac_TH(v, M): # Geração do sinal MQAM Entrelaçado tipo A
		dec = ""
		bin_arr_x0 = []
		lim = np.log2(M) # Execução do logarítimo para iteração
		for i in range (0, int(lim)): # Divisão do vetor
			bin_arr_x0.append(np.array(v[int(i*(len(v)/lim)):(i+1)*(int(len(v)/lim))]))
		print(np.array(v))
		print(len(v))
		aux = np.transpose(np.array(bin_arr_x0)) # transposição do vetor
		print(aux)
		a2 = []
		a1 = []
		# obtenção das partes reiais e imaginárias a partir da divisão da matriz transposta
		for b in aux: # mapeamento dos bits
			l1 = len(b)
			l2 = mth.ceil(len(b)/2)
			ax = b[0:l2]
			ay = b[l2:l1]
			d = 2**l2
			aux2r = ""
			for i in ax:
				aux2r += str(i)
			aux2i = ""
			for i in ay:
				aux2i += str(i)
			z1 = [int(aux2r, 2), int(aux2i,2)]
			z2 = []
			for num in z1:
				if(num - d/2 < 0):
					z2.append(float(num - d/2))
				else:
					z2.append(float((num - d/2) + 1))
			a1.append(z1[0] + 1j*z1[1])
			a2.append(z2[0] + 1j*z2[1])
		GRAY.gray_mapping(l2)
		print(np.array(a2))
		sns.set_style("whitegrid")
		pd.DataFrame({"X":np.array(a1).real, "Y":np.array(a1).imag}).plot(subplots=True)
		plt.title("Pre-Mod")
		plt.show()
		
		sns.set_style("whitegrid")
		pd.DataFrame({"X":np.array(a2).real, "Y":np.array(a2).imag}).plot(subplots=True)
		plt.title("Pre-Mod-Gray")
		plt.show()
		s = []
		for a in np.array(a2): # modulação
			j = 16
			while j > 0:
				s.append(a.real*np.cos((2*np.pi)/j) + 
					a.imag*np.sin((2*np.pi)/j)*1j)
				j -= 1
		return np.array(s), d
	def MQAM_Entrelac_TV(v, M): # Geração do sinal MQAM Entrelaçado Tipo B
		dec = ""
		bin_arr_x0 = []
		lim = np.log2(M) # Execução do logarítimo para iteração
		for i in range(0, len(v), int(lim)): # Divisão do vetor
			bin_arr_x0.append(np.array(v[i:i+int(lim)]))
		print(np.array(v))
		print(len(v))
		aux = np.transpose(np.array(bin_arr_x0)) # transposição do vetor
		print(aux)
		a2 = []
		a1 = []
		# obtenção das partes reiais e imaginárias a partir da divisão da matriz transposta
		for b in aux: # mapeamento dos bits
			l1 = len(b)
			l2 = mth.ceil(len(b)/2)
			ax = b[0:l2]
			ay = b[l2:l1]
			d = 2**l2
			aux2r = ""
			for i in ax:
				aux2r += str(i)
			aux2i = ""
			for i in ay:
				aux2i += str(i)
			z1 = [int(aux2r, 2), int(aux2i,2)]
			z2 = []
			for num in z1:
				if(num - d/2 < 0):
					z2.append(float(num - d/2))
				else:
					z2.append(float((num - d/2) + 1))
			a1.append(z1[0] + 1j*z1[1])
			a2.append(z2[0] + 1j*z2[1])
		GRAY.gray_mapping(l2)
		print(np.array(a2))
		sns.set_style("whitegrid")
		pd.DataFrame({"X":np.array(a1).real, "Y":np.array(a1).imag}).plot(subplots=True)
		plt.title("Pre-Mod")
		plt.show()
		
		sns.set_style("whitegrid")
		pd.DataFrame({"X":np.array(a2).real, "Y":np.array(a2).imag}).plot(subplots=True)
		plt.title("Pre-Mod-Gray")
		plt.show()
		s = []
		for a in np.array(a2): # modulação
			j = 16
			while j > 0:
				s.append(a.real*np.cos((2*np.pi)/j) + 
					a.imag*np.sin((2*np.pi)/j)*1j)
				j -= 1
		return np.array(s), d
	def MQAM(v, M): # Geração do sinal MQAM
		dec = ""
		bin_arr_x0 = []
		lim = np.log2(M) # Execução do logarítimo para iteração
		print(f"{lim} | {len(v)}")
		print(np.array(v))
		for i in range(0, len(v), int(lim)): # Divisão do vetor
			bin_arr_x0.append(np.array(v[i : i + int(lim)]))
		aux = np.array(bin_arr_x0) # transposição do vetor
		print(aux)
		a2 = []
		a1 = []
		# obtenção das partes reiais e imaginárias a partir da divisão da matriz transposta
		for b in aux: # mapeamento dos bits
			l1 = len(b)
			l2 = mth.ceil(len(b)/2)
			ax = b[0:l2]
			ay = b[l2:l1]
			d = 2**l2
			aux2r = ""
			for i in ax:
				aux2r += str(i)
			aux2i = ""
			for i in ay:
				aux2i += str(i)
			z1 = [int(aux2r, 2), int(aux2i,2)]
			z2 = []
			for num in z1:
				if(num - d/2 < 0):
					z2.append(float(num - d/2))
				else:
					z2.append(float((num - d/2) + 1))
			a1.append(z1[0] + 1j*z1[1])
			a2.append(z2[0] + 1j*z2[1])
		print(np.array(a2))
		GRAY.gray_mapping(l2)
		sns.set_style("whitegrid")
		pd.DataFrame({"X":np.array(a1).real, "Y":np.array(a1).imag}).plot(subplots=True)
		plt.title("Pre-Mod")
		plt.show()
		sns.set_style("whitegrid")
		pd.DataFrame({"X":np.array(a2).real, "Y":np.array(a2).imag}).plot(subplots=True)
		plt.title("Pre-Mod-Gray")
		plt.show()
		s = []
		for a in np.array(a2): # modulação
			j = 16
			while j > 0:
				s.append(a.real*np.cos((2*np.pi)/j) + 
					a.imag*np.sin((2*np.pi)/j)*1j)
				j -= 1
		return np.array(s), d
	def MQPSK(v, M): #Geração do sinal MQAM
		dec = ""
		bin_arr_x0 = []
		lim = np.log2(M) # Execução do logarítimo para iteração
		for i in range (0, int(lim)): # Divisão do vetor
			bin_arr_x0.append(np.array(v[int(i*(len(v)/lim)):(i+1)*(int(len(v)/lim))]))
		print(np.array(v))
		print(len(v))
		aux = np.transpose(np.array(bin_arr_x0)) # transposição do vetor
		print(aux)
		a2 = []
		# obtenção das partes reiais e imaginárias a partir da divisão da matriz transposta
		a1 = []
		# obtenção das partes reiais e imaginárias a partir da divisão da matriz transposta
		for b in aux: # mapeamento dos bits
			l1 = len(b)
			l2 = mth.ceil(len(b)/2)
			ax = b[0:l2]
			ay = b[l2:l1]
			d = 2**l2
			aux2r = ""
			for i in ax:
				aux2r += str(i)
			aux2i = ""
			for i in ay:
				aux2i += str(i)
			z1 = [int(aux2r, 2), int(aux2i,2)]
			z2 = []
			for num in z1:
				if(num - d/2 < 0):
					z2.append(float(num - d/2))
				else:
					z2.append(float((num - d/2) + 1))
			a1.append(z1[0] + 1j*z1[1])
			a2.append(z2[0] + 1j*z2[1])
		print(np.array(a2))
		GRAY.gray_mapping(l2)
		sns.set_style("whitegrid")
		pd.DataFrame({"X":np.array(a1).real, "Y":np.array(a1).imag}).plot(subplots=True)
		plt.title("Pre-Mod")
		plt.show()
		
		sns.set_style("whitegrid")
		pd.DataFrame({"X":np.array(a2).real, "Y":np.array(a2).imag}).plot(subplots=True)
		plt.title("Pre-Mod-Gray")
		plt.show()
		s = []
		for a in np.array(a2):
			s.append(np.cos((2*np.pi)/a.real) + 
				np.sin((2*np.pi)/a.imag)*1j)
		return np.array(s), d

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
	def De_MQAM(signal, d):
		x = signal.real
		y = signal.imag
		print(pd.DataFrame({"X":x, "Y":y}))
		xdm = []
		ydm = []
		xgm = []
		ygm = []
		for i in range(0, len(x)):
			if(i%16 == 0) & (i > 0):
				xgm.append(np.mean(xdm))
				xdm = []
				ygm.append(np.mean(ydm))
				ydm = []
			xaux = x[i]/np.cos(2*np.pi/(16 - i%16))
			if xaux < 0:
				xdm.append(xaux + d/2)
			else:
				xdm.append(xaux + (d/2 - 1))
			yaux = y[i]/np.sin(2*np.pi/(16 - i%16))
			if yaux < 0:
				ydm.append(yaux + d/2)
			else:
				ydm.append(yaux + (d/2 - 1))
		xgm.append(np.mean(xdm))
		ygm.append(np.mean(ydm))
		print(pd.DataFrame({"Xdm":xgm, "Ydm":ygm}))
		sns.set_style("whitegrid")
		pd.DataFrame({"X":xgm, "Y":ygm}).plot(subplots=True)
		plt.title("Sinal Reconstruído")
		plt.show()
		bin_x = itob_array(xgm, np.log2(d))
		bin_y = itob_array(ygm, np.log2(d))
		rec = []
		for i in range(0, len(bin_x)):
			for j in bin_x[i]:
				rec.append(int(j))
			for j in bin_y[i]:
				rec.append(int(j))
		print(np.array(rec))
		return rec
	
	def De_MQAM_Entrelac_TV(signal, d):
		x = signal.real
		y = signal.imag
		print(pd.DataFrame({"X":x, "Y":y}))
		xdm = []
		ydm = []
		xgm = []
		ygm = []
		for i in range(0, len(x)):
			if(i%16 == 0) & (i > 0):
				xgm.append(np.mean(xdm))
				xdm = []
				ygm.append(np.mean(ydm))
				ydm = []
			xaux = x[i]/np.cos(2*np.pi/(16 - i%16))
			if xaux < 0:
				xdm.append(xaux + d/2)
			else:
				xdm.append(xaux + (d/2 - 1))
			yaux = y[i]/np.sin(2*np.pi/(16 - i%16))
			if yaux < 0:
				ydm.append(yaux + d/2)
			else:
				ydm.append(yaux + (d/2 - 1))
		xgm.append(np.mean(xdm))
		ygm.append(np.mean(ydm))
		print(pd.DataFrame({"Xdm":xgm, "Ydm":ygm}))
		sns.set_style("whitegrid")
		pd.DataFrame({"X":xgm, "Y":ygm}).plot(subplots=True)
		plt.title("Sinal Reconstruído")
		plt.show()
		bin_x = filt.itob_array(xdm, np.log2(d))
		bin_y = filt.itob_array(ydm, np.log2(d))
		recm = []
		for i in range(0, len(bin_x)):
			aux = []
			for n in bin_x[i]:
				aux.append(n)
			for n in bin_y[y]:
				aux.append(n)
			recm.append(aux)
		rech = np.transpose(np.array(recm))
		rec = []
		for vec in rech:
			for i in vec:
				rec.append(i)
		return rec

	def De_MQAM_Entrelac_TH(signal, d):
		x = signal.real
		y = signal.imag
		print(pd.DataFrame({"X":x, "Y":y}))
		xdm = []
		ydm = []
		xgm = []
		ygm = []
		for i in range(0, len(x)):
			if(i%16 == 0) & (i > 0):
				xgm.append(np.mean(xdm))
				xdm = []
				ygm.append(np.mean(ydm))
				ydm = []
			xaux = x[i]/np.cos(2*np.pi/(16 - i%16))
			if xaux < 0:
				xdm.append(xaux + d/2)
			else:
				xdm.append(xaux + (d/2 - 1))
			yaux = y[i]/np.sin(2*np.pi/(16 - i%16))
			if yaux < 0:
				ydm.append(yaux + d/2)
			else:
				ydm.append(yaux + (d/2 - 1))
		xgm.append(np.mean(xdm))
		ygm.append(np.mean(ydm))
		print(pd.DataFrame({"Xdm":xgm, "Ydm":ygm}))
		sns.set_style("whitegrid")
		pd.DataFrame({"X":xgm, "Y":ygm}).plot(subplots=True)
		plt.title("Sinal Reconstruído")
		plt.show()
		bin_x = itob_array(xgm, np.log2(d))
		bin_y = itob_array(ygm, np.log2(d))
		rec = []
		for i in range(0, len(bin_x)):
			aux = []
			for n in bin_x[i]:
				aux.append(int(n))
			for n in bin_y[i]:
				aux.append(int(n))
			rec.append(aux)
		print(np.array(rec))
		rec2 = np.transpose(np.array(rec))
		print(rec2)
		recf = []
		for num in rec2:
			for i in num:
				recf.append(i)
		print(recf)
		return recf

	def De_MQPSK(signal, M, d):
		x = signal.real
		y = signal.imag
		xdm = []
		ydm = []
		xgm = []
		ygm = []
		for i in range(0, len(x)):
			aux_X = ((np.arccos(x[i])**(-1))*np.pi)
			if aux_X < 0:
				xdm.append(aux_X + d/2)
			else:
				xdm.append(aux_X + (d/2 - 1))
			xgm.append(xdm[i])
			aux_Y = ((np.arcsin(y[i])**(-1))*np.pi)
			if aux_Y < 0:
				ydm.append(aux_Y + d/2)
			else:
				ydm.append(aux_Y + (d/2 - 1))
			ygm.append(aux_Y)
		print(pd.DataFrame({"Xgm":xdm, "Ygm":ydm}))
		sns.set_style("whitegrid")
		pd.DataFrame({"X":xgm, "Y":ygm}).plot(subplots=True)
		plt.title("Sinal Reconstituído")
		plt.show()
		print(pd.DataFrame({"Xdm":xdm, "Ydm":ydm}))
		bin_x = filt.itob_array(xdm, np.log2(M))
		bin_y = filt.itob_array(ydm, np.log2(M))
		rec = []
		for i in range(0, len(bin_x)):
			for j in bin_x[i]:
				rec.append(j)
			for j in bin_y[i]:
				rec.append(j)
		print(np.array(rec))
		return rec


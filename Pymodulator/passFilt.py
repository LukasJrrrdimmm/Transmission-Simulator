import numpy as np
import math as mth

class binary_conversor:
	def arrayNPAM(v, N):
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
				
class gray_scheme:
	def binary_gnerator(s, N):
		n = np.random.randint(2, size = s*N)
		return n
	def gray_generator(N):
		gray_dict = {}
		for i in range (0, N):
			a = (i - N/2)
			if a >= 0:
				a =  (i - mth.floor(N/2)) + 1
			gray_dict[i] = [bin(i), a*3]
		return(gray_dict)
	def encode_gray(v, g):
		decode_vec = []
		for num in v:
			for e in g:
				aux = e[0]
				if int(num,2) == int(aux[0],2):
					vec.append(aux[1])
					break
		return decode_vec

class RCossin:
	p0 = 1
	def Process(pulse, B, f, f1):
		l = len(pulse)
		m_signal = []
		print("{} + {} + {}".format(f, f1, 2*B - f1))
		if f >= 0 & f < f1:
			m_signal = RCossin.R1(pulse, B, f, f1)
		elif f >= f1 & f < 2*B - f1:
			m_signal = RCossin.R2(pulse, B, f, f1)
		else:
			m_signal = RCossin.R3(pulse, B, f, f1)
		print(m_signal)
		return m_signal

	def R1(pulse, B, f, f1):
		irn = []
		c = 0
		for num in pulse:
			irn.append(RCossin.p0/(2*B))
		return irn

	def R2(pulse, B, f, f1):
		irn = []
		c = 0
		for num in pulse:
			c += 1
			irn.append((RCossin.p0/(4*B))*(1 + np.cos(((np.pi/16)*(f - f1))*c)/(2*B-f1)))
		return irn

	def R3(pulse, B, f, f1):
		irn = []
		for num in pulse:
			irn.append(0)
		return irn

	def Alpha(B, f1):
		a = 1 - f1/B
		return a

class Convolute:
	def C_Filter(a1, a2):
		for i in range(0, len(a1)):
			s1.append(a1[i]*np.cos((np.pi/8)*fp*((i+1)/100)))
			s2.append(a2[i]*np.sin((np.pi/8)*fp*((i+1)/100)))
		return s1, s2

class Nyquist:
	def N_Filter(a1, a2):
		print("Implementação do Filtro de Nyquist")

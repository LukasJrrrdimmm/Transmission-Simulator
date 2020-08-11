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
	def Re_arrayMQAM(v, M):
		i = 0
		dec = ""
		bin_arr_x0 = []
		lim = np.log2(M)
		for i in range (0, int(lim)):
			bin_arr_x0.append(np.array(v[int(i*(len(v)/lim)):(i+1)*(int(len(v)/lim))]))
			i += 1
		print(np.array(v))
		print(len(v))
		print(np.transpose(np.array(bin_arr_x0)))
		print(np.shape(bin_arr_x0))
		bin_arr_x = []
		for arr in np.transpose(bin_arr_x0):
			print(arr)
			aux = ""
			i = 0.0
			j = 0
			while j < len(arr):
				if i < float(j):
					bin_arr_x.append(complex(int(aux, 2)).real*np.cos(2*np.pi + 
						i*(2*np.pi)))
					i += 0.1
				else:
					for k in range(0, len(arr)):
						aux += str(arr[k])
					j += 1
		print(np.array(bin_arr_x))
		return bin_arr_x
	def Im_arrayMQAM(v, M):
		i = 0
		dec = ""
		bin_arr_x0 = []
		lim = np.log2(M)
		for i in range (0, int(lim)):
			bin_arr_x0.append(np.array(v[int(i*(len(v)/lim)):(i+1)*(int(len(v)/lim))]))
			i += 1
		print(np.array(v))
		print(len(v))
		print(np.transpose(np.array(bin_arr_x0)))
		print(np.shape(bin_arr_x0))
		bin_arr_x = []
		for arr in np.transpose(bin_arr_x0):
			print(arr)
			aux = ""
			i = 0.0
			j = 0
			while j < len(arr):
				if i < float(j):
					bin_arr_x.append((int(aux, 2)*1j).imag*np.sin(2*np.pi + 
						i*(2*np.pi)))
					i += 0.1
				else:
					aux = ""
					for k in range(0, len(arr)):
						aux += str(arr[k])
					j += 1
		print(np.array(bin_arr_x))
		return bin_arr_x
				
class gray_scheme:
	def binary_gnerator(s, N):
		n = np.random.randint(2, size = s*N)
		return n
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
		return(gray_dict, n)
	def gray_mapping(v, dct, m):
		x0 = []
		x = []
		i = 0
		for n in v:
			x0 = []
			print(n)
			aux = list(n)
			a1 = ""
			a2 = ""
			for i in range(0, len(aux)):
				if i < len(aux)/2:
					a1 += aux[i]
				else:
					a2 += aux[i]
			x.append(a1)
			y.append(a2)
		print("|X0 Y0|")
		print(x)
		print(y)
		x1 = gray_scheme.encode_gray(x, dct)
		y1 = gray_scheme.encode_gray(y, dct)
		return x1, y1
				
	def gray_generator_MQAM(M):
		gray_dict = {}
		aux = np.log2(M)
		for i in range (0, int(aux)):
			a = (i - aux/2)
			n = a
			if a >= 0:
				a = (i - aux) + 1
				n = a
			if (abs(n)-1) != 0:
				n = (3*(abs(n)-1))*(n/abs(n))
			gray_dict[i] = [bin(i), n]
		return(gray_dict, aux)
	def encode_gray(v, dct):
		decode_vec = []
		test_vec = []
		for num in v:
			for e in dct:
				#print(e)
				aux = dct[e]
				#print(aux)
				a = int(num,2)
				b = int(aux[0],2)
				#print(" {} | {} ".format(a, b))
				if a == b:
					decode_vec.append(aux[1])
					test_vec.append(b)
					break
		print("testvec = {}".format(test_vec))
		return decode_vec

class RCossin:
	p0 = 1
	def Process(pulse, B, f, f1):
		l = len(pulse)
		m_signal = []
		print("{} + {} + {}".format(f, f1, 2*B - f1))
		if abs(f) >= 0 & abs(f) < f1:
			m_signal = RCossin.R1(pulse, B, f, f1)
		elif abs(f) >= f1 & abs(f) < 2*B - f1:
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
			#irn.append((RCossin.p0/(4*B))*(1 + np.cos(((np.pi/16)*(f - f1))*c)/(2*B-f1)))
			irn.append((RCossin.p0/(4*B))*(1 + np.sin(((np.pi/16)*(f - f1))*c)/(2*B-f1)))
		return irn

	def R3(pulse, B, f, f1):
		irn = []
		for num in pulse:
			irn.append(1.0)
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

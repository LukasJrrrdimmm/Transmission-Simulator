import math as mth
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def binary_generator(s, N):
		return np.random.randint(2, size = s*N)

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
	def gray_mapping(v, M):
		dec = ""
		bin_arr_x0 = []
		lim = np.log2(M)
		for i in range (0, int(lim)): 
			bin_arr_x0.append(np.array(v[int(i*(len(v)/lim)):(i+1)*(int(len(v)/lim))]))
		print(np.array(v))
		print(len(v))
		aux = np.transpose(np.array(bin_arr_x0))
		print(aux)
		a2 = []
		for b in aux:
			l1 = len(b)
			l2 = mth.ceil(len(b)/2)
			ax = b[0:l2]
			ay = b[l2:l1]
			aux2r = ""
			for i in ax:
				aux2r += str(i)
			aux2i = ""
			for i in ay:
				aux2i += str(i)
			a2.append(float(int(aux2r, 2)) + 1j*float(int(aux2i,2)))
		x = []
		y = []
		for n in a2:
			x.append(n.real)
			y.append(n.imag)
		print("|X0 Y0|")
		print(x)
		print(y)
		sns.set_style("whitegrid")
		plt.plot(x, y, "go")
		plt.show()

class Modulations:
	def NPAM(v, N):
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
	def MQAM(v, M):
		dec = ""
		bin_arr_x0 = []
		lim = np.log2(M)
		for i in range (0, int(lim)): 
			bin_arr_x0.append(np.array(v[int(i*(len(v)/lim)):(i+1)*(int(len(v)/lim))]))
		print(np.array(v))
		print(len(v))
		aux = np.transpose(np.array(bin_arr_x0))
		print(aux)
		a2 = []
		for b in aux:
			l1 = len(b)
			l2 = mth.ceil(len(b)/2)
			ax = b[0:l2]
			ay = b[l2:l1]
			aux2r = ""
			for i in ax:
				aux2r += str(i)
			aux2i = ""
			for i in ay:
				aux2i += str(i)
			a2.append(float(int(aux2r, 2)) + 1j*float(int(aux2i,2)))
		print(np.array(a2))
		x = []
		y = []
		s = []
		for a in a2:
			print(a)
			j = 0.00
			while j < 1.00:
				x.append(a.real*np.cos(2*np.pi + j*(2*np.pi)))
				j += 0.01
			j = 0.00
			while j < 1.00:
				y.append(a.imag*np.sin(2*np.pi + j*(2*np.pi)))
				s.append(a.real*np.cos(2*np.pi + j*(2*np.pi)) + 
					a.imag*np.sin(2*np.pi + j*(2*np.pi)))
				j += 0.01
		return x, y, s


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



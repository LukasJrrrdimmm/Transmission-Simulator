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
		l1 = 0
		c1 = 0
		c2 = 0
		for b in aux:
			l1 = len(b)
			l2 = mth.ceil(len(b)/2)
			a2.append(c1 + 1j*c2)
			c1 += 1
			if c1 == l1:
				c1 = 0
				c2 += 1
			if c2 == l1:
				c2 = 0
		n = np.array(a2)
		print("|X0 Y0|")
		print(n.real)
		print(n.imag)
		sns.set_style("whitegrid")
		plt.plot(n.real, n.imag, "go")
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
		s = []
		for a in a2:
			j = 0.00
			while j < 1.00:
				s.append(a.real*np.cos(2*np.pi + j*(4*np.pi)) + 
					a.imag*np.sin(2*np.pi + j*(4*np.pi))*1j)
				j += 0.01
		return np.array(s)


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
		
	def De_MQAM(signal):
		x = signal.real
		y = signal.imag
		for num in signal:
			x.append(num.real)
			y.append(num.img)
		xdm = []
		ydm = []
		for i in range(0, len(x)):
			xdm.append(x[i]/np.cos(2*np.pi + (i/100)*(4*np.pi)))
			ydm.append(y[i]/np.sin(2*np.pi + (i/100)*(4*np.pi)))
		xrs = []
		yrs = []
		c = 0
		r = []
		n = []
		for i in range(0, len(xdm)):
			if(len(r) != 0):
				flag = False
				for j in range(0, len(r)):
					if xdm[i] == r[j]:
						flag = True
						n[j] += 1
				if flag == False:
					r.append(xdm[i])
					n.append(1)
			else:
				r.append(xdm[i])
				n.append(1)
			c += 1
			hg = [0, 0]
			if c == 100:
				for j in range(0, len(n)):
					if hg[1] < n[j]:
						hg[0] = r[j]
						hg[1] = n[j]
				xrs.append(hg[0])
				r = []
				n = []
				c = 0
		if c != 0:
			for j in range(0, len(n)):
				if hg[1] < n[j]:
					hg[0] = r[j]
					hg[1] = n[j]
			xrs.append(hg[0])
			r = []
			n = []
			c = 0
		r = []
		n = []
		c = 0
		for i in range(0, len(ydm)):
			if(len(r) != 0):
				flag = False
				for j in range(0, len(r)):
					if ydm[i] == r[j]:
						flag = True
						n[j] += 1
				if flag == False:
					r.append(ydm[i])
					n.append(1)
			else:
				r.append(ydm[i])
				n.append(1)
			c += 1
			hg = [0, 0]
			if c == 100:
				for j in range(0, len(n)):
					if hg[1] < n[j]:
						hg[0] = r[j]
						hg[1] = n[j]
				yrs.append(hg[0])
				r = []
				n = []
				c = 0
		return xrs, yrs

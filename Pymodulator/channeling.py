import numpy as np
import pandas as pd
class Noising:
	def WhiteNoiseGenerator(sm, snr, Ps, s_len):
		Pr = 10**((snr/np.log10(Ps))**(-1))
		n = np.random.randint(6, size=s_len)
		csm = []
		for i in range(0, len(n)):
			csm.append(sm[i] + n[i]*Pr)
		print(pd.DataFrame({"S":sm, "N0":np.array(csm)}))
		return np.array(csm)
	def ThermicNoiseGenerator():
		#Ruído Térmico
		print("não implementado")
	def TunnelNoiseGenerator():
		#Ruído de Túnel
		print("não implementado")
class DeNoising:
	def Tunnel_Filter():
		print("não implementado")
		#remoção ou atenuação de ruído de túnel
	def Thermic_Filter():
		print("não implementado")
		#remoção ou atenuação de ruído térmico
	"""
	signal = sinal AWGN
	key = Período do Quadro
	SF = fator do sinal = abs(min(s)) == abs(max(s))
	Quanto maior o período mais fácil a filtragem
	"""
	def AWGN_Filter(signal, T, sf):
		if T < 8:
			print("é impossível filtrar, período (T) muito curto")
			return signal
		else:
			x = signal.real
			y = signal.imag
			dAe = abs(abs(min(x)) - abs(max(x)))
			reduxf = (dAe/sf)*(-1)
			xf = []
			for n in range(0, len(x), key):
				aux = x[n:n+key]
				xf.append((np.avr(aux) - dAe)/sf.real)
			yf = []
			for n in range(0, len(y), key):
				aux = y[n:n+key]
				yf.append((np.avr(aux) - dAe)/sf.imag)
			#remoção ou atenuação de ruído branco
			return np.array(xf) + np.array(yf)*1j

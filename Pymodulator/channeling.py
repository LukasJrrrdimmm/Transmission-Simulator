import numpy as np
import pandas as pd
class Noising:
	def WhiteNoiseGenerator(sm, snr, Ps, s_len):
		Pr = Ps/snr
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
	def AWGN_Filter():
		print("não implementado")
		#remoção ou atenuação de ruído branco

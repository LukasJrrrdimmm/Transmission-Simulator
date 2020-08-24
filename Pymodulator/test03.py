import passFilt as pf
import seaborn as sns
import pandas as pd
import numpy as np
import math as mth
import matplotlib.pyplot as plt
import filtering as filt
def MQAM_testing(sz, M, entrada):
	e = []
	if entrada == True:
		print("digite o sinal de entrada")
		for i in range(0, sz):
			print("valor da posição {}".format(i))
			e.append(int(input()))
		e = np.array(e)
	else:
		e = filt.binary_generator(sz, mth.ceil(M**(1/2)))
	s = filt.Modulations.MQAM(e, M)
	filt.GRAY.gray_mapping(e, M)
	sns.set_style("whitegrid")
	plt.plot(s.real, s.imag, "go")
	plt.title("MQAM Signal Constellation")
	plt.show()
	sns.set_style("whitegrid")
	pd.DataFrame({"Fase":s.real, "Quadratura":s.imag, "Sinal Completo":(s.real - s.imag)}).plot(subplots=True)
	plt.title("MQAM")
	plt.show()
	return s
def MQAM_Demod_testing(signal, M):
	x, y = filt.Demodulations.De_MQAM(signal)
	df = pd.DataFrame({"X":x, "Y":y})
	sns.set_style("whitegrid")
	df.plot(subplots=True)
	plt.show()
	e = get0signal(x, y, M)

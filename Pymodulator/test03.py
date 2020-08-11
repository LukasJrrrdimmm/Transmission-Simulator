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
	x, y, s = filt.AdjustFilters.MQAM(e, M)
	filt.GRAY.gray_mapping(e, M)
	sns.set_style("whitegrid")
	plt.plot(x, y, "go")
	plt.title("MQAM Signal Constellation")
	plt.show()
	sns.set_style("whitegrid")
	pd.DataFrame({"Fase":x, "Quadratura":y, "Sinal Completo":s}).plot(subplots=True)
	plt.title("MQAM")
	plt.show()
	return s

import passFilt as pf
import seaborn as sns
import pandas as pd
import numpy as np
import math as mth
import matplotlib.pyplot as plt
import filtering as filt
def MQAM_moddemod_testing(sz, M, entrada):# início da função
	e = []
	if entrada == True: # dúvida manualmente ou aleatória através da var entrada
		print("digite o sinal de entrada")
		for i in range(0, sz):
			print("valor da posição {}".format(i))
			e.append(int(input()))
		e = np.array(e)
	else:
		e = filt.binary_generator(sz, M)
	s, d = filt.Modulations.MQAM(e, 2**M) # modulação
	sns.set_style("whitegrid")
	plt.plot(s.real, s.imag, "r")
	plt.plot(s.real, s.imag, "ko")
	plt.title("MQAM Signal Eye Diagram Emissor")
	plt.show()
	sns.set_style("whitegrid")
	pd.DataFrame({"Fase":s.real, "Quadratura":s.imag, 
		"Sinal Completo":(s.real - s.imag)}).plot(subplots=True)
	plt.title("MQAM")
	plt.show()
	rec = filt.Demodulations.De_MQAM(s, d)
	sns.set_style("whitegrid")
	pd.DataFrame({"Original":e, "Reconstitution":rec}).plot(subplots=True)
	plt.title("Sinal Reconstituido")
	plt.show()
	return rrc
def MQAMENV_moddemod_testing(sz, M, entrada):# início da função
	e = []
	if entrada == True: # dúvida manualmente ou aleatória através da var entrada
		print("digite o sinal de entrada")
		for i in range(0, sz):
			print("valor da posição {}".format(i))
			e.append(int(input()))
		e = np.array(e)
	else:
		e = filt.binary_generator(sz, M)
	s, d = filt.Modulations.MQAMEntrelac_TV(e, 2**M) # modulação
	sns.set_style("whitegrid")
	plt.plot(s.real, s.imag, "r")
	plt.plot(s.real, s.imag, "ko")
	plt.title("MQAM Signal Eye Diagram Emissor")
	plt.show()
	sns.set_style("whitegrid")
	pd.DataFrame({"Fase":s.real, "Quadratura":s.imag, 
		"Sinal Completo":(s.real - s.imag)}).plot(subplots=True)
	plt.title("MQAM")
	plt.show()
	rec = filt.Demodulations.De_MQAMEntrelac_TV(s, d)
	sns.set_style("whitegrid")
	pd.DataFrame({"Original":e, "Reconstitution":rec}).plot(subplots=True)
	plt.title("Sinal Reconstituido")
	plt.show()
	return rrc
def MQPSK_moddemod_testing(sz, M, entrada):
	e = []
	if entrada == True:
		print("digite o sinal de entrada")
		for i in range(0, sz):
			print("valor da posição {}".format(i))
			e.append(int(input()))
		e = np.array(e)
	else:
		e = filt.binary_generator(sz, mth.ceil(M**(1/2)))
	s = filt.Modulations.MQPSK(e, M)
	filt.GRAY.gray_mapping(e, M)
	sns.set_style("whitegrid")
	plt.plot(s.real, s.imag, "r")
	plt.plot(s.real, s.imag, "ko")
	plt.title("MQPSK Signal Eye Diagram Emissor")
	plt.show()
	sns.set_style("whitegrid")
	pd.DataFrame({"Fase":s.real, "Quadratura":s.imag,
		"Sinal Completo":(s.real - s.imag)}).plot(subplots=True)
	plt.title("MQPSK Mod Signal")
	plt.show()
	b_x, b_y = filt.Demodulations.De_MQAM(s, M)
	r = []
	for i in range(0, len(bin_x)):
		r.append(b_x[i] + b_y[i])
	print(r)
	rec = filt.QuadratureDecoder(r, log2(M))
	sns.set_style("whitegrid")
	pd.DataFrame({"Original":e, "Reconstitution":rec}).plot(subplots=True)
	plt.title("Sinal Reconstituido")
	plt.show()
	return r

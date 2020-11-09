import passFilt as pf
import seaborn as sns
import pandas as pd
import numpy as np
import math as mth
import matplotlib.pyplot as plt
import filtering as filt

def test_mqam(sd, rg): # MQAM Tradicional
	e = filt.binary_generator(sd, rg)
	s, d = filt.Modulations.MQAM(e, 2**rg) # modulação
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
	rec = np.array(rec)
	print("diff = {}".format(len([(e[i] - rec[i]) for i in range(0, len(e)) if(e[i] != rec[i])])))
	plt.show()
def test_mqamEntrelac_A(sd, rg): #MQAM Entrelqaçado Tipo A
	e = filt.binary_generator(sd, rg)
	s, d = filt.Modulations.MQAM_Entrelac_TH(e, 2**rg) # modulação
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
	rec = filt.Demodulations.De_MQAM_Entrelac_TH(s, d)
	sns.set_style("whitegrid")
	pd.DataFrame({"Original":e, "Reconstitution":rec}).plot(subplots=True)
	plt.title("Sinal Reconstituido")
	plt.show()
def test_mqamEntrelac_B(sd, rg): #MQAM Entrelaçado Tipo B
	e = filt.binary_generator(sd, rg)
	s, d = filt.Modulations.MQAM_Entrelac_TV(e, 2**rg) # modulação
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
def test_mqpsk(sd, rg): # MQPSK
	e = filt.binary_generator(sd, rg)
	s, d = filt.Modulations.MQPSK(e, rg)
	#filt.GRAY.gray_mapping(e, rg)
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
	rec = filt.Demodulations.De_MQPSK(s, rg, d)
	sns.set_style("whitegrid")
	pd.DataFrame({"Original":e, "Reconstitution":rec}).plot(subplots=True)
	plt.title("Sinal Reconstituido")
	plt.show()

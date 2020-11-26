import passFilt as pf
import seaborn as sns
import pandas as pd
import numpy as np
import math as mth
import matplotlib.pyplot as plt
from channeling import Noising as Chan_N
import filtering_hibrid as filt

def test_mqam(sd, rg): # MQAM Tradicional
	e = filt.binary_generator(sd, rg)
	s, key, M, f1, f2 = filt.Modulations.MQAM(e, 2**rg) # modulação
	Pf = f1[0]/2
	Pq = f2[0]/2
	f = Pf + Pq/2
	print("Ps = {}".format(f))
	if(f < 0):
		f = abs(f)
	g = np.size(s)
	cs = Chan_N.WhiteNoiseGenerator(s, 2.8, f, g)
	'''sns.set_style("whitegrid")
	plt.plot(s.real, s.imag, "r")
	plt.plot(s.real, s.imag, "ko")
	plt.title("MQAM Signal Eye Diagram Emissor")
	plt.show()'''
	sns.set_style("whitegrid")
	pd.DataFrame({"Fase":s.real, "Quadratura":s.imag, 
		"Sinal Completo":(s.real - s.imag)}).plot(subplots=True)
	plt.title("MQAM")
	plt.show()
	sns.set_style("whitegrid")
	pd.DataFrame({"Fase":cs.real, "Quadratura":cs.imag, 
		"Sinal Completo (Com Ruido Branco)":(cs.real - cs.imag)}).plot(subplots=True)
	plt.title("MQAM")
	plt.show()
	rec = filt.Demodulations.De_MQAM(s, key, M)
	rec = np.array(rec)
	print("diff = {}".format(len([(e[i] - rec[i]) for i in range(0, len(e)) if(e[i] != rec[i])])))
	plt.show()
def test_mqamEntrelac_A(sd, rg): #MQAM Entrelqaçado Tipo A
	e = filt.binary_generator(sd, rg)
	s, key, M, f1, f2 = filt.Modulations.MQAM_Entrelac_TH(e, 2**rg) # modulação
	Pf = f1[0]/2
	Pq = f2[0]/2
	f = Pf + Pq/2
	print("Ps = {}".format(f))
	if(f < 0):
		f = abs(f)
	g = np.size(s)
	cs = Chan_N.WhiteNoiseGenerator(s, 3.6, f, g)
	'''sns.set_style("whitegrid")
	plt.plot(s.real, s.imag, "r")
	plt.plot(s.real, s.imag, "ko")
	plt.title("MQAM Signal Eye Diagram Emissor")
	plt.show()'''
	sns.set_style("whitegrid")
	pd.DataFrame({"Fase":s.real, "Quadratura":s.imag, 
		"Sinal Completo (Sem Ruido)":(s.real - s.imag)}).plot(subplots=True)
	plt.title("MQAM")
	plt.show()
	sns.set_style("whitegrid")
	pd.DataFrame({"Fase":cs.real, "Quadratura":s.imag, 
		"Sinal Completo (Com Ruido Branco)":(cs.real - cs.imag)}).plot(subplots=True)
	plt.title("MQAM")
	plt.show()
	rec = filt.Demodulations.De_MQAM_Entrelac_TH(s, d)
	sns.set_style("whitegrid")
	pd.DataFrame({"Original":e, "Reconstitution":rec}).plot(subplots=True)
	plt.title("Sinal Reconstituido")
	plt.show()
def test_mqamEntrelac_B(sd, rg, T): #MQAM Entrelaçado Tipo B
	e = filt.binary_generator(sd, rg)
	s, key, M, f1, f2 = filt.Modulations.MQAM_Entrelac_TV(e, 2**rg, T) # modulação
	'''sns.set_style("whitegrid")
	plt.plot(s.real, s.imag, "r")
	plt.plot(s.real, s.imag, "ko")
	plt.title("MQAM Signal Eye Diagram Emissor")
	plt.show()'''
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
def test_mqpsk(sd, rg, T): # MQPSK
	e = filt.binary_generator(sd, rg)
	s, key, M, f1, f2 = filt.Modulations.MQPSK(e, 2**rg, T)
	Pf = f1[0]/2
	Pq = f2[0]/2
	f = Pf + Pq/2
	print("Ps = {}".format(f))
	if(f < 0):
		f = abs(f)
	g = np.size(s)
	cs = Chan_N.WhiteNoiseGenerator(s, 3.6, f, g)
	"""sns.set_style("whitegrid")
	plt.plot(s.real, s.imag, "r")
	plt.plot(s.real, s.imag, "ko")
	plt.title("MQPSK Signal Eye Diagram Emissor")
	plt.show()"""
	sns.set_style("whitegrid")
	pd.DataFrame({"Fase":s.real, "Quadratura":s.imag,
		"Sinal Completo":(s.real - s.imag)}).plot(subplots=True)
	plt.title("MQPSK Mod Signal")
	plt.show()
	sns.set_style("whitegrid")
	pd.DataFrame({"Fase":cs.real, "Quadratura":s.imag, 
		"Sinal Completo (Com Ruido Branco)":(cs.real - cs.imag)}).plot(subplots=True)
	plt.title("MQPSK AWGN")
	plt.show()
	rec = filt.Demodulations.De_MQPSK(s, M, key, T)
	sns.set_style("whitegrid")
	pd.DataFrame({"Original":e, "Reconstitution":rec}).plot(subplots=True)
	plt.title("Sinal Reconstituido")
	plt.show()

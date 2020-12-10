import passFilt as pf
import seaborn as sns
import pandas as pd
import numpy as np
import math as mth
import matplotlib.pyplot as plt
from channeling import Noising as Chan_N
import filtering_hibrid as filt

def test_mqam(sd, rg, M, T, SNR): # MQAM Tradicional
	e = filt.binary_generator(sd, rg)
	s, q, i = np.array(filt.Modulations.MQAM(e, M, T)) # modulação
	sf = s.real + s.imag
	'''plt.plot(s.real, s.imag, "r")
	plt.plot(s.real, s.imag, "ko")
	plt.title("MQAM Signal Eye Diagram Emissor")
	plt.show()'''
	sns.set_style("whitegrid")
	pd.DataFrame({"Fase":q, "Quadratura":i}).plot(subplots=True)
	plt.title("MQAM")
	plt.show()
	sns.set_style("whitegrid")
	pd.DataFrame({"Sinal Completo":sf}).plot()
	plt.title("MQAM")
	plt.show()
	cs = Chan_N.WhiteNoiseGenerator(sf, SNR, T)
	sns.set_style("whitegrid")
	pd.DataFrame({"Sinal Completo (Com Ruido Branco)":cs}).plot()
	plt.title("MQAM")
	plt.show()
	rec = filt.Demodulations.De_MQAM((q + i*1j), M, T)
	rec = np.array(rec)
	print("diff = {}".format(len([abs(e[i] - rec[i]) for i in range(0, len(e)) if(e[i] != rec[i])])))
def test_mqamEntrelac_A(sd, rg, M, T, SNR): #MQAM Entrelqaçado Tipo A
	e = filt.binary_generator(sd, rg)
	s, key, tau = filt.Modulations.MQAM_Entrelac_TH(e, 2**rg, M, T) # modulação
	'''sns.set_style("whitegrid")
	plt.plot(s.real, s.imag, "r")
	plt.plot(s.real, s.imag, "ko")
	plt.title("MQAM Signal Eye Diagram Emissor")
	plt.show()'''
	sns.set_style("whitegrid")
	pd.DataFrame({"Fase":s.real, "Quadratura":s.imag}).plot()
	plt.title("MQAM")
	plt.show()
	sns.set_style("whitegrid")
	pd.DataFrame({"Sinal Completo (Sem Ruido)":(s.real - s.imag)}).plot()
	plt.title("MQAM")
	plt.show()
	cs = Chan_N.WhiteNoiseGenerator(s, SNR, T) + Chan_N.WhiteNoiseGenerator(cs.real, SNR, T)*1j
	sns.set_style("whitegrid")
	pd.DataFrame("Sinal Completo (Com Ruido Branco)":(cs.real - cs.imag)}).plot()
	plt.title("MQAM")
	plt.show()
	rec = filt.Demodulations.De_MQAM_Entrelac_TH(s, key, M, T)
	print("diff = {}".format(len([abs(e[i] - rec[i]) for i in range(0, len(e)) if(e[i] != rec[i])])))
def test_mqamEntrelac_B(sd, rg, M, T, SNR): #MQAM Entrelaçado Tipo B
	e = filt.binary_generator(sd, rg)
	s, key, tau = filt.Modulations.MQAM_Entrelac_TV(e, 2**rg, M, T) # modulação
	'''sns.set_style("whitegrid")
	plt.plot(s.real, s.imag, "r")
	plt.plot(s.real, s.imag, "ko")
	plt.title("MQAM Signal Eye Diagram Emissor")
	plt.show()'''
	sns.set_style("whitegrid")
	pd.DataFrame({"Sinal Completo":(s.real - s.imag)}).plot()
	plt.title("MQAM")
	plt.show()
	cs = Chan_N.WhiteNoiseGenerator(s, SNR, T)
	sns.set_style("whitegrid")
	pd.DataFrame({"Sinal Completo (Com Ruido Branco)":(cs.real - cs.imag)}).plot()
	plt.title("MQAM")
	plt.show()
	rec = filt.Demodulations.De_MQAM_Entrelac_TV(s, key, M, T)
	print("diff = {}".format(len([abs(e[i] - rec[i]) for i in range(0, len(e)) if(e[i] != rec[i])])))
def test_mqpsk(sd, rg, M, T, SNR): # MQPSK
	e = filt.binary_generator(sd, rg)
	s, tau = filt.Modulations.MQPSK(e, 2**rg, M, T)
	sns.set_style("whitegrid")
	pd.DataFrame({"Fase":s.real, "Quadratura":s.imag}).plot(subplots=True)
	plt.title("MPSK")
	plt.show()
	cs = Chan_N.WhiteNoiseGenerator(cs.real, SNR, T) + Chan_N.WhiteNoiseGenerator(cs.imag, SNR, T)*1j
	sns.set_style("whitegrid")
	pd.DataFrame({"Fase":cs.real, "Quadratura":cs.imag}).plot()
	plt.title("MPSK AWGN (Com Ruido Branco)")
	plt.show()
	rec = filt.Demodulations.De_MQPSK(s, M, T)
	print("diff = {}".format(len([abs(e[i] - rec[i]) for i in range(0, len(e)) if(e[i] != rec[i])])))

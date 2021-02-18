#import passFilt as pf
import seaborn as sns
import pandas as pd
import numpy as np
import math as mth
import matplotlib.pyplot as plt
from channeling import Noising as Chan_N
import filtering_hibrid as filt

def test_mqam(sd, rg, M, T, SNR): # MQAM Tradicional
	e = filt.binary_generator(sd, rg)
	print(e)
	s, q, i = np.array(filt.Modulations.MQAM(e, M, T)) # modulação	sns.set_style("whitegrid")
	pd.DataFrame({"Fase":q, "Quadratura":i}).plot(subplots=True)
	sns.set_style("whitegrid")
	pd.DataFrame({"Sinal MQAM": s}).plot()
	plt.title("Sinal MQAM Sem Ruído")
	plt.show()
	cs = Chan_N.WhiteNoiseGenerator(s, SNR, T)
	sns.set_style("whitegrid")
	pd.DataFrame({"Sinal MQAM (Com Ruido Branco)":cs}).plot()
	plt.title("Sinal MQAM Com Ruído")
	plt.show()
	rec2 = filt.Demodulations.De_MQAM(s, M, T)
	rec2 = np.array(rec2)
	print(e)
	print("diff = {}".format(len([abs(e[i] - rec2[i]) for i in range(0, len(e)) if(e[i] != rec2[i])])))
def test_mqamEntrelac_A(sd, rg, M, T, SNR): #MQAM Entrelqaçado Tipo A
	e = filt.binary_generator(sd, rg)
	s, key, tau = filt.Modulations.MQAM_Entrelac_TH(e, 2**rg, M, T) # modulação
	sns.set_style("whitegrid")
	pd.DataFrame({"Sinal MQAM Entrelaçado (Sem Ruido)":s}).plot()
	plt.title("MQAM")
	plt.show()
	cs = Chan_N.WhiteNoiseGenerator(s, SNR, T)
	sns.set_style("whitegrid")
	pd.DataFrame({"Sinal MQAM Entrelaçado (Com Ruido Branco)":(cs.real - cs.imag)}).plot()
	plt.title("MQAM")
	plt.show()
	rec = filt.Demodulations.De_MQAM_Entrelac_TH(s, key, M, T)
	print("diff = {}".format(len([abs(e[i] - rec[i]) for i in range(0, len(e)) if(e[i] != rec[i])])))
def test_mqamEntrelac_B(sd, rg, M, T, SNR): #MQAM Entrelaçado Tipo B
	e = filt.binary_generator(sd, rg)
	s, key, tau = filt.Modulations.MQAM_Entrelac_TV(e, 2**rg, M, T) # modulação
	sns.set_style("whitegrid")
	pd.DataFrame({"Sinal MQAM Entrelaçado":s}).plot()
	plt.title("MQAM")
	plt.show()
	cs = Chan_N.WhiteNoiseGenerator(s, SNR, T)
	sns.set_style("whitegrid")
	pd.DataFrame({"Sinal MQAM Entrelaçado (Com Ruido Branco)":(cs.real - cs.imag)}).plot()
	plt.title("MQAM")
	plt.show()
	rec = filt.Demodulations.De_MQAM_Entrelac_TV(s, key, M, T)
	print("diff = {}".format(len([abs(e[i] - rec[i]) for i in range(0, len(e)) if(e[i] != rec[i])])))
def test_mpsk(sd, rg, M, T, SNR): # MPSK
	e = filt.binary_generator(sd, rg)
	s, i, q = filt.Modulations.MPSK(e, M, T)
	sns.set_style("whitegrid")
	pd.DataFrame({"Sinal MPSK":s}).plot(subplots=True)
	plt.title("MPSK")
	plt.show()
	cs = Chan_N.WhiteNoiseGenerator(s, SNR, T)
	sns.set_style("whitegrid")
	pd.DataFrame({"Sinal MPSK (Com Ruido Branco)":cs}).plot(subplots = True)
	plt.title("MPSK AWGN")
	plt.show()
	rec = filt.Demodulations.De_MPSK(s, M, T)
	print("diff = {}".format(len([abs(e[i] - rec[i]) for i in range(0, len(e)) if(e[i] != rec[i])])))

def test_mppm(sd, rg, M, T, SNR): # MPPM Prototype (nexts steps)
	e = filt.binary_generator(sd, rg)
	s, i, q = filt.Modulations.MPPM(e, M, T)
	sns.set_style("whitegrid")
	pd.DataFrame({"Sinal Completo":s}).plot(subplots=True)
	plt.title("MPPM")
	plt.show()
	cs = Chan_N.WhiteNoiseGenerator(s, SNR, T)
	sns.set_style("whitegrid")
	pd.DataFrame({"Fase":cs}).plot(subplots = True)
	plt.title("MPPM AWGN (Com Ruido Branco)")
	plt.show()
	#rec = filt.Demodulations.De_MPPM(s, M, T)
	#print("diff = {}".format(len([abs(e[i] - rec[i]) for i in range(0, len(e)) if(e[i] != rec[i])])))

#import passFilt as pf
import seaborn as sns
import pandas as pd
import numpy as np
import math as mth
import matplotlib.pyplot as plt
from channeling import Noising as Chan_N
import filtering_hibrid as filt

def generateBinMSG(msg_range, seed=2):
	msg = filt.binary_generator(seed, msg_range)
	return msg

def printFQ(q, i):
	pd.DataFrame({"Fase": q, "Quadratura": i}).plot(subplots=True)
	plt.show()

def ModemStart(msg, modtype, T, M=16 ,SNR = -5, fq=False, itermG=False, demode=True, add_noise=True):  # MQAM Tradicional
	flag = True
	if modtype.upper() == 'MQAM':
		s, f, q = np.array(filt.Modulations.MQAM(msg, M, T, itermG))  # modulação	sns.set_style("whitegrid")
	elif modtype.upper() == 'MPSK':
		s, f, q = np.array(filt.Modulations.MPSK(msg, M, T, itermG))  # modulação	sns.set_style("whitegrid")
	elif modtype.upper() == 'MPPM':
		print("Modulação ainda não implementada")
		flag = False
	else:
		print("Modulação Inválida")
		flag = False
	if flag:
		print("Sinal Modulado")
		if fq:
			"Grafico Real/Imag Habilitado"
			printFQ(f, q)
		sns.set_style("whitegrid")
		pd.DataFrame({"Sinal MQAM": s}).plot()
		plt.title("Sinal MQAM Sem Ruído")
		plt.show()
		if add_noise:
			print("Canal AWGN Habilitado")
			cs = Chan_N.WhiteNoiseGenerator(s, SNR, T)
			sns.set_style("whitegrid")
			pd.DataFrame({"Sinal MQAM (Com Ruido Branco)": cs}).plot()
			plt.title("Sinal MQAM Com Ruído")
			plt.show()
		if demode:
			print("Demodulação Habilitada")
			if modtype.upper()  == 'MQAM':
				rec2 = np.array(filt.Demodulations.De_MQAM(s, M, T, itermG))  # modulação	sns.set_style("whitegrid")
			elif modtype.upper()  == 'MPSK':
				rec2 = np.array(filt.Demodulations.De_MPSK(s, M, T, itermG))  # modulação	sns.set_style("whitegrid")
			print(msg)
			print("diff = {}".format(len([abs(msg[i] - rec2[i]) for i in range(0, len(msg)) if (msg[i] != rec2[i])])))

def EntrelacModemStart(msg, T, Entrelac,  M=16, SNR=-5, fq=False, itermG=False, demode=True, add_noise=True): #MQAM Entrelqaçado Tipo A
	flag = True
	if Entrelac.upper() == 'A':
		s, key, tau, f, q = filt.Modulations.MQAM_Entrelac_TH(msg, len(msg), M, T, itermG) # modulação
		sns.set_style("whitegrid")
		pd.DataFrame({"Sinal MQAM Entrelaçado (Sem Ruido)":s}).plot()
		plt.title("MQAM")
		plt.show()
	elif Entrelac.upper() == 'B':
		s, key, tau, f, q = filt.Modulations.MQAM_Entrelac_TV(msg, len(msg), M, T)  # modulação
		sns.set_style("whitegrid")
		pd.DataFrame({"Sinal MQAM Entrelaçado (Sem Ruido)": s}).plot()
		plt.title("MQAM")
		plt.show()
	else:
		print("Tipo de Entrelaçamento Inválido")
		flag=False
	if flag:
		if fq:
			printFQ(f, q)
		if add_noise:
			cs = Chan_N.WhiteNoiseGenerator(s, SNR, T, itermG)
			sns.set_style("whitegrid")
			pd.DataFrame({"Sinal MQAM Entrelaçado (Com Ruido Branco)":(cs.real - cs.imag)}).plot()
			plt.title("MQAM")
			plt.show()
		if demode:
			if Entrelac.upper() == 'A':
				rec = filt.Demodulations.De_MQAM_Entrelac_TH(s, key, M, T, itermG)
			if Entrelac.upper() == 'B':
				rec = filt.Demodulations.De_MQAM_Entrelac_TV(s, key, M, T, itermG)
			print("diff = {}".format(len([abs(msg[i] - rec[i]) for i in range(0, len(msg)) if(msg[i] != rec[i])])))


def test_mppm(m_range, T, M=16, seed = 2, SNR = -5, itermG=False): # MPPM Prototype (nexts steps)
	e = filt.binary_generator(seed, m_range)
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

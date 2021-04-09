import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from channeling import Noising as Chan_N
import filtering_hibrid as filt
'''
Autor/Author: Lukas Maximo Grilo Abreu Jardim, Orientador/Manager: Me. Yuri Pedro dos Santos, Prof. Luiz Felipe de Queiroz Silveira
Poweredby: UFRN - Departamento de Computação e Automação, Commpy and his developers, DCA - Departamento de Conputação e Automação - Centro de Tecnologia da UFRN
PT: Esse código, por enquanto, aceita apenas mensagens binárias
****************
EN: These code only accept binary messages for a while 
'''


def generateBinMSG( msg_range, seed=2):
	# msg_range - the range of the sender message - o tamanho da mensagem a ser enviada pelo emissor
	msg = filt.binary_generator(seed, msg_range)
	print(msg)
	print("Mensagem Gerada")
	return msg
'''
generateBinMsg
EN: these function generate a binary message with range 2^msg_range
PT: essa função gera uma mensagem de tamanho 2^msg_range
'''


def printFQ(q, i):
	pd.DataFrame({"Fase": q, "Quadratura": i}).plot(subplots=True)
	plt.show()


def ModemStart(msg, modtype, T, M=16 ,SNR = -5, pq=False, itermG=False, demode=True,
			   add_noise=True, finalG=False):
	if(len(msg)%np.log2(M) != 0):
		#profilaxy - profilaxia
		g = int(np.log2(M)) - int(len(msg)%np.log2(M))
		for i in range(0, g):
			msg = np.array([0] + list(msg))
	'''
	ModemStart()
	:param msg: message - mensagem a ser enviada
	:param modtype: modulation type - o tipo da modulação a ser executada
	:param T: period - o período da onda portadora
	:param M: modulation number - o número da modulação
	:param SNR: signal-noise ratio - a relação sinal-ruído
	:param pq: phase-quadrature signal specte graphic (optinal) - o gráfico do sinal dividido em suas contrapartes em fase e em quadratura
	:param itermG: M-ary constellation mapped message graphics (optional) - o gráfico da mensagem com o mapeamento M-ário em fase e quadratura
	:param demode: demodulation switch (enabled as standard) - switch de demodulação (habilitado por padrão)
	:param add_noise: AWGN channel sinulation switch (enabled as standard) - switch de simulação do canal AWGN (habilitado por padrão)
	:param finalG: regenerated message comparative graphic (optional) - o gráfico comparativo da mensagem regenerada após a demodulação (opcional)
	'''
	global f, q, s, rec2
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
		print("Sinal Modulado Disponível")
		if pq:
			"Grafico Real/Imag Habilitado"
			printFQ(f, q)
		sns.set_style("whitegrid")
		pd.DataFrame({f"Sinal {modtype.upper()}": s}).plot()
		plt.title("Sinal {} Sem Ruído".format(modtype.upper()))
		plt.show()
		if add_noise:
			print("Canal AWGN Habilitado")
			cs = Chan_N.WhiteNoiseGenerator(s, SNR, T)
			sns.set_style("whitegrid")
			pd.DataFrame({f"Sinal {modtype.upper()} (Com Ruido Branco)": cs}).plot()
			plt.title("Sinal {} Com Ruído SNR = {}".format(modtype.upper(), SNR))
			plt.show()
		if demode:
			print("Demodulação Habilitada")
			if modtype.upper() == 'MQAM':
				rec2 = np.array(filt.Demodulations.De_MQAM(s, M, T, itermG))  # modulação	sns.set_style("whitegrid")
			elif modtype.upper() == 'MPSK':
				rec2 = np.array(filt.Demodulations.De_MPSK(s, M, T, itermG))  # modulação	sns.set_style("whitegrid")
			print(msg)
			print("diff = {}".format(len([abs(msg[i] - rec2[i]) for i in range(0, len(msg)) if (msg[i] != rec2[i])])))
			if finalG:
				sns.set_style("whitegrid")
				pd.DataFrame({"Original": msg, "Reconstituído": rec}).plot()
				plt.title("Comparação da Mensagem Reconstituída")
				plt.show()


def EntrelacModemStart(msg, T, Entrelac,  M=16, SNR=-5, pq=False, itermG=False,
					   demode=True, add_noise=True, finalG=False): #MQAM Entrelqaçado Tipo A
	global f, q, s, key, rec
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
		if pq:
			printFQ(f, q)
		if add_noise:
			cs = Chan_N.WhiteNoiseGenerator(s, SNR, T)
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
			if finalG:
				sns.set_style("whitegrid")
				pd.DataFrame({"Original": msg, "Reconstituído": rec}).plot()
				plt.title("Comparação da Mensagem Reconstituída")
				plt.show()


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

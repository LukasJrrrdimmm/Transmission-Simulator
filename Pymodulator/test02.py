import passFilt as pf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def MQAM_Gen(S, N):
	a = pf.gray_scheme.binary_gnerator(S, N)
	b = pf.binary_conversor.arrayNPAM(a, N)
	c = pf.gray_scheme.gray_generator(N)
	print(a)
	print(b)
	print(pd.DataFrame(c))
	d = pf.gray_scheme.encode_gray(b,c)
	print(d)
	
	prt = []
	for i in range(0, len(d)):
		prt.append(d[i])
		for j in range(0, 100):
			prt.append(0)
	plt.plot(prt, 'r')
	plt.grid()
	plt.show()
	return d
def MQAM_Tester(l, N, M):
	x1 = pf.binary_conversor.Re_arrayMQAM(pf.gray_scheme.binary_gnerator(l, N), M)
	y1 = pf.binary_conversor.Im_arrayMQAM(pf.gray_scheme.binary_gnerator(l, N), M)
	print("X1{} Y1{}".format(len(x1), len(y1)))
	sg = []
	for i in range(0, len(x1)):
		sg.append(x1[i] + y1[i])
	import seaborn as sns
	sns.set_style('whitegrid')
	pd.DataFrame({"Fase":x1, "Quadratura":y1, "Sinal Completo":sg}).plot(subplots=True)
	plt.show()

def MQAM_Rcos_Gen(S, N, B, F1):
	a = pf.gray_scheme.binary_gnerator(S, N)
	b = pf.binary_conversor.arrayNPAM(a, N)
	c = pf.gray_scheme.gray_generator(N)
	print(a)
	print(b)
	print(pd.DataFrame(c))
	d = pf.gray_scheme.encode_gray(b,c)
	print("signal = {}".format(d))
	f = int(input())
	en = pf.RCossin.Process(d, B, f, F1)
	print("F_signal = {}".format(en))
	prt = []
	for i in range(0, len(en)):
		prt.append(en[i])
		for j in range(0, 100):
			prt.append(0)
	plt.plot(prt, 'r')
	plt.grid()
	plt.show()
	return d

def GRAY_Mapping(S, N):
	a = pf.gray_scheme.binary_gnerator(S, N)
	b = pf.binary_conversor.arrayNPAM(a, N)
	c = pf.gray_scheme.gray_generator_map(N)
	print(a)
	print(b)
	print(pd.DataFrame(c))
	x, y = pf.gray_scheme.gray_mapping(b, c)
	print(pd.DataFrame({"X": x, "Y": y}))

	plt.scatter(x, y, marker='.', c='k')
	plt.grid()
	plt.show()
	return x, y

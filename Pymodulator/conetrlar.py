import numpy as np

def best_constelaris(l):
	for i in range(0, 100):
		if(l%2**i != 0):
			c_num = 2**(i-1)
			print("Constelar num = {}".format(c_num))
			return c_num
			break
	

def constelaris_factory(digi_signal, const_num):
	print(const_num)
	constelaris = []
	for i in range(0, len(digi_signal), const_num):
		k = 0
		k1 = const_num - 1
		for j in range(i, i + const_num):
			k += digi_signal[j]*2**k1
			k1 -= 1
		constelaris.append(k)
	print(np.array(constelaris))
	return constelaris

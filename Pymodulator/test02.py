import passFilt as pf
import pandas as pd
a = pf.gray_scheme.binary_gnerator(32, 4)
b = pf.binary_conversor.arrayNPAM(a, 4)
c = pf.gray_scheme.gray_generator(4)
print(a)
print(b)
print(pd.DataFrame(c))
d = pf.gray_scheme.encode_gray(b,c)
print(d)
import numpy as np
import matplotlib.pyplot as plt
prt = []
for i in range(0, len(d)):
	prt.append(d[i])
	for j in range(0, 100):
		prt.append(0)
plt.plot(prt, 'r')
plt.grid()
plt.show()

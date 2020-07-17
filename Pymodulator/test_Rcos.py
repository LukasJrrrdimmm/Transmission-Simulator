import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from passFilt import RCossin as rcs

def PAM_Adjust(v):
	n1 = []
	for num in v:
		n1 = []
		for num in v:
			if num == 0:
				n1.append(-4)
			elif num == 1:
				n1.append(-2)
			elif num == 2:
				n1.append(2)
			elif num == 3:
				n1.append(4)
		return np.array(n1) # PAM personalizada

v1 = np.random.randint(4, size = 16)
v2 = np.random.randint(4, size = 16)
v1 = PAM_Adjust(v1)
v2 = PAM_Adjust(v2)
print("{} | {}".format(v1, v2))
a1 = []
a2 = []


for i in range(0, len(v1)):
	a1.append(v1[i])
	a2.append(v2[i])
	for j in range(0, 100):
		a1.append(0)
		a2.append(0)
fp = 500
s1 = rcs.Process(np.array(a1), 500, 450, fp)
s2 = rcs.Process(np.array(a1), 500, 550, fp)

df1 = pd.DataFrame({"v1": v1, "v2": v2})
df = pd.DataFrame({"a1": a1, "a2": a2})
print(s1)
print(s2)
df2 = pd.DataFrame({"s1":s1, "s2":s2})
sns.set_style('whitegrid')
df1.plot(subplots=True, title = 'Vetor de Pulsos')
plt.show()
sns.set_style('whitegrid')
df.plot(subplots=True, title = 'Trem de Pulsos')
plt.show()
sns.set_style('whitegrid')
df2.plot(subplots=True, title = 'Cosseno Elevado de Trem de Pulsos (Tempo e Quadratura)')
plt.show()

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


v1 = np.random.randint(10, size = 16)
v2 = np.random.randint(10, size = 16)
# Informações a serem transmitidas


M = 4
a1 = []
a2 = []
t = []
for i in range(0, len(v1)):
	a1.append(v1[i])
	a2.append(v2[i])
	for j in range(0, 100):
		a1.append(0)
		a2.append(0)
fp = 500
s1 = []
s2 = []
for i in range(0, len(a1)):
	s1.append(a1[i]*np.cos((np.pi/8)*fp*((i+1)/100)))
	s2.append(a2[i]*np.sin((np.pi/8)*fp*((i+1)/100)))

df1 = pd.DataFrame({"v1": v1, "v2": v2})
df = pd.DataFrame({"a1": a1, "a2": a2})
df2 = pd.DataFrame({"s1":s1, "s2":s2})
sns.set_style('whitegrid')
df1.plot(subplots=True, title = 'Vetor de Pulsos')
plt.show()
sns.set_style('whitegrid')
df.plot(subplots=True, title = 'Trem de Pulsos')
plt.show()
sns.set_style('whitegrid')
df2.plot(subplots=True, title = 'Convolução de Trem de Pulsos (Fase e Quadratura)')
plt.show()
s3 = []
for i in range(0, len(s1)):
	s3.append(s1[i] + s2[i])
sns.set_style('whitegrid')
df3 = pd.DataFrame({"s3": s3})
df3.plot(title = "Sinal Completo")
plt.show()

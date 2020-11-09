import numpy as np
import pandas as pd

print("Seed:")
sd = int(input())
print("Range:")
rg = int(input())

v1 = np.random.randint(rg, size=2**sd)
s = []
for i in range(0, len(v1), 4):
	s.append(v1[i:i+4])
print(np.array(s))
m1 = np.array(s)
print("=============")
print(np.transpose(np.array(s)))
m2 = np.transpose(np.array(s))
l = [0, 0]
s1 = []
hx1 = []
for a in m1:
	nm1 = ""
	l[0] = len(a)
	for num in a:
		nm1 += str(num)
	s1.append(int(nm1, 2))
	hx1.append(hex(int(nm1, 2)))
print(s1)
print(hx1)
s2 = []
hx2 = []
for a in m2:
	nm2 = ""
	for num in a:
		nm2 += str(num)
	s2.append(int(nm2, 2))
	hx2.append(hex(int(nm2, 2)))
print(s2)
print(hx2)
	

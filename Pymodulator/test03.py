import passFilt as pf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
a = pf.gray_scheme.binary_gnerator(32, 4)
b = pf.binary_conversor.arrayNPAM(a, 4)
c = pf.gray_scheme.gray_generator_map(4)
print(a)
print(b)
print(pd.DataFrame(c))
x, y = pf.gray_scheme.gray_mapping(b, c)
print(pd.DataFrame({"X": x, "Y": y}))

plt.scatter(x, y, marker='.', c='k')
plt.grid()
plt.show()

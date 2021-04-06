import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from channeling import Noising as Chan_N
import filtering_hibrid as filt

class Pymodulator:
    def __init__(self):
        self.MQAM = "MQAM"
        self.MPAK = "MPSK"
        self.AWGN = False

    def generate_msg(self, seed=2, msg_size):
        return filt.binary_generator(seed, msg_size)

    def beginTransmission(self, msg, modtype, M, T, demodulation=True, noising=True, SNR=-10):
        t = type(msg)
        if modtype = 'MQAM':
        elif modtype = 'MPSK':
        else:



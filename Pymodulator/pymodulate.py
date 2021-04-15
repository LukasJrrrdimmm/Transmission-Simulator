import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from channeling import Noising as Chan_N
import filtering_hibrid as filt

class Pymodulator:
    def __init__(self):
        self.modtype = "MQAM"
        self.T = 16
        self.itermG = False
        self.msg = []

    def generate_msg(self, msgSQsize, seed=2):
        return filt.binary_generator(seed, msgSQsize)

    def printFQ(self, q, i):
        pd.DataFrame({"Fase": q, "Quadratura": i}).plot(subplots=True)
        plt.show()

    def MSGRegularizer(self, msg, M):
        if (len(msg) % np.log2(M) != 0):
            # profilaxy - profilaxia
            g = int(np.log2(M)) - int(len(msg) % np.log2(M))
            for i in range(0, g):
                msg = np.array([0] + list(msg))
        return msg

    def Modulate(self, msg, modtype, M, T, fq=False, itermG=False):
        t = type(msg)
        self.T = T
        self.modtype = modtype
        self.itermG = itermG
        flag = True
        if modtype.upper() == 'MQAM':
            msg = self.MSGRegularizer(self, msg, M)
            self.msg = msg
            s, f, q = np.array(filt.Modulations.MQAM(msg, M, T, itermG))  # modulação	sns.set_style("whitegrid")
        elif modtype.upper() == 'MPSK':
            msg = self.MSGRegularizer(self, msg, M)
            self.msg = msg
            s, f, q = np.array(filt.Modulations.MQAM(msg, M, T, itermG))  # modulação	sns.set_style("whitegrid")
        else:
            print("Modulação Inválida")
            flag=False
        if flag:
            if fq:
                "Grafico Real/Imag Habilitado"
                Pymodulator.printFQ(f, q)
            sns.set_style("whitegrid")
            pd.DataFrame({f"Sinal {modtype.upper()}": s}).plot()
            plt.title("Sinal {} Sem Ruído".format(modtype.upper()))
            plt.show()
            return s

    def Noiser(self, s, SNR):
        print("Canal AWGN Habilitado")
        cs = Chan_N.WhiteNoiseGenerator(s, SNR, self.T)
        sns.set_style("whitegrid")
        pd.DataFrame({f"Sinal {self.modtype.upper()} (Com Ruido Branco)": cs}).plot()
        plt.title("Sinal {} Com Ruído SNR = {}".format(self.modtype.upper(), SNR))
        plt.show()


    def Demodulate(self, s, M, finalG=False):
        print("Demodulação Habilitada")
        if self.modtype.upper() == 'MQAM':
            rec2 = np.array(filt.Demodulations.De_MQAM(s, M, self.T, self.itermG))  # modulação	sns.set_style("whitegrid")
        elif self.modtype.upper() == 'MPSK':
            rec2 = np.array(filt.Demodulations.De_MPSK(s, M, self.T, self.itermG))  # modulação	sns.set_style("whitegrid")
        print(self.msg)
        print("diff = {}".format(len([abs(self.msg[i] - rec2[i]) for i in range(0, len(self.msg)) if (self.msg[i] != rec2[i])])))
        if finalG:
            sns.set_style("whitegrid")
            pd.DataFrame({"Original": self.msg, "Reconstituído": rec2}).plot()
            plt.title("Comparação da Mensagem Reconstituída")
            plt.show()
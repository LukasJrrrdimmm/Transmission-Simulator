import math as mth
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import commpy.modulation as commod
import mpskadjust as pskf
import carrier as crr
import scipy.fft as FFT

def binary_generator(s, N):
    return np.random.randint(2, size = s**N)

def max2pow(lim):
    i = 0
    a = 2**i
    while 1:
        if a >= lim:
            break
        else:
            i += 1
            a = 2**i
    return a

def eqalising2pow(l, M):
    i = M
    a = 2**M
    while 1:
        if a % i == 0:
            break
        else:
            i -= 1
            a = 2**i
    return a

def itob_array(v, N):
    bin_vec = []
    for num in v:
        print(num)
        aux = bin(int(num)).split('b')[1]
        g = ''
        if len(aux) < N:
            c = 0
            for i in range(0, mth.ceil(N)):
                g += '0'
                c += 1
                if c + len(aux) == N:
                    bin_vec.append(g+aux)
                    break
        else:
            bin_vec.append(aux)
    print(bin_vec)
    return bin_vec



def QuadratureDecoder(v, N):
    s = ''
    for i in range(0, N):
        for num in v:
            s += num[i]
    return s
class GRAY:
    def gray_generator_map(N):
        gray_dict = {}
        for i in range (0, N):
            a = (i - N/2)
            n = a
            if a >= 0:
                a = (i - N/2) + 1
                n = a
            if (abs(n)-1) != 0:
                n = (3*(abs(n)-1))*(n/abs(n))
            gray_dict[i] = [bin(i), n]
        return gray_dict
    def gray_mapping(l1):
        a2 = []
        l2 = 0
        lim2 = (2**l1)/2
        c1 = 0
        c2 = 0
        while 1: #Mapeamento de Bits
            if (c1-lim2) < 0: # Execução da
                if (c2-lim2) < 0:
                    a2.append((c1 - lim2) + 1j*(c2 - lim2))
                else:
                    a2.append((c1 - lim2) + 1j*(c2 - (lim2 - 1)))
            else:
                if (c2-lim2) < 0:
                    a2.append((c1 - (lim2 - 1)) + 1j*(c2 - lim2))
                else:
                    a2.append((c1 - (lim2 - 1)) + 1j*(c2 - (lim2 - 1)))
            c1 += 1
            if c1 == lim2*2:
                c1 = 0
                c2 += 1
            if c2 == lim2*2:
                c2 = 0
                break
        n = np.array(a2)
        print("|X0 Y0|")
        print(n.real)
        print(n.imag)
        sns.set_style("whitegrid")
        plt.axis([-lim2-1, lim2+1, -lim2-1, lim2+1])
        plt.plot(n.real, n.imag, "ko")
        plt.show()

def plot_message(qr, qi):
    sns.set_style("whitegrid")
    pd.DataFrame({"X": qr, "Y": qi}).plot(subplots=True)
    plt.title("Pre-Mod Constellated")
    plt.show()

class Modulations:
    def MPPM(v, M, T, itermG=False):
        print("Modulação Iniciada")
        modcpy = commod.QAMModem(M)
        a2 = modcpy.modulate(v)
        qam_real = a2.real
        qam_img = a2.imag
        m = []
        q = []
        i = []
        f, t = crr.Generic_Carrier(T)
        print(f"{f} , {t}")
        if itermG == True:
            plot_message(qam_real, qam_img)
        for k in range(0,len(qam_real)):
            yr=qam_real[k]*np.array([1]*int(t))
            yim=qam_img[k]*np.array([1]*int(t))
            y=[a + b for a, b in zip(yr, yim)]
            m = m + y
            q = q + list(yr)
            i = i + list(yim)
        print("Modulação Finalizada")
        return np.array(m), np.array(q), np.array(i)

    def MQAM_Entrelac_TH(v, sz, M, T, itermG=False):
        # Geração do sinal MQAM Entrelaçado tipo A (divisão pelo logatítimo do comprimento da mensagem)
        """
        v = mensagem de Entrada
        M = nº da modulação
        T = periodo do quadro
        """
        dec = ""
        bin_arr_x0 = []
        lim = max2pow(np.log2(sz)) # Execução do logarítimo para iteração
        if lim > 64: # (M <= 64)
            lim = 64
        print("M = {}QAM".format(lim))
        print("Entrelaçamento Iniciado")
        for i in range (0, int(lim)): # Divisão do vetor
            bin_arr_x0.append(np.array(v[int(i*(len(v)/lim)):(i+1)*(int(len(v)/lim))]))
        print(np.array(v))
        print(len(v))
        aux = np.transpose(np.array(bin_arr_x0)) # transposição do vetor
        print(aux)
        a2 = []
        print("Entrelaçamento Finalizado")
        print("Modulação Iniciada")
        modcpy = commod.QAMModem(M)
        l1 = 0
        # obtenção das partes reiais e imaginárias a partir da divisão da matriz transposta e conversão M-ária gradual
        for b in aux: # mapeamento dos bits
            d1 = modcpy.modulate(b)
            l1 = len(d1)
            for i in d1:
                a2.append(i)
        a2 = np.array(a2)
        qam_real = a2.real
        qam_img = a2.imag
        m = []
        f, t = crr.Generic_Carrier(T)
        print(f"{f} , {t}")
        if itermG == True:
            plot_message(qam_real, qam_img)
        for k in range(0,len(qam_real)):
            yr=qam_real[k]*np.cos(2*np.pi*f*t)
            yim=qam_img[k]*np.sin(2*np.pi*f*t)
            y=[a + b for a, b in zip(yr, yim)]
            m = m + y
        c1 = np.cos(2*np.pi*f*t)
        print("Modulação Finalizada")
        return np.array(m), l1, len(c1), qam_real, qam_img

    def MQAM_Entrelac_TV(v, sz, M, T, itermG=False):
        # Geração do sinal MQAM Entrelaçado Tipo B (usando divisão vetorial de tamanho igual ao logaritmo do tamanho da mensagem)
        """
        v = mensagem de Entrada
        M = nº da modulação
        T = periodo do quadro
        """
        print("Entrelaçamento Iniciado")
        dec = ""
        bin_arr_x0 = []
        lim = max2pow(np.log2(M)) # Execução do logarítimo para iteração
        if lim > 16: # (M <= 256)
            lim = 16
        print("M = {}QAM".format(lim))
        for i in range(0, len(v), int(lim)): # Divisão do vetor
            bin_arr_x0.append(np.array(v[i:i+int(lim)]))
        print(np.array(v))
        print(len(v))
        aux = np.transpose(np.array(bin_arr_x0)) # transposição do vetor
        print(aux)
        a2 = []
        l1 = 0
        print("Entrelaçamento Finalizado")
        print("Modulação Iniciada")
        modcpy = commod.QAMModem(M)
        # obtenção das partes reiais e imaginárias a partir da divisão da matriz transposta e conversão M-ária gradual
        for b in aux: # mapeamento dos bits
            d1 = modcpy.modulate(b)
            l1 = len(d1)
            for i in d1:
                a2.append(i)
        a2 = np.array(a2)
        qam_real = a2.real
        qam_img = a2.imag
        m = []
        f, t = crr.Generic_Carrier(T)
        print(f"{f} , {t}")
        if itermG == True:
            plot_message(qam_real, qam_img)
        for k in range(0,len(qam_real)):
            yr=qam_real[k]*np.cos(2*np.pi*f*t)
            yim=qam_img[k]*np.sin(2*np.pi*f*t)
            y=[a + b for a, b in zip(yr, yim)]
            m = m + y
        c1 = np.cos(2*np.pi*f*t)
        print("Modulação Terminada")
        return np.array(m), l1, len(c1)

    def MQAM(v, M, Ts, T, itermG=False): # Geração do sinal MQAM
        """
        v = mensagem de Entrada
        M = nº da modulação
        Ts = período por símbolo
        T = periodo da portadora
        """
        print("Modulação Iniciada")
        modcpy = commod.QAMModem(M)
        a2 = modcpy.modulate(v)
        print(a2)
        qam_real = []
        qam_img = []
        for i in a2:
            qam_real += [i.real]*Ts
            qam_img += [i.imag]*Ts
        qam_real = np.array(qam_real)
        qam_img = np.array(qam_img)
        m = []
        q = []
        i = []
        f, t = crr.Generic_Carrier(T)
        print(f"{f} , {t}")
        if itermG == True:
            plot_message(qam_real, qam_img)
        for k in range(0,len(qam_real)):
            yr=qam_real[k]*np.cos(2*np.pi*f*t)
            yim=qam_img[k]*np.sin(2*np.pi*f*t)
            y=[a + b for a, b in zip(yr, yim)]
            m = m+y
            q = q + list(yr)
            i = i + list(yim)
        c1 = np.cos(2*np.pi*f*t)
        print("Modulação Terminada")
        return np.array(m), np.array(q), np.array(i)

    def MQPSK(v, M, T, itermG=False): #Double-MPSK geração de 2 sinais MPSK: 1 em fase e 1 em quadratura
        """
        v = mensagem de Entrada
        M = nº da modulação
        T = periodo do quadro
        """
        print("Modulação Iniciada")
        dec = ""
        print(np.array(v))
        modcpy = commod.QAMModem(M)
        a2 = modcpy.modulate(v)
        print(np.array(a2))
        if itermG == True:
            plot_message(np.array(a2).real, np.array(a2).imag)
            s = []
            # Ajuste do MPSK
            gs = pskf.cosAdjust(np.array(a2).real, T, M) + pskf.sinAdjust(np.array(a2).imag, T, M)
            print(np.array(gs))
            f, t = crr.Generic_Carrier(T)
            c1 = np.cos(2*np.pi*f*t)
        print("Modulação Terminada")
        return np.array(gs), a2.real, a2.imag

    def MPSK(v, M, Ts, T, itermG=False):
        # Geração do sinal MQAM
        """
        v = mensagem de Entrada
        M = nº da modulação
        T = periodo do quadro
        """
        print("Modulação Iniciada")
        modcpy = commod.PSKModem(M)
        a2 = modcpy.modulate(v)
        qam_real = []
        qam_img = []
        for i in a2:
            qam_real += [i.real] * Ts
            qam_img += [i.imag] * Ts
        print(np.array(qam_real) + 1j*np.array(qam_img))
        m = []
        q = []
        i = []
        f, t = crr.Generic_Carrier(T)
        print(f"{f} , {t}")
        if itermG == True:
            plot_message(qam_real, qam_img)
        for k in range(0,len(qam_real)):
            yr=qam_real[k]*np.cos(2*np.pi*f*t)
            yim=qam_img[k]*np.sin(2*np.pi*f*t)
            y=[a + b for a, b in zip(yr, yim)]
            m = m+y
            q = q + list(yr)
            i = i + list(yim)
        print("Modulação Terminada")
        return np.array(m), np.array(q), np.array(i)# s(t), T


class Demodulations:
    def get0signal(x, y, M):
        lim = np.log2(M)
        rs = []
        for i in range(0, len(x)):
            aux_a = bin(x[i])
            aux_b = bin(y[i])
            xa = aux_a.split('b')[1]
            xb = aux_b.split('b')[1]
            la = len(xa.split(''))
            lb = len(xb.split(''))
            c = lim/2
            aux_xa = ""
            for j in range (0, lim/2):
                if(c > la):
                    aux_xa += "0"
                else:
                    aux_xa += xa
                    break
                c -= 1
            c = lim/2
            aux_xb = ""
            for j in range (0, lim/2):
                if(c > lb):
                    aux_xb += "0"
                else:
                    aux_xb += xa
                    break
                c -= 1
            rs.append(aux_xa + aux_xb)
        print(np.array(rs))
    #	def De_MQPM(signal, M, T):
    def De_MQAM(signal, M, Ts, T, itermG=False):
        """
        signal = sinal modulado
        M = nº da modulação
        key = chave de desentrelaçamento da constelação
        T = período do cada quadro
        """
        modcpy = commod.QAMModem(M)
        msg = crr.CarrierDemodeQAM(signal, Ts, T, modcpy, itermG)
        return msg
    def De_MQAM_Entrelac_TV(signal, key, M, T, itermG=False):
        """
        signal = sinal modulado
        M = nº da modulação
        key = chave de desentrelaçamento da constelação
        T = período do cada quadro
        """
        modcpy = commod.QAMModem(M)
        msg = crr.CarrierDemodeQAMEntrelac(signal, T, modcpy, key, itermG)
        return msg
    def De_MQAM_Entrelac_TH(signal, key, M, T, itermG=False):
        """
        signal = sinal modulado
        M = nº da modulação
        key = chave de desentrelaçamento da constelação
        T = período do cada quadro
        """
        modcpy = commod.QAMModem(M)
        msg = crr.CarrierDemodeQAMEntrelac(signal, T, modcpy, key, itermG)
        return msg
    def De_MPSK(signal, M, Ts, T, itermG=False):# D-MPSK
        """
        signal = sinal modulado
        M = nº da modulação
        key = chave de desentrelaçamento da constelação
        T = período do cada quadro
        """
        modcpy = commod.PSKModem(M)
        msg = crr.CarrierDemodeMPSK(signal, Ts, T, modcpy, itermG)
        return msg


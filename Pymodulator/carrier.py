import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd


def Generic_Carrier(T, period=False):
    bp = 0.01
    sp = bp * 2  # symbol period for M-array QAM
    sr = 1 / sp  # symbol rate
    f = sr * 2  # carry frequency
    t = np.arange(0, sp, sp / T)
    if period == False:
        return t, f
    else:
        return t, f, sp


def plot_message(qr, qi):
    sns.set_style("whitegrid")
    pd.DataFrame({"X": qr, "Y": qi}).plot(subplots=True)
    plt.title("Pre-Mod Constellated")
    plt.show()


def CarrierDemodeQAMEntrelac(signal, T, modcpy, key, itermG=False):
    print("Demodulação Iniciada:")
    t, f, sp = Generic_Carrier(T, period=True)
    sig1 = []
    sig2 = []
    xgm = []
    c1 = np.cos(2 * np.pi * f * t)
    c2 = np.sin(2 * np.pi * f * t)
    g1 = []
    h1 = []
    for i in range(0, len(signal), len(c1)):
        g = np.trapz((signal[[j for j in range(i, (i + len(c1)))]] * c1), t)
        g1 = round(2 * g / sp)
        h = np.trapz((signal[[j for j in range(i, (i + len(c1)))]] * c2), t)
        h1 = round(2 * h / sp)
        # print(g1)
        sig1.append(g1)
        sig2.append(h1)
        # print(h1)
        print("============{}B |{}| ".format((i / len(c1)), (np.array(g1) + 1j * np.array(h1))))
        xgm += [np.array(g1) + 1j * np.array(h1)]
    if itermG:
        plot_message(np.array(sig1), np.array(sig2) * 1j)
    localiza = np.array(sig1) + 1j * np.array(sig2)
    print("Demodulação Finalizada")
    print("Variável Localiza:")
    print(localiza)
    print("Desentrelaçamento Iniciado")
    entrelac_M = []
    aux = []
    for i in range(0, len(localiza), key):
        entrelac_M.append(modcpy.demodulate(localiza[i: i + key], demod_type="hard"))
    # desconversão da constelação realizada no desentrelaçamento
    msg_EM = np.transpose(np.array(entrelac_M))
    msg = []
    for vec in msg_EM:
        for i in vec:
            msg.append(i)
    print("Desentrelaçamento Finalizado")
    return np.array(msg)


def CarrierDemodeQAM(signal, T, modcpy, itermG=False):
    print("Demodulação Iniciada:")
    t, f, sp = Generic_Carrier(T, period=True)
    sig1 = []
    sig2 = []
    c1 = np.cos(2 * np.pi * f * t)
    c2 = np.sin(2 * np.pi * f * t)
    g1 = []
    h1 = []
    for i in range(0, len(signal), len(c1)):
        g = np.trapz((signal[[j for j in range(i, (i + len(c1)))]] * c1), t)
        g1 = round(2 * g / sp)
        h = np.trapz((signal[[j for j in range(i, (i + len(c1)))]] * c2), t)
        h1 = round(2 * h / sp)
        print("============{}B |{}| ".format((i / len(c1)), (np.array(g1) + 1j * np.array(h1))))
        sig1.append(g1)
        sig2.append(h1)
    # print(sig1)
    # print(sig2)
    if itermG:
        plot_message(np.array(sig1), np.array(sig2) * 1j)
    # esse vetor é complexo
    localiza = np.array(sig1) + 1j * np.array(sig2)
    # usar o mapeamento  com compy (essa função não existe, use o compy para fazer esse mapeamento)
    msg = modcpy.demodulate(localiza, demod_type="hard")
    print("Demodulação Finalizada")
    print("Variável Localiza:")
    print(localiza)
    return msg


#


def CarrierDemodeMPSK(signal, T, modcpy, itermG=False):
    print("Demodulação Iniciada:")
    t, f, sp = Generic_Carrier(T, period=True)
    sig1 = []
    sig2 = []
    c1 = np.cos(2 * np.pi * f * t)
    c2 = np.sin(2 * np.pi * f * t)
    g1 = []
    h1 = []
    for i in range(0, len(signal), len(c1)):
        g = np.trapz((signal[[j for j in range(i, (i + len(c1)))]] * c1), t)
        g1 = 2 * g / sp
        h = np.trapz((signal[[j for j in range(i, (i + len(c1)))]] * c2), t)
        h1 = 2 * h / sp
        print("============{}B |{}| ".format((i / len(c1)), (np.array(g1) + 1j * np.array(h1))))
        sig1.append(g1)
        sig2.append(h1)
    # print(sig1)
    # print(sig2)
    # esse vetor é complexo
    if itermG:
        plot_message(np.array(sig1), np.array(sig2) * 1j)
    localiza = np.array(sig1) + 1j * np.array(sig2)

    # usar o mapeamento  com compy (essa função não existe, use o compy para fazer esse mapeamento)
    msg = modcpy.demodulate(localiza, demod_type="hard")
    print("Demodulação Finalizada")
    print("Variável Localiza:")
    print(localiza)
    return msg

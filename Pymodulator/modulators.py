import numpy as np
import multiprocessing as mp

def mqam(signal, fe, amp):#-> numpy_array
	moduled_signal_mqam1 = []
	moduled_signal_mqam2 = []
	j = 0
	for i in signal:
		moduled_signal_mqam1.append(amp*i*np.cos((np.pi/4)*fe + j*(np.pi/4)))
		moduled_signal_mqam2.append(amp*i*np.sin((np.pi/4)*fe + j*(np.pi/4)))
		j+=1
	return [np.array(moduled_signal_mqam1), np.array(moduled_signal_mqam2)]

def mpsk_modulate1(value, fe, amp, mu, dp, j):
	if value <= mu-dp:
		return(amp*value*np.array(np.sin(2*(np.pi/4)*fe*j)))
	elif value <= mu:
		return(amp*value*np.array(np.sin(2*(np.pi/4)*fe*j + np.pi/4)))
	elif value <= mu+dp:
		return(amp*value*np.array(np.sin(2*(np.pi/4)*fe*j + np.pi/2)))
	else:
		return(amp*value*np.array(np.sin(2*(np.pi/4)*fe*j + 3*np.pi/4)))

def mpsk_modulate2(value, fe, amp, mu, dp, j):
	if value <= mu-dp:
		return(amp*value*np.array(np.cos(2*(np.pi/4)*fe*j)))
	elif value <= mu:
		return(amp*value*np.array(np.cos(2*(np.pi/4)*fe*j + np.pi/4)))
	elif value <= mu+dp:
		return(amp*value*np.array(np.cos(2*(np.pi/4)*fe*j + np.pi/2)))
	else:
		return(amp*value*np.array(np.cos(2*(np.pi/4)*fe*j + 3*np.pi/4)))

def mpsk(signal, fe, amp, mu, dp):
	moduled_signal_mpsk1 = []
	moduled_signal_mpsk2 = []
	j = 0
	for value in signal:
		moduled_signal_mpsk1.append(mpsk_modulate1(value, fe, amp, mu, dp, j))
		moduled_signal_mpsk2.append(mpsk_modulate2(value, fe, amp, mu, dp, j))
	return [moduled_signal_mpsk1, moduled_signal_mpsk2]

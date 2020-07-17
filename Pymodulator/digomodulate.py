import numpy as np
import conetrlar as cnt

class carrier:
	def module_freq(f0, star):
		return f0*(star/16)
	def p500Hz_10A():
		freq = 500
		amp = 10
		return [freq, amp]

	def p1KHz_20A():
		freq = 1000
		amp = 20
		return [freq, amp]

	def sin_carrier(mm10):
		return np.sin(np.randon.random((mm10,))*mm10)

	def cos_carrier(mm10):
		return np.cos(np.randon.random((mm10,))*mm10)

	def sign_carrier(mm10):
		return np.sign(np.randon.random((mm10,))*mm10)

	def digital_carrier(mm10):
		return np.sin(np.randon.bytes((mm10,)))
class MPSK:
	def M1(signal, amp, f0):
		best_c = cnt.best_constelaris(len(signal))
		constellation = cnt.constelaris_factory(signal, best_c)
		star_signal = []
		quadrature_signal = []
		t = 0
		for star in constellation:
			fm = module_freq(f0, star)
			for i in range(0, best_c):
				star_signal.append(amp*np.cos(np.pi/4*fm*t))
				quadrature_signal.append(- amp*np.sin(np.pi/4*fm*t))
				t += 1
		return [np.array(star_signal), np.array(quadrature_signal)]

	def M2(signal, amp, f0, constelar_num):
		constellation = cnt.constelaris_factory(signal, constelar_num)
		star_signal = []
		quadrature_signal = []
		t = 0
		for star in constellation:
			fm = module_freq(f0, star)
			for i in range(0, constelar_num):
				star_signal.append(amp*np.cos(np.pi/4*fm*t))
				quadrature_signal.append(- amp*np.sin(np.pi/4*fm*t))
				t += 1
		return [np.array(star_signal), np.array(quadrature_signal)]

class MQAM:
	def M1(signal, amp, f0):
		best_c = cnt.best_constelaris(len(signal))
		constellation = cnt.constelaris_factory(signal, best_c)
		star_signal = []
		quadrature_signal = []
		t = 0
		for star in constellation:
			fm = module_freq(f0, star)
			for i in range(0, best_c):
				star_signal.append(star*amp*np.cos(np.pi/4*f0*t))
				quadrature_signal.append(star*amp*np.sin(np.pi/4*f0*t))
				t += 1
		return [np.array(star_signal), np.array(quadrature_signal)]

	def M2(signal, amp, f0, constelar_num):
		constellation = cnt.constelaris_factory(signal, constelar_num)
		star_signal = []
		quadrature_signal = []
		t = 0
		for star in constellation:
			fm = module_freq(f0, star)
			for i in range(0, constelar_num):
				star_signal.append(star*amp*np.cos(np.pi/4*f0*t))
				quadrature_signal.append(star*amp*np.sin(np.pi/4*f0*t))
				t += 1
		return [np.array(star_signal), np.array(quadrature_signal)]
class MASK:
	def M1(signal, amp):
		ask_single = []
		for bit in signal:
			if bit == 0:
				bit = -1
			ask_single.append(bit)
		return np.array(ask_single)

	def M2(signal, amp, f0, constellar_num):
		constellation = cnt.constelaris_factory(signal, constellar_num)
		ASK_Signal = []
		factor = constellar_num/2
		t = 0
		for bit in constellation:
			if bit-factor >= 0:
				s = bit - factor + 1
			else:
				s = bit - factor
			for i in range (0, constellar_num):
				ASK_Signal.append(s*np.cos(np.pi/4*f0*t))
			t += 1
		return np.array(ASK_Signal)
			


def strBits(w):
	a = list(w)
	b = []
	print(a)
	for i in a:
		b.append(ord(i))
	s = []
	print(b)
	for i in a:
		if ord(i) <= ord('Z'):
			s.append(list("1{0:06b}".format(ord(i)-(ord('A')))))
		elif ord(i) <= ord('z'):
			s.append(list("0{0:06b}".format(ord(i)-(ord('a')))))
	print(s)
	sf = []
	for v in s:
		f = len(v)
		for i in v:
			sf.append(int(i))
	print(sf)
	print(len(sf))
	return sf, f

def bitsStr(sf, f):
	c = 0
	s1 = ""
	aux = 0
	r = []
	for n in r:
		s += str(n)
		if c = 1:
			aux = int(s1, 2)
			s1 = ""
		elif c = f:
			if aux == 0:
				r.append(chr(int(s1, 2) + ord('A')))
			else:
				r.append(chr(int(s1, 2) + ord('a')))
	return r

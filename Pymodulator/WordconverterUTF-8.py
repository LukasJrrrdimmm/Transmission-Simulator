def strBits(w):
	a = list(w)
	b = []
	print(a)
	for i in a:
		b.append(ord(i))
	s = []
	print(b)
	for i in a:
		s.append(list("{0:08b}".format(ord(i)))))
	print(s)
	sf = []
	for v in s:
		f = len(v)
		for i in v:
			sf.append(int(i))
	print(sf)
	print(len(sf))
	return sf

def bitsStr(sf, f):
	c = 0
	s1 = ""
	aux = 0
	r = []
	for n in r:
		s += str(n)
		elif c = f:
			r.append(chr(int(s1, 2) + ord('A')))
	return r

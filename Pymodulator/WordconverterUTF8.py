def strBits(w):
	a = list(w)
	b = []
	print(a)
	for i in a:
		b.append(ord(i))
	s = []
	print(b)
	for i in a:
		s.append(list("{0:08b}".format(ord(i))))
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
	r = ""
	for n in sf:
		if c == f:
			r += chr(int(s1, 2))
			c = 0
			s1 = ""
		s1 += str(n)
		c += 1
	r += chr(int(s1, 2))
	c = 0
	s1 = ""
	return r

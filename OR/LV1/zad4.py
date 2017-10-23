def Ispisi(seq):
	if type(seq) == list:
		print('{', end='')
		for elem in seq:
			Ispisi(elem)
			if elem != seq[-1]:
				print(', ', end='')
		print('}', end='')
	else:
		print(seq, end='')

Ispisi([1, 7, [-1, [-2, 100], -3], 4, 5, [10, 20, 30]])
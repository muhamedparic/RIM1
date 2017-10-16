def Permutacije(seq):
	def Glupe_permutacije(seq, n = None):
		if n is None:
			n = len(seq)
		if n == 1:
			yield seq[:]
		else:
			for i in range(n - 1):
				for perm in Glupe_permutacije(seq, n - 1):
					yield perm
				j = 0 if n % 2 == 0 else i
				seq[j], seq[n - 1] = seq[n - 1], seq[j]
			for perm in Glupe_permutacije(seq, n - 1):
				yield perm
	return list(Glupe_permutacije(seq))
            

#perms = list(Permutacije([1, 2, 3, 4]))
print(Permutacije([int(num) for num in input().split(' ')]))
#print(len(Permutacije([1, 2, 3, 4, 5, 6])))

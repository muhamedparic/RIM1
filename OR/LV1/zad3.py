import random

def Generisi(duzina):
	chars = ['A', 'B', 'C', 'D', 'E']
	return [random.choice(chars) for _ in range(duzina)]


def Najslicnije(duzina, broj_uzoraka):
	uzorci = [Generisi(duzina) for _ in range(broj_uzoraka)]
	def dist(seq1, seq2):
		diff_cnt = 0
		for pair in zip(seq1, seq2):
			if pair[0] != pair[1]:
				diff_cnt += 1
		return diff_cnt
	list1, list2, list_diff = None, None, duzina + 1
	for i in range(broj_uzoraka - 1):
		for j in range(i + 1, broj_uzoraka):
			cur_dist = dist(uzorci[i], uzorci[j])
			if cur_dist < list_diff:
				list1 = uzorci[i]
				list2 = uzorci[j]
				list_diff = cur_dist
	return list1, list2
	
print(Najslicnije(4, 10))
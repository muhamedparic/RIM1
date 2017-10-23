class Matrica:
    def __init__(self, pocetna_vrijednost = None):
        self.elementi = pocetna_vrijednost if pocetna_vrijednost is not None else []


    def at(self, i, j):
        return self.elementi[i][j]


    def zeros(self, n, m = None):
        if m is None:
            m = n
        self.elementi = [[0 for i in range(m)] for j in range(n)]


    def ones(self, n, m):
        if m is None:
            m = n
        self.elementi = [[1 for i in range(m)] for j in range(n)]


    def eye(self, n):
        self.elementi = [[1 if i == j else 0 for i in range(n)] for j in range(n)]


a = Matrica([[1, 2, 3], [4, 5, 6]])
a.eye(5)
print(a.at(2, 2))

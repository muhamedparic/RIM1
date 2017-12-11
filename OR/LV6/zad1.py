from __future__ import print_function, division
import random

class ApstraktnaIndividua:
    def __init__(self, DuzinaHromozoma):
        if DuzinaHromozoma < 1:
            raise Exception('Duzina hromozoma mora biti cijeli broj veci od 0')
        self.DuzinaHromozoma = DuzinaHromozoma
        self.Hromozom = [random.randint(0, 1) for _ in range(DuzinaHromozoma)]
        self.Fitness = -float('inf')

    def SetDuzinaHromozoma(self, val):
        self.DuzinaHromozoma = val
        return self

    def GetDuzinaHromozoma(self):
        return self.DuzinaHromozoma

    def SetHromozom(self, val):
        if len(val) != self.DuzinaHromozoma:
            raise Exception('Duzina hromozoma nije ispravna')
        self.Hromozom = val
        return self

    def GetHromozom(self):
        return self.Hromozom

    def SetFitness(self, val):
        self.Fitness = val
        return self

    def Evaluiraj(self):
        pass

class MojaIndividua(ApstraktnaIndividua):
    def Evaluiraj(self):
        pass

class Populacija:
    def __init__(self, VelicinaPopulacije, VjerovatnocaKrizanja, VjerovatnocaMutacije, MaxGeneracija, VelicinaElite, DuzinaHromozoma = 16):
        if VjerovatnocaKrizanja < 0 or VjerovatnocaKrizanja > 1:
            raise Exception('Vjerovatnoca krizanja mora biti u intervalu [0, 1]')
        if VjerovatnocaMutacije < 0 or VjerovatnocaMutacije > 1:
            raise Exception('Vjerovatnoca mutacije mora biti u intervalu [0, 1]')
        if MaxGeneracija <= 0:
            raise Exception('Maksimalan broj generacija mora biti > 0')
        if VelicinaElite < 0 or VelicinaElite > 2:
            raise Exception('Velicina elite mora biti u intervalu [0, 2]')
        self.VelicinaPopulacije = VelicinaPopulacije
        self.VjerovatnocaKrizanja = VjerovatnocaKrizanja
        self.VjerovatnocaMutacije = VjerovatnocaMutacije
        self.MaxGeneracija = MaxGeneracija
        self.VelicinaElite = VelicinaElite
        self.DuzinaHromozoma = DuzinaHromozoma

    def SetVelicinaPopulacije(self, val):
        self.VelicinaPopulacije = val
        return self

    def GetVelicinaPopulacije(self):
        return self.VelicinaPopulacije

    def SetVjerovatnocaKrizanja(self, val):
        if val < 0 or val > 1:
            raise Exception('Vjerovatnoca krizanja mora biti u intervalu [0, 1]')
        self.VjerovatnocaKrizanja = val
        return self

    def GetVjerovatnocaKrizanja(self):
        return self.VjerovatnocaKrizanja

    def SetVjerovatnocaMutacije(self, val):
        if val < 0 or val > 1:
            raise Exception('Vjerovatnoca mutacije mora biti u intervalu [0, 1]')
        self.VjerovatnocaMutacije = val
        return self

    def GetVjerovatnocaMutacije(self):
        return self.VjerovatnocaMutacije

    def SetMaxGeneracija(self, val):
        if val <= 0:
            raise Exception('Maksimalan broj generacija mora biti > 0')
        self.VelicinaPopulacije = val
        return self

    def GetMaxGeneracija(self):
        return self.VelicinaPopulacije

    def GetVelicinaElite(self):
        return self.VelicinaElite

    def SetVelicinaElite(self, val):
        if val < 0 or val > 2:
            raise Exception('Velicina elite mora biti u intervalu [0, 2]')
        self.VelicinaElite = val
        return self

    def GetDuzinaHromozoma(self):
        return self.DuzinaHromozoma

    def SetDuzinaHromozoma(self, val):
        if val <= 0:
            raise Exception('Duzina hromozoma mora biti > 0')
        self.DuzinaHromozoma = val
        return self

    def OpKrizanjaTacka(self, h1, h2):
        tackaUkrstanja = random.randint(0, len(h1) - 2)
        p1, p2 = [], []
        for i in range(len(h1)):
            if i <= tackaUkrstanja:
                p1.append(h1[i])
                p2.append(h2[i])
            else:
                p1.append(h2[i])
                p2.append(h1[i])
        return p1, p2

    def OpKrizanjaDvijeTacke(self, h1, h2):
        tackaUkrstanja1, tackaUkrstanja2 = None, None
        while tackaUkrstanja1 == tackaUkrstanja2:
            tackaUkrstanja1 = random.randint(0, len(h1) - 3)
            tackaUkrstanja2 = random.randint(0, len(h1) - 2)
            if tackaUkrstanja1 > tackaUkrstanja2:
                tackaUkrstanja1, tackaUkrstanja2 = tackaUkrstanja2, tackaUkrstanja1
        i = 0
        p1, p2 = [], []
        while i <= tackaUkrstanja1:
            p1.append(h1[i])
            p2.append(h2[i])
            i += 1
        while i <= tackaUkrstanja2:
            p1.append(h2[i])
            p2.append(h1[i])
        while i < len(h1):
            p1.append(h1[i])
            p2.append(h2[i])
        return p1, p2

    def OpBinMutacija(self, h):
        return [(1 - g) if random.random() < self.GetVjerovatnocaKrizanja() else g for g in h]

def Test():
    p = Populacija(10, .99 , .99, 10, 1, 10)
    r1 = random.randint(1, p.GetVelicinaPopulacije() - 1)
    r2 = random.randint(1, p.GetVelicinaPopulacije() - 1)
    p1 = p.GetPopulacija()[r1]
    p2 = p.GetPopulacija()[r2]
    print("P1", p1.GetHromozom())
    print("P2" , p2.GetHromozom())
    c1, c2 = p.OpKrizanjeTacka(p1, p2)
    print("C1", c1.GetHromozom())
    print("C2", c2.GetHromozom())
    c3 = p.OpBinMutacije(c1)
    print("C3", c3.GetHromozom(), "C1 Nakon mutiranja")

Test()

import math
class Wind:
    """ calculations for wind pressures """
    def __init__(self, A, Cdir, Cs, Cp, z, vmap):
        self.A = A # altitude 
        self.Cdir = Cdir # direction factor
        self.Cs = Cs # seasonal factor
        self.Cp = Cp # probability factor
        self.z = z # height above ground level
        self.vmap = vmap # basic map wind speed

        # calculate the altitute factor
        if self.z <= 10:
            self.Ca = 1+0.001*self.A
        else:
           self.Ca = 1+0.001*self.A*(10/self.z)**0.20
        self.vb = self.Cdir * self.Cs * self.Cp * self.Ca * vmap
        self.qb = 0.613 * self.vb**2

    def qp(self, Cez, Cet):
        """ calculate the peak velocity pressure given Cez and Cet """
        qpValue = Cez *  Cet * self.qb * 10**-3 # value in kPa
        print(f"The peak velocity pressure = {qpValue:.2f}kPa")
        return Cez * Cet * self.qb

    def hDispl(self, h, have, x):
        if x <= 2*have:
            return min(0.8*have, 0.60 * h)
        elif x >= 6 * have:
            return  0
        else:
            return min(1.2*have - 0.20*x, 0.60 * h)


def cProbCal(p):
    n = 0.50
    K = 0.20
    cp = ((1-K*math.log(-math.log(1-p)))/(1-K*math.log(-math.log(0.98))))**n
    return cp
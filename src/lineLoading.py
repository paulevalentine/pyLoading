# Line load calculation module
# 01 May 2023 
# Paul Valentine

class LineLoad:
    """ calculate UDL line loading """
    def __init__(self, name, gk, qk, lengths):
        """
        name is the reference
        gk is a dictionary of dead loads
        qk is a dictionary of imposed loads
        lengths is a list of attributary lengths
        """
        self.name = name
        self.gk = gk
        self.qk = qk
        self.lengths = lengths

        print(name+':')
        self.total_gk = 0
        for load, length in zip(self.gk.items(), self.lengths):
            self.total_gk = self.total_gk + load[1]*length
        print(f"Total dead load = {self.total_gk:.2f}kN/m")

        self.total_qk = 0
        for load, length in zip(self.qk.items(), self.lengths):
            self.total_qk = self.total_qk + load[1]*length
        print(f"Total imposed load = {self.total_qk:.2f}kN/m")

    def sls_load(self):
        """ calculate the total sls loading """
        sls = self.total_gk + self.total_qk
        print(f"{self.name}: Total sls loading = {sls:.2f}kN/m")
        return sls

    def uls_load(self):
        """ calculate the total uls loading """
        uls = self.total_gk * 1.35 + self.total_qk * 1.5
        print(f"{self.name}: Total uls loading = {uls:.2f}kN/m")
        return uls


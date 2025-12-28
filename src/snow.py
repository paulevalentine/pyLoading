class Snow:
    def __init__(self, Z, A):
        self.A = A # altitude of the site
        self.Z = Z # snow zone number from the map

        self.sk = (0.15 + (0.1*self.Z+0.05))+((self.A-100)/525)
    
    def printSk(self):
        print(f"The characteristic ground snow load = {self.sk:.2f} kPa")
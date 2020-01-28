from FourMomentum import FourMomentum
import math

class Muon(FourMomentum):
    """A muon.
    Holds the muon four momentum
    """
    def __init__(self, px=0, py=0, pz=0, E=0):
        super(Muon, self).__init__(px, py, pz, E)
        self.charge = None
        self.iso = None

class Jet(FourMomentum):
    """A jet.
    Holds the muon four momentum
    """
    def __init__(self, px=0,py=0,pz=0,E=0):
        super(Jet, self).__init__(px, py, pz, E)
        self.has_b_tag = False

class MET(FourMomentum):
    def __init__(self,px=0,py=0):
        super(MET, self).__init__(px,py,0,0)


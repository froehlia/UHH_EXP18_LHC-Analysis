import math

class FourMomentum(object):
    """
    Four-momentum of a particle in the form of (px, py, pz, E)
    """
    def __init__(self, px=0, py=0, pz=0, E=0):
        self.px = px
        self.py = py
        self.pz = pz
        self.E = E

    def __add__(self, other):
        """
        implementation for adding two four-vectors.
        """
        # Exercise 1.1 Adding four-momenta:
        # this part needs to be implemented
        pass

    def __mul__(self, other):
        """
        implementation of vector multiplication.

        returns scalar if multiplication with other FourMomentum (aka scalar product)
        reutrns FourMomentum if multiplication with number
        """
        if isinstance(other, FourMomentum):
            # scalar product of two four-vectors
            result = 0.0

            # Exercise 1.2 invariant mass:
            # this part needs to be implemented

            return result

        elif isinstance(other, (int, long, float, complex)) and not isinstance(other, bool):
            # multiplication with a scalar
            new_fourvector = FourVector(self.E*other, self.px*other, self.py*other, self.pz*other)
            return new_fourvector

    # multiplication is commutative
    __rmul__ = __mul__

    def pt(self):
        """
        return transverse momentum
        """
        return math.sqrt(self.px**2 + self.py**2)

    def eta(self):
        """
        return pseudorapidity
        """
        theta = math.atan(self.py/self.px)
        return -1 * math.log(math.tan(theta/2))

    def phi(self):
        """
        return azimuthal angle phi
        """
        return math.acos(self.pz / math.sqrt(self.px**2 + self.py**2 + self.pz**2))
    
    def E(self):
        """
        return energy
        """
        return self.E

    def m(self):
        """
        return invariant mass.
        """
        m2 = self*self
        if m2 >= 0:
            return math.sqrt(m2)
        else:
            return -math.sqrt(-m2)

    def set_v4(self, *args):
        """
        Set four-momentum.
        Expects either 1 or 4 arguments:
        1 argument: FourMomentum
        4 arguments: px, py, pz, E
        """
        if len(args) == 4:
            self.__init__(args[0], args[1], args[2], args[3])
        elif len(args) == 1:
            self.__init__(args[0].px, args[0].py, args[0].pz, args[0].E)
        else:
            raise TypeError("set_v4() takes 1 or 4 arguments (%d given)" % len(args))


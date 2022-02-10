from FourMomentum import FourMomentum
import cmath, math, functools, itertools

class TopReco:

    def __init__(self, hl_diff, n_jet_min, n_jet_max):
        if(not (isinstance(hl_diff, (float,int)) and isinstance(n_jet_min, int) and isinstance(n_jet_max, int))):
            raise TypeError("Please use the correct parameter types for TopReco(float or int, int, int)")
        elif(hl_diff<0 or n_jet_min<2 or n_jet_min>n_jet_max):
            raise ValueError("Please use the correct parameter ranges for TopReco(x,y,z) with x>0, y>1 and z>=y")
        else:
            self.max_diff = hl_diff
            self.njet_min = n_jet_min
            self.njet_max = n_jet_max



    def neutrinoReconstruction(self, met, muon):
        Mw = 80.399
        mu = Mw**2/2 + met.pt()*muon.pt()*math.cos(math.acos(met.px / met.pt())-muon.phi())
        A = mu*muon.pz/muon.pt()**2
        B = mu**2*muon.pz**2/muon.pt()**4
        C = (muon.E**2*met.pt()**2-mu**2)/muon.pt()**2
        discriminant = B-C
        solutions=[]
        if(discriminant<0):
            solutions.append(A)
        else:
            solutions.append(A+math.sqrt(B-C))
            solutions.append(A-math.sqrt(B-C))
        return solutions

    def calculateTopMass(self, jets, met, muon):
        N_bjets = 0
        Mt = -1.0
        B_jet = []
        l_diff = self.max_diff
        if not isinstance(muon, FourMomentum) or not len(jets) > 2: return -1
        #Calculating the neutrino 4-vector by using the missing transverse energy (met)
        solutions = self.neutrinoReconstruction(met, muon)
        if not solutions: return -1

        #Counting number of b-tagged jets
        for x in range(len(jets)):
            if(jets[x].has_b_tag):
                N_bjets += 1
                B_jet.append(x)

        #Looping over all possible neutrino four momentums
        for sol in range(len(solutions)):
            neutrino = FourMomentum(met.px, met.py, solutions[sol], math.sqrt(met.pt()**2+solutions[sol]**2))
            #Looping over all jets as possible leptonic top candidates.
            for x in range(len(jets)):
                #If there are two B-jets we want the leptonic top to have one of them
                if(N_bjets > 1):
                    if(not jets[x].has_b_tag): continue

                #Calculating the four momentum and the mass of the leptonic top
                P_lep = neutrino + muon + jets[x]
                Mt_lep = math.sqrt(P_lep*P_lep)

                #For each leptonic top candidate there are N-1 jets for the hadronic top remaining
                for l in range(self.njet_min-1,self.njet_max):
                    #Looping over all possible permutations of N-1 jets for the hadronic top
                    for y in itertools.combinations(jets,l):
                        #We don't want to reuse the jet from the leptonic top
                        if jets[x] in y: continue
                        #Making sure that if possible b_tagged jets are getting used as b-jets
                        if N_bjets > 1 or (N_bjets == 1 and not jets[x].has_b_tag):
                            Contains_B_jet = False
                            for k in B_jet:
                                if jets[k] in y:
                                    Contains_B_jet = True
                                    break
                            if not Contains_B_jet: continue
                        #Sum of the N-1 jets that are getting used for hadronic top quark reconstruction
                        P_had = functools.reduce(lambda a,b: a+b, y)
                        Mt_had = math.sqrt(P_had*P_had)
                        #Only the best candidate is getting used.
                        if(l_diff > abs(Mt_lep - Mt_had)):
                            l_diff = abs(Mt_lep - Mt_had)
                            Mt = (Mt_lep + Mt_had) / 2
        return Mt

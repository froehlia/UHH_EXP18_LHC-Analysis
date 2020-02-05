from Analyzer import Analyzer
from uhhHists import DefaultHistograms
from uhhHists import TopMassHist
from FourMomentum import FourMomentum
from ROOT import TH1F
import cmath
import math
import functools
import itertools

class TTbarAnalyzer(Analyzer):
    """
    Analyzer for the ttbar cross-section and mass measurement.
    Derived from Analyzer base class.
    """

    def __init__(self, dataset_name, file_name, event_options = {}):
        # initialize base class functionality
        # DO NOT TOUCH #
        super(TTbarAnalyzer, self).__init__(dataset_name, file_name, event_options)
        ################

        ## Add the Histograms you want to use here
        self.attach_histogram(DefaultHistograms(dataset_name+"_no_cuts"), "no_cuts")
        self.attach_histogram(DefaultHistograms(dataset_name+"_trigger"), "trigger")

        #self.attach_histogram(TopMassHist(dataset_name+"_top_mass"), "top_mass")
        
        ## Here you can define your own variables ##
        self.n_total = 0.0

        ## Variables for Top Quark Reconstruction ##
        self.m_top = 0.0
        self.n_top = 0.0
        #########################################

    def process(self,event):
        """
        This method is called for each event.
        You can fill all attatched histograms using self.fill_histograms(event, <hist_name>).
        """

        # increase total number of events for processed dataset
        self.n_total += 1
        # fill initial histogram
        self.fill_histograms(event, "no_cuts")

        # check if event fulfills the "IsoMu24" trigger
        if not event.trigger["IsoMu24"]:
            return


        ############################################

        self.fill_histograms(event, "trigger")
        # only events fulfilling the "IsoMu24" trigger will be further processed

        ## Top Quark Reconstruction ##
        mass = self.calculateTopMass(event.jets, event.met, event.muons[0])

        if(mass > 0):
            self.m_top += mass
            self.n_top += 1
            event.top_mass = mass
            self.fill_histograms(event, "top_mass")

    def neutrinoReconstruction(self, met, muon):
        Mw = 80.399
        mu = Mw**2/2 + met.pt()*muon.pt()*math.cos(math.acos(met.px / met.pt())-muon.phi())
        A = mu*math.sinh(muon.eta())/muon.pt()
        B = mu**2*math.sinh(muon.eta())**2/muon.pt()**2
        C = (muon.E**2*met.pt()**2-mu**2)/muon.pt()**2
        discriminant = B-C
        solutions=[]
        if(discriminant<0):
            Pz = A+cmath.sqrt(B-C)
            Pz = Pz.real
            solutions.append(Pz)
        else:
            Pz = A+math.sqrt(B-C)
            solutions.append(Pz)
            Pz2 = A-math.sqrt(B-C)
            solutions.append(Pz2)
        return solutions

    def calculateTopMass(self, jets, met, muon):
        N_bjets = 0
        l_diff = 10.0
        Mt = -1.0
        B_jet = []
        if not isinstance(muon, FourMomentum): return -1
        solutions = self.neutrinoReconstruction(met, muon)
        if not solutions: return -1
        
        for x in range(len(jets)):
            if(jets[x].has_b_tag):
                N_bjets += 1
                B_jet.append(x)
            
        for sol in range(len(solutions)):
            lepton = FourMomentum(met.px, met.py, solutions[sol], math.sqrt(met.pt()**2+solutions[sol]**2))
            for x in range(len(jets)):
                if(N_bjets > 1):
                    if(not jets[x].has_b_tag): continue

                P_lep = lepton + muon + jets[x]
                Mt_lep = math.sqrt(P_lep*P_lep)
                
                for y in itertools.combinations(jets,3):
                    if jets[x] in y: continue
                    if N_bjets > 1 or (N_bjets is 1 and not jets[x].has_b_tag):
                        Contains_B_jet = False
                        for k in B_jet:
                            if jets[k] in y:
                                Contains_B_jet = True
                                break
                        if not Contains_B_jet: continue
                    P_had = functools.reduce(lambda a,b: a+b, y)
                    Mt_had = math.sqrt(P_had*P_had)
                    if(l_diff > abs(Mt_lep - Mt_had)):
                        l_diff = abs(Mt_lep - Mt_had)
                        Mt = (Mt_lep + Mt_had) / 2

                for y in itertools.combinations(jets,4):
                    if jets[x] in y: continue
                    if N_bjets > 1 or (N_bjets is 1 and not jets[x].has_b_tag):
                        Contains_B_jet = False
                        for k in B_jet:
                            if jets[k] in y:
                                Contains_B_jet = True
                                break
                        if not Contains_B_jet: continue
                    P_had = functools.reduce(lambda a,b: a+b, y)
                    Mt_had = math.sqrt(P_had*P_had)
                    if(l_diff > abs(Mt_lep - Mt_had)):
                        l_diff = abs(Mt_lep - Mt_had)
                        Mt = (Mt_lep + Mt_had) / 2

                for y in itertools.combinations(jets,5):
                    if jets[x] in y: continue
                    if N_bjets > 1 or (N_bjets is 1 and not jets[x].has_b_tag):
                        Contains_B_jet = False
                        for k in B_jet:
                            if jets[k] in y:
                                Contains_B_jet = True
                                break
                        if not Contains_B_jet: continue
                    P_had = functools.reduce(lambda a,b: a+b, y)
                    Mt_had = math.sqrt(P_had*P_had)
                    if(l_diff > abs(Mt_lep - Mt_had)):
                        l_diff = abs(Mt_lep - Mt_had)
                        Mt = (Mt_lep + Mt_had) / 2

        return Mt

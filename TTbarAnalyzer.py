from Analyzer import Analyzer
from uhhHists import DefaultHistograms, TopMassHist
from ROOT import TH1F
from TopReco import TopReco

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

##
        self.attach_histogram(TopMassHist(dataset_name+"_top_mass"), "top_mass")
        
        ##Creating the class that will reconstruct the top mass
        self.TopReconstruction = TopReco(10.0,3,6)
        #TopReco(x,y,z)
        # x = max allowed mass difference between leptonic and hadronic top quark
        # y = minimum number of jets used for reconstruction.
        # z = maximum number of jets used for reconstruction
        # y=z is possible.

        ## Here you can define your own variables ##
        self.n_total = 0.0

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

        ## Using some cuts for testing purposes ##
        if not event.n_muons() >= 1:
            return
        if not event.muons[0].pt() > 30.:
            return
        if not event.n_jets() > 2:
            return
        if not event.jets[0].pt() > 30:
            return
        if not event.n_b_jets() >= 1:
            return

        self.fill_histograms(event, "trigger")
        # only events fulfilling the "IsoMu24" trigger will be further processed

        ## Top Quark Reconstruction ##
        #mass = self.TopReconstruction.calculateTopMass(event.jets, event.met, event.muons[0])

        #if(mass > 0):
        #    event.top_mass = mass
        #    self.fill_histograms(event, "top_mass")

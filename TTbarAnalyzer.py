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
        self.TopReconstruction = TopReco(10.0,2,4)
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

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Exercise 1: MC / data comparisons
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        # Event selection:
        # check if event fulfills the "IsoMu24" trigger
        if not event.trigger["IsoMu24"]:
            return 
        # only events fulfilling the "IsoMu24" trigger will be further processed
        
        # fill histograms for all events passing the trigger selection
        self.fill_histograms(event, "trigger")

        # Have a look at your histograms and compare the different background samples.
        # Try to enrich the fraction of ttbar events by cutting on any of the distributions 
        # Plot all variables after every cut you introduce. Therefore define a new set of Histogramms at the top of this program 

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Exercise 2: Measurement of the ttbar production cross section
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        # Once you have optimized your event selection, define a variable in __init__ for the weighted number of selected events. 
        # Also, define a variable for the weighted number of generated events. With these numbers, 
        # the selection efficiency can be calculated. Afterwards, move to the 'Analysis.py' 
        # file to determine the efficiency and the ttbar cross section.

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Exercise 3: Reconstruction of the top quark mass
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        # Start off with a new event selection here
        # Decomment the following part to enable the top quark reconstruction.
        # Decomment the lines responsible for fitting the top mass in 'Analysis.py'. You may modify the variables x,y in fit(x,y)

        ## Top Quark Reconstruction ##
        #mass = self.TopReconstruction.calculateTopMass(event.jets, event.met, event.muons[0])

        #if(mass > 0):
        #    event.top_mass = mass
        #    self.fill_histograms(event, "top_mass")

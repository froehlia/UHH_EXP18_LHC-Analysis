from Analyzer import Analyzer
from uhhHists import DefaultHistograms

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
        self.attach_histogram(DefaultHistograms(dataset_name+"trigger"), "trigger")
        
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
        self.fill_histograms(event, "trigger")
        # only events fulfilling the "IsoMu24" trigger will be further processed

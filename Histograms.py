import ROOT
from collections import defaultdict

class Histograms(object):
    """
    A collection of histograms.
    """
    def __init__(self, name):
        self.name = name
        if not self.hists:
            self.hists = {}
        self.is_init = False
        self.initialize_histograms()

    def initialize_histograms(self):
        """
        Add collection name to histograms to avoid root overwriting
        histograms with same name.
        """
        # prevent to initialize histograms multiple times
        if self.is_init:
            raise ValueError("Histograms(): called initialize_histograms() on initialized histograms")
        for hist in self.hists.values():
            hist.SetName(self.name+"_"+hist.GetName())

    def fill(self, event):
        """
        Fill histograms.

        Has to be implemented by actual implemenation of Histograms.
        """
        raise NotImplementedError()
    
    

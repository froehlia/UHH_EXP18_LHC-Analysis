import ROOT
from EventBuilder import EventBuilder
from Event import Event
from collections import OrderedDict

class Analyzer(object):
    """
    Base class for analyzing datasets using the FPraktikum framework.
    """

    def __init__(self, dataset_name, file_name, event_options = {}):
        self.dataset_name = dataset_name
        self.file_name = file_name
        self.event_builder = EventBuilder(event_options)
        self.histograms = OrderedDict()
        self.working_dataset = None

    def attach_histogram(self, histogram, name):
        """
        Attatch a histogram to the analyzer.  

        The analyzer will call all attached histograms when
        fill_histograms is called.
        """
        self.histograms[name] = histogram

    def detach_histogram(self, name):
        """
        Detach a histogram from the analyzer.
        """
        self.histogram.remove(name)

    def fill_histograms(self, event, name):
        """
        Fill all attatched histograms.
        """
        self.histograms[name].fill(event)

    def run(self):
        """
        Loop over all datasets and process each event.
        """
        print "Start processing %s."% self.dataset_name
        f = ROOT.TFile.Open('files/'+self.file_name)
        n_event = 0
        for event_data in f.events:
            n_event += 1
            if n_event % 10000 == 0: print "%d events processed" % n_event
            # build event from TTree
            event = self.event_builder.build_event(event_data)
            # process event
            self.process(event)
        f.Close()
        print "Done. Processed %d events." % n_event
        self.write_output()

    def write_output(self):
        """
        Create new root file containing the histograms filled by the analyzer.
        """
        f = ROOT.TFile.Open('output_'+self.file_name, 'RECREATE')
        # write histograms
        for name in self.histograms.keys():
            tdir = f.mkdir(name)
            tdir.cd()
            for hist in self.histograms[name].hists.values():
                hist.Write()
        f.Close()

    def process(self, event):
        """
        The method is called for each event.
        Has to be implemented in derived classes.
        """
        raise NotImplementedError()


import ROOT
from collections import defaultdict

class Hists(object):
    def __init__(self,name):
        self.muon_pt = ROOT.TH1F(name+'_pt_muons', 'p_T [GeV]', 30, 0, 300)
        

    def fill(self,event):
        for muon in event.muons:
            self.muon_pt.Fill(muon.pt(), event.weight)

class Plotter(object):
    """
    A plotter to create sets of histograms
    """
    def __init__(self, dataset_names, hist_names):
        self.dataset_names = dataset_names
        self.hist_names = hist_names
        self.hists = defaultdict(dict)
        for dataset_name in dataset_names:
            for hist_name in hist_names:
                self.hists[dataset_name][hist_name] = Hists(hist_name)

        self.working_dataset = None
        # plotting styles for the different processes
        self.cosmetics = {'Data':{'marker_color':ROOT.kBlack},
                          'TTbar':{'fill_color':ROOT.kRed}
                          }

    def set_dataset(self,dataset_name):
        if dataset_name in self.dataset_names:
            self.working_dataset = dataset_name
        else:
            raise ValueError('Plotter.set_dataset(): dataset_name %s not in list of datasets' % dataset_name)

    def fill(self,event, hist_name):
        if hist_name in self.hist_names:
            self.hists[self.working_dataset][hist_name].fill(event)
        else:
            raise ValueError('Plotter.fill(): hist_name %s not in list of histograms' % hist_name)

    def plot(self):
        for dataset in self.dataset_names:
            for hist_name, hist in self.hists[dataset].iteritems():
                hist.muon_pt.Draw()

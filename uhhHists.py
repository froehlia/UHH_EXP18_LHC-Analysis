from Histograms import Histograms
from ROOT import TH1F

class DefaultHistograms(Histograms):
    """
    A default set of Histograms for the ttbar analysis.
    """
    def __init__(self, name):
        self.hists = {'muons_pt':     TH1F('muons_pt','p_{T,#mu} [GeV]', 60,0,300),
                      'muons_eta':    TH1F('muons_eta','#eta_{#mu}', 50,-5.0,5.0),
                      'muons_phi':    TH1F('muons_phi','#phi_{#mu}', 40,-3.2,3.2),
                      'muons_number': TH1F('muons_number','N_#mu', 11,-0.5,10.5),
                      'muon1_pt':     TH1F('muon1_pt','p_{T,#mu} [GeV]', 60,0,300),
                      'muon2_pt':     TH1F('muon2_pt','p_{T,#mu} [GeV]', 60,0,300)
                      }
        ## DO NOT TOUCH THIS PART ##
        name = name + "_default"
        super(DefaultHistograms, self).__init__(name)

    def fill(self, event):
        """
        Here the histograms are filled.
        """

        event_weight = event.weight
        
        # fill muon hists
        i_muon = 0
        for muon in event.muons:
            i_muon += 1
            # fill leading muon
            if i_muon == 1:
                self.hists['muon1_pt'].Fill(muon.pt(), event_weight)
            if i_muon == 2:
                self.hists['muon2_pt'].Fill(muon.pt(), event_weight)

            self.hists['muons_pt'].Fill(muon.pt(), event_weight)
            self.hists['muons_eta'].Fill(muon.eta(), event_weight)
            self.hists['muons_phi'].Fill(muon.phi(), event_weight)
        self.hists['muons_number'].Fill(event.n_muons(), event_weight)
        
        # other histograms go here

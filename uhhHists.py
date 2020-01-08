from Histograms import Histograms
from ROOT import TH1F

class DefaultHistograms(Histograms):
    """
    A default set of Histograms for the ttbar analysis.
    """
    def __init__(self, name):
        self.hists = {'muons_number': TH1F('muons_number','N_#mu', 11,-0.5,10.5),
                      'muon1_pt':     TH1F('muon1_pt','p_{T,#mu} [GeV]', 60,0,300),
                      'muon1_eta':    TH1F('muon1_eta','#eta_{#mu}', 50,-5.0,5.0),
                      'muon1_phi':    TH1F('muon1_phi','#phi_{#mu}', 40,-3.2,3.2),
                      'jets_number' : TH1F('jets_number', 'N_{jets}', 11, -0.5, 10.5),
                      'jet1_pt':      TH1F('jet1_pt','p_{T,jet} [GeV]', 60,0,300),
                      'jet1_eta':     TH1F('jet1_eta','#eta_{jet}', 50,-5.0,5.0),
                      'jet1_phi':     TH1F('jet1_phi','#phi_{jet}', 40,-3.2,3.2),
                      'jet2_pt':      TH1F('jet2_pt','p_{T,jet} [GeV]', 60,0,300),
                      'jet2_eta':     TH1F('jet2_eta','#eta_{jet}', 50,-5.0,5.0),
                      'jet2_phi':     TH1F('jet2_phi','#phi_{jet}', 40,-3.2,3.2),
                      'jet3_pt':      TH1F('jet3_pt','p_{T,jet} [GeV]', 60,0,300),
                      'jet3_eta':     TH1F('jet3_eta','#eta_{jet}', 50,-5.0,5.0),
                      'jet3_phi':     TH1F('jet3_phi','#phi_{jet}', 40,-3.2,3.2)
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
        self.hists['muons_number'].Fill(event.n_muons(), event_weight)
        if event.n_muons() >= 1:
            muon = event.muons[0]
            self.hists['muon1_pt'].Fill(muon.pt(), event_weight)
            self.hists['muon1_eta'].Fill(muon.eta(), event_weight)
            self.hists['muon1_phi'].Fill(muon.phi(), event_weight)

        
        # fill jet hists
        self.hists['jets_number'].Fill(event.n_jets())
        i_jet = 0
        for jet in event.jets:
            i_jet += 1
            if i_jet == 1:
                self.hists['jet1_pt'].Fill(jet.pt(), event_weight)
                self.hists['jet1_eta'].Fill(jet.eta(), event_weight)
                self.hists['jet1_phi'].Fill(jet.phi(), event_weight)
            elif i_jet == 2:
                self.hists['jet2_pt'].Fill(jet.pt(), event_weight)
                self.hists['jet2_eta'].Fill(jet.eta(), event_weight)
                self.hists['jet2_phi'].Fill(jet.phi(), event_weight)
            elif i_jet == 3:
                self.hists['jet3_pt'].Fill(jet.pt(), event_weight)
                self.hists['jet3_eta'].Fill(jet.eta(), event_weight)
                self.hists['jet3_phi'].Fill(jet.phi(), event_weight)
            elif i_jet > 3:
                break
        
        # other histograms go here

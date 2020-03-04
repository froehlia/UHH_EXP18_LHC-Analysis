import ROOT

class Fitter(object):

    def __init__(self, analyzer):
        self.top_hist = analyzer.histograms['top_mass'].hists['top_mass']
        self.mean = 0.0
        self.unc = 0.0

    def fit(self, fit_min, fit_max):
        c = ROOT.TCanvas()
        MyStyle = ROOT.TStyle("MyStyle1","My Root Style1");
        MyStyle.SetOptStat(0);
        MyStyle.SetOptFit(1);
        ROOT.gROOT.SetStyle("MyStyle1");
        self.top_hist.Draw()
        self.top_hist.Fit("gaus", "Q", "", fit_min, fit_max)
        fit = self.top_hist.GetFunction("gaus")
        self.mean = fit.GetParameter(1)
        self.unc = fit.GetParError(1)
        print('\n\n\n----------------------------------------------------------')
        output = 'Fitted top quark mass: ' + str(self.mean) + ' +- ' +  str(self.unc) + ' GeV\n\n'
        print(output)
        output = 'With ' + str(self.top_hist.GetEntries()) + ' top quark candidates'
        print(output)
        c.SaveAs("plots/ReconstructedTopMass.pdf")
        del c
        return self.top_hist

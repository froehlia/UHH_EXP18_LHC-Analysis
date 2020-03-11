import ROOT

class Fitter(object):

    def __init__(self, analyzers):
        self.top_hist_MC = 0
        self.top_hist = 0
        for x in analyzers:
            if(x == 'Data'):
                self.top_hist = analyzers[x].histograms['top_mass'].hists['top_mass']
            elif(self.top_hist_MC == 0):
                self.top_hist_MC = analyzers[x].histograms['top_mass'].hists['top_mass']
            else:
                self.top_hist_MC.Add(analyzers[x].histograms['top_mass'].hists['top_mass'])
        self.mean = 0.0
        self.unc = 0.0

    def fit(self, fit_min, fit_max):
        MyStyle = ROOT.TStyle("MyStyle1","My Root Style1")
        MyStyle.SetOptStat(0)
        MyStyle.SetOptFit(1)
        MyStyle.SetOptLogy(False)
        ROOT.gROOT.SetStyle("MyStyle1")
        if(not self.top_hist == 0):
            c = ROOT.TCanvas()
            self.top_hist.Draw()
            self.top_hist.Fit("gaus", "Q", "", fit_min, fit_max)
            fit = self.top_hist.GetFunction("gaus")
            self.mean = fit.GetParameter(1)
            self.unc = fit.GetParError(1)
            print('\n\n\n----------------------------------------------------------')
            output = 'Fitted top quark mass in data: ' + str(self.mean) + ' +- ' +  str(self.unc) + ' GeV\n\n'
            print(output)
            output = 'With ' + str(self.top_hist.GetEntries()) + ' top quark candidates'
            print(output)
            c.SaveAs("plots/ReconstructedTopMass.pdf")
            del c

        c = ROOT.TCanvas()
        self.top_hist_MC.Draw()
        self.top_hist_MC.Fit("gaus", "Q", "", fit_min, fit_max)
        fit = self.top_hist_MC.GetFunction("gaus")
        self.mean = fit.GetParameter(1)
        self.unc = fit.GetParError(1)
        print('\n\n\n----------------------------------------------------------')
        output = 'Fitted top quark mass in Monte Carlo: ' + str(self.mean) + ' +- ' +  str(self.unc) + ' GeV\n\n'
        print(output)
        output = 'With ' + str(self.top_hist_MC.GetEntries()) + ' top quark candidates\n'
        print(output)
        c.SaveAs("plots/ReconstructedTopMass_MC.pdf")
        del c
        return self.top_hist_MC

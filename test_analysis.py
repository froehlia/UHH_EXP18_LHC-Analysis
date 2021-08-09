from TTbarAnalyzer import TTbarAnalyzer
from Plotter import Plotter
from collections import OrderedDict
from Fitter import Fitter

if __name__ == "__main__":
    """
    Test Analysis to check if the framework runs properly
    """

    print "Staring test analysis..."
    datasets = OrderedDict([('Data', 'data.root'),
                                ('QCD', 'qcd.root'),
                                ('Diboson', 'diboson.root'),
                                ('DY+jets', 'dy.root'),
                                ('single top', 'single_top.root'),
                                ('TTbar', 'ttbar.root'), 
                                ('W+jets', 'wjets.root'), ])

    event_options = {'JEC': 'nominal',
                     'muon_isolation': 0.1,
                     'max_events':10
                     }
    analyzers = OrderedDict()
    for name, file_name in datasets.iteritems():
        analyzer = TTbarAnalyzer(name, file_name, event_options)
        # run analysis for dataset
        analyzer.run()
        analyzers[name] = analyzer

    plotter = Plotter(analyzers)
    plotter.process()

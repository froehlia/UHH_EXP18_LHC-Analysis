from TTbarAnalyzer import TTbarAnalyzer
from Plotter import Plotter
from collections import OrderedDict
from Fitter import Fitter

if __name__ == "__main__":
    #only run over TTbar for debugging and run over everything to get results
    run_all = False
    if run_all:
        datasets = OrderedDict([('Data', 'data.root'),
                                ('QCD', 'qcd.root'),
                                ('Diboson', 'diboson.root'),
                                ('DY+jets', 'dy.root'),
                                ('single top', 'single_top.root'),
                                ('TTbar', 'ttbar.root'), 
                                ('W+jets', 'wjets.root'),
        ]
        )
    else:
        datasets = OrderedDict([('TTbar', 'ttbar.root'), 
        ]
        )

    event_options = {'JEC': 'nominal',
                     'muon_isolation': 0.1
                     }
    analyzers = OrderedDict()
    for name, file_name in datasets.iteritems():
        analyzer = TTbarAnalyzer(name, file_name, event_options)
        # run analysis for dataset
        analyzer.run()
        analyzers[name] = analyzer

    plotter = Plotter(analyzers)
    plotter.process()

    ## fitting the top mass ##
    if run_all:
        fitter = Fitter(analyzers['Data'])
        fitter.fit(130., 210.)
        # fitter.fit(x,y)
        # (x,y) = fit range
    else:
        fitter = Fitter(analyzers['TTbar'])
        fitter.fit(130., 210.)

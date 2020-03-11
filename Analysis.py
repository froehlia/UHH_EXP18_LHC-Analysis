from TTbarAnalyzer import TTbarAnalyzer
from Plotter import Plotter
from collections import OrderedDict
from Fitter import Fitter

if __name__ == "__main__":
    #run_all = True to run over both data and monte carlo.
    #run_all = False to only run over monte carlo. Useful to save time while debugging and testing.
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
        datasets = OrderedDict([('QCD', 'qcd.root'),
                                ('Diboson', 'diboson.root'),
                                ('DY+jets', 'dy.root'),
                                ('single top', 'single_top.root'),
                                ('TTbar', 'ttbar.root'), 
                                ('W+jets', 'wjets.root'),
        ]
        )

    event_options = {'JEC': 'nominal',
                     'muon_isolation': 0.1
                     }

    analyzers = OrderedDict()
    #running analysis over all datasets.
    for name, file_name in datasets.iteritems():
        analyzer = TTbarAnalyzer(name, file_name, event_options)
        analyzer.run()
        analyzers[name] = analyzer

    # +++++++++++++++++++++++++++++++++++++++++++
    # Exercise 2: Measurement of the cross section
    # +++++++++++++++++++++++++++++++++++++++++++
    #Access variables from TTbarAnalyzer like this:
    print analyzers['TTbar'].n_total
    n_background_total = sum([an.n_total for key, an in analyzers.iteritems() if not (key == 'Data' or key == 'TTbar')])

    #plotting the output
    plotter = Plotter(analyzers)
    plotter.process()

    #fitting the top mass
    #fitter = Fitter(analyzers)
    #fitter.fit(130., 210.)
    # fitter.fit(x,y)
    # (x,y) = fit range

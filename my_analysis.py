from TTbarAnalyzer import TTbarAnalyzer
from Plotter import Plotter
from collections import OrderedDict
from Fitter import Fitter

if __name__ == "__main__":
    """
    Main analysis script. Here you run the analysis and evaluate the results.
    """

    #run_all = True to run both data and Monte Carlo simulation.
    #run_all = False to only run the Monte Carlo simulation. Use this as you default for the design and optimization of the analysis.
    run_all = False

    # List of datasets to be analyzed
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

    # Options for the event builder
    event_options = {'JEC': 'nominal', # Jet Energy corrections: change to "up" or "down" to evaluate the systematic uncertainties
                     'muon_isolation': 0.1 # muon isolation, you can leave this at the default value
                     }

    analyzers = OrderedDict()

    # Analyze all datasets:
    for name, file_name in datasets.items():
        analyzer = TTbarAnalyzer(name, file_name, event_options) # create an Analyzer for each dataset
        analyzer.run() # run the Analyzer
        analyzers[name] = analyzer # store the results


    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Exercise 2: Measurement of the ttbar production cross section
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # You can access variables from TTbarAnalyzer like this:
    n_ttbar = analyzers['TTbar'].n_total # get total number of ttbar events
    print("Total Number of ttbar events: {0}".format(n_ttbar)) # write to the console
    n_background_total = sum([an.n_total for key, an in analyzers.items() if not (key == 'Data' or key == 'TTbar')]) # Sum total number of all events, except data and ttbar
    print("Total Number of background events: {0}".format(n_background_total))

    # Plot all histograms filled in the Analysis
    plotter = Plotter(analyzers)
    plotter.process()

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Exercise 3: Reconstruction of the top quark mass
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Run the fit of the top mass distribution
    #fitter = Fitter(analyzers)
    #fitter.fit(130., 210.)
    # fitter.fit(x,y)
    # (x,y) = fit range

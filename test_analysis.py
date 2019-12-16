from TTbarAnalyzer import TTbarAnalyzer


if __name__ == "__main__":
    datasets = {'TTbar': 'ttbar.root'}

    event_options = {'JEC': 'nominal',
                     'muon_isolation': 0.1
                     }
    
    analyzers = {}
    for name, file_name in datasets.iteritems():
        analyzer = TTbarAnalyzer(name, file_name, event_options)
        # run analysis for dataset
        analyzer.run()
        analyzers[name] = analyzer

    print analyzers['TTbar'].n_total

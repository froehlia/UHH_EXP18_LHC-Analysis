import ROOT
from EventBuilder import EventBuilder
from Event import Event
from Plotter import Plotter

def process(event, plotter):
    """
    This function is run for each event.
    The event selection and mass reconstruction is done here.
    Histogramms can be filled at each step using Plotter.fill(event, <hist_name>).
    """
    # Fill initial Histogramm
    plotter.fill(event, "no_cuts")
    
    # Select events fulfilling the "IsoMu24" trigger
    if not event.trigger['IsoMu24']:
        return
    plotter.fill(event, "trigger_selection")

if __name__=="__main__":
    """
    This is the main analysis file.
    """
    # list of input files
    # root_files = {'Data':'data.root', 'Z+jets':'dy.root', 'Multijet':'qcd.root', 'Single Top':'single_top.root', 'TTbar':'ttbar.root', 'W+jets':'wjets.root', 'WW':'ww.root', 'WZ':'wz.root', 'ZZ':'zz.root'}
    root_files = {'TTbar':'ttbar.root'}
    dataset_names = [key for key in root_files.keys()]
    # Setup event builder
    event_options = {'JEC':'nominal'} # variation of Jet Energy Corrections (JEC) nominal, up, down
    event_builder = EventBuilder(event_options)

    # Set Histograms here:
    hist_names = ['no_cuts',
                  'trigger_selection'
                  ]

    plotter = Plotter(dataset_names, hist_names) # need to implement
    for sample_name, root_file in root_files.iteritems():
        f = ROOT.TFile.Open('files/'+root_file)
        plotter.set_dataset(sample_name)
        for event_data in f.events:
            # build event from TTree
            event = event_builder.build_event(event_data)
            # process event
            process(event, plotter)
        f.Close()
        plotter.plot()
        raw_input("done...")

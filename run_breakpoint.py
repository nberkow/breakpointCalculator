from BreakpointPlotMaker import BreakpointPlotMaker
from PartitionFinder import PartitionFinder

if __name__ == "__main__":
    pf = PartitionFinder()

    params = {
        "mr1"    : 1/(-1),   # lower MIC breakpoint
        "mr2"    :  1/(1),   # upper MIC breakpoint
        "M1"     :  4,   # weight for very major error penalty
        "VM1"    :  4,   # weight for major error penalty
        "m1"     :  1,   # weight for minor error penalty
        "M2"     :  20,  # 
        "VM2"    :  20,  # corresponding values for errors that occur outside one dilution of the intermediate
        "m2"     :  8,   # 
        "delim"  : ","   # infile delimiter
    }

    pf.params = params
    pf.load_file("data1.csv")
    #pf.scan_breakpoints()
    print(pf.compute_succeptability_categories(35.0, 39.0))

    bpm = BreakpointPlotMaker()
    desnity_plot = bpm.make_desnity_plot(pf.get_density_grid())



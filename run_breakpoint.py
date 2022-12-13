from BreakpointInputHandler import BreakpointInputHandler
from PartitionFinder import PartitionFinder

if __name__ == "__main__":

    input_handler = BreakpointInputHandler()
    input_handler.load_file("data1.csv")
    

    params = {
        "mr1"    : -1,   # lower MIC breakpoint
        "mr2"    :  1,   # upper MIC breakpoint
        "M1"     :  4,   # weight for very major error penalty
        "VM1"    :  4,   # weight for major error penalty
        "m1"     :  1,   # weight for minor error penalty
        "M2"     :  20,  # 
        "VM2"    :  20,  # corresponding values for errors that occur outside one dilution of the intermediate
        "m2"     :  8,   # 
        "delim"  : ","   # infile delimiter
    }

    pf = PartitionFinder(params)
    a, b = 34, 39
    
    counts = pf.compute_succeptability_categories(input_handler.value_pairs, a, b)
    for c in counts:
        print(f"{c}\t{counts[c]}")


    #bpm = BreakpointPlotMaker()
    #desnity_plot = bpm.make_desnity_plot(pf.get_density_grid())



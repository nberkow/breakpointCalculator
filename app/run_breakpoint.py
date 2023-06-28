from BreakpointInputHandler import BreakpointInputHandler
from PartitionFinder import PartitionFinder
import sys

if __name__ == "__main__":

    params = {
        "mr1"     : -1,   # lower MIC breakpoint
        "mr2"     :  1,   # upper MIC breakpoint
        "weights" :  {    # weights for minor, major and very major errors
            "r":{"m" : 1, "M" : 4, "VM" : 4},   # within one range
            "R":{"m" : 8, "M" : 20, "VM" : 20}  # more extreme error
        },
        "bzk_a"   : .8,
        "delim"   : ","   # infile delimiter
    }

    input_handler = BreakpointInputHandler(params)
    input_handler.load_file(sys.argv[1])

    pf = PartitionFinder(params, input_handler)
    breakpoints_by_score = pf.score_all_breakpoints()
    
    s = sorted(list(breakpoints_by_score.keys()))
    for score in s[0:3]:
        for p in breakpoints_by_score[score]:
            print(f"{score}\t{p[0]}\t{p[1]}\t{p[2]}\t{p[3]}")

  


    #bpm = BreakpointPlotMaker()
    #desnity_plot = bpm.make_desnity_plot(pf.get_density_grid())



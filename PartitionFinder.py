import sys
import math

class PartitionFinder:

    """
    Find the dilution breakpoints for a disc diffusion resistance experiment

    main inputs: 
        - 2 column data sets with paired "MIC" (gold standard) and "DIA" (experimental) values
        - two thresholds (breakpoints) for susceptability and resistance

    outputs:
        - 2 DIA breakpoint values corresponding to the 2 MIC values
        - scatterplot data
    
    """

    def __init__(self):

        self.params = {}
        

        self.mic = []
        self.dia = []
        
        self.val_pair_counts = {} # keep track of the number of times a dia/mic pair occurs

    def load_file(self, path):

        transform_mic = False
        with open(path) as mic_dia_file:
            mic_dia_file.readline()
            for md in mic_dia_file:
                m, d = md.rstrip().split(self.params['delim'])
                m = float(m)
                if transform_mic:
                    m = 1/(2**m)
                d = float(d)
                self.mic.append(m)
                self.dia.append(d)
                if not (m,d) in self.val_pair_counts:
                    self.val_pair_counts[(m,d)] = 0
                self.val_pair_counts[(m,d)] += 1

    def compute_succeptability_categories(self, zr, zs):

        """
        There are 9 succeptability categories based on MIC and DIA
        they come from the possible combinations of MIC and DIA.

        for example if the MIC value is less than the lower MIC breakpoint:

            MIC < mr1
        
        and the the DIA is less than zs, some breakpoint value being tested

            DIA < zr

        then both values agree that the classification is "resisistant"

        when they disagree, the classification is a major error, minor error or very major error

        """

        scores = {
            "resistant"        : 0,
            "susceptible"      : 0,
            "very_major_error" : 0,  # false susceptible
            "major_error"      : 0,  # false resistant
            "minor_error"      : 0   # one reading is resistant or susceptible, the other is intermediate
        }

        mic_range = self.params['mr2'] - self.params['mr1'] 

        for i in range(len(self.mic)):
            mic_val = self.mic[i]
            dia_val = self.dia[i]

            if mic_val + mic_range <= self.params['mr1'] or mic_val - mic_range > self.params['mr2']:
                w_m = self.params['m2']
                w_M = self.params['M2']              
                w_VM = self.params['VM2']
            else:
                w_m = self.params['m1']
                w_M = self.params['M1']              
                w_VM = self.params['VM1']

            # susceptible according to MIC
            if mic_val > self.params['mr2']:
            

                #print(f"{mic_val}\t{dia_val}\tS")

                # agree on susceptible
                if dia_val <= zr:
                    scores["susceptible"] += 1

                # minor error
                elif dia_val > zr and dia_val <= zs:
                    scores["minor_error"] += w_m

                # false resistant
                elif dia_val > zs:
                    scores["major_error"] += w_M

            # intermediate according to MIC
            elif mic_val > self.params['mr1'] and mic_val <= self.params['mr2']:

                #print(f"{mic_val}\t{dia_val}\tI")

                # minor error
                if dia_val <= zr:
                    scores["minor_error"] += w_m

                # agree on intermediate (not used in calc)
                elif dia_val > zr and dia_val <= zs:
                    pass

                # minor error
                elif dia_val > zs:
                    scores["minor_error"] += w_m

            # resistant according to MIC
            elif mic_val <= self.params['mr1']:

                #print(f"{mic_val}\t{dia_val}\tR")

                # false susceptible
                if dia_val <= zr:
                    scores["very_major_error"] += w_VM

                # minor error
                elif dia_val > zr and dia_val <= zs:
                    scores["minor_error"] += w_m

                # agree on resistant
                elif dia_val > zs:
                    scores["resistant"] += 1
            
        return(scores)

    def scan_breakpoints(self):

        # get a unique sorted list of possible breakpoints
        candidate_breakpoints = sorted(list(set(self.dia)))
        n = len(candidate_breakpoints)

        best_index = math.inf
        best_pair = (0, 0)

        # get the error breakdown for every pair
        for i in range(n-1):
            for j in range(i + 1, n):
                scores = self.compute_succeptability_categories(candidate_breakpoints[i], candidate_breakpoints[j])
                breakpoint_index = scores["very_major_error"] + scores["major_error"] + scores["minor_error"]

                if breakpoint_index < best_index:
                    best_pair = (candidate_breakpoints[i], candidate_breakpoints[j])
                    best_index = breakpoint_index
        print(best_pair)

    def get_density_grid(self):

        mic_val_range =  sorted(list(set(self.mic)))
        dia_val_range =  sorted(list(set(self.dia)))
        grid = []
        
        #for k in self.val_pair_counts:
        #    print(f"{k[0]}\t{k[1]}\t{self.val_pair_counts[k]}")

        i = 0
        mic_val_range.reverse()
        for m in mic_val_range:
            grid.append([])
            for d in dia_val_range:

                if (m,d) in self.val_pair_counts:
                    grid[i].append(self.val_pair_counts[(m,d)])
                else:
                    grid[i].append('')
            i+=1
            
        return(grid, mic_val_range, dia_val_range)

        


        

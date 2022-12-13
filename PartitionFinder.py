import sys
import math

class PartitionFinder:

    """
    Find the dilution breakpoints for a disc diffusion resistance experiment

    main inputs: 
        - 2 column data sets with paired "MIC" (gold standard) and "DIA" (clinical) values
        - two MIC thresholds (breakpoints) for susceptability and resistance

    outputs:
        - 2 DIA breakpoint values corresponding to the 2 MIC values
    
    """

    def __init__(self, params):

        self.params = params


    def compute_succeptability_categories(self, score_pairs, dia_br1, dia_br2):

        """
        input:
        -   score_pairs: dictionary of MIC, DIA score pairs. Values are counts for that pair
        -   dia_br1: lower DIA breakpoint
        -   dia_br2: upper DIA breakpoint

        The MIC breakpoints are also required to be set in self.params

        output:
        -   category_counts: dict of all possible zones. values are counts of
        points falling into each zone.

        description:
            The MIC and DIA breakpoints divide the data into 9 zones.

                            DIA
            MIC             S | I | R     
            susceptible     x |   |
            intermediate      | x |
            resistant         |   | x 

            Additionally, scores are weighted differently depending on how far outside 
            of the expected zone they fall. Count them separately if they are off
            by more than the width of the intermediate zone.
        """

        category_counts = {}

        mic_range = self.params['mr2'] - self.params['mr1'] - 1

        for p in score_pairs:
            mic_val, dia_val = p
            score_pair_count = score_pairs[p]
            weight_type = "r" # within one MIC range, R for outside

            # susceptible according to MIC
            mic_prefix = "ERR"
            if mic_val >= self.params['mr2']:
                mic_prefix = 'S'
                if mic_val >= (self.params['mr2'] + mic_range):
                    weight_type = 'R'

            # intermediate according to MIC
            elif mic_val > self.params['mr1'] and mic_val <= self.params['mr2']:
                mic_prefix = 'I'

            # resistant according to MIC
            elif mic_val <= self.params['mr1']:
                mic_prefix = 'R'
                if mic_val <= (self.params['mr1'] - mic_range):
                    weight_type = 'R'

            # susceptible according to DIA
            dia_prefix = "ERR"
            if dia_val <= dia_br1:
                dia_prefix = 'S'

            # intermediate according to DIA
            elif dia_val > dia_br1 and dia_val < dia_br2:
                dia_prefix = 'I'

            # resistant according to DIA
            elif dia_val >= dia_br2:
                dia_prefix = 'R'

            category = (mic_prefix, dia_prefix, weight_type)
            if not category in category_counts:
                category_counts[category] = 0    
            category_counts[category] += score_pair_count

        return(category_counts)         

  
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

        


        

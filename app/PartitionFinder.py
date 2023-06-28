import sys
import math

class PartitionFinder:

    def __init__(self, params, input_handler):

        self.params = params
        self.input_handler = input_handler

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
            mic_call = "ERR"
            if mic_val >= self.params['mr2']:
                mic_call = 'S'
                if mic_val >= (self.params['mr2'] + mic_range):
                    weight_type = 'R'

            # intermediate according to MIC
            elif mic_val > self.params['mr1'] and mic_val <= self.params['mr2']:
                mic_call = 'I'

            # resistant according to MIC
            elif mic_val <= self.params['mr1']:
                mic_call = 'R'
                if mic_val <= (self.params['mr1'] - mic_range):
                    weight_type = 'R'

            # susceptible according to DIA
            dia_call = "ERR"
            if dia_val <= dia_br1:
                dia_call = 'S'

            # intermediate according to DIA
            elif dia_val > dia_br1 and dia_val < dia_br2:
                dia_call = 'I'

            # resistant according to DIA
            elif dia_val >= dia_br2:
                dia_call = 'R'

            category = (mic_call, dia_call, weight_type)
            if not category in category_counts:
                category_counts[category] = 0    
            category_counts[category] += score_pair_count

        return(category_counts) 

    
    def score_all_breakpoints(self):

        range_min = min(self.input_handler.dia_names)
        range_max = max(self.input_handler.dia_names)
        breakpoints_by_score = {}

        for i in range(range_min, range_max - 1):
            for j in range(i + 1, range_max):
                category_counts = self.compute_succeptability_categories(self.input_handler.value_pairs, i, j)
                index_vals = self.calculate_index_vals(category_counts, i, j)
                if not index_vals['max_err'] in breakpoints_by_score:
                    breakpoints_by_score[index_vals['max_err']] = []
                breakpoints_by_score[index_vals['max_err']].append((i, j, index_vals['FS'], index_vals['FR']))

        return(breakpoints_by_score)


    def calculate_index_vals(self, category_counts, dia_br1, dia_br2):

        """
        input: category counts - a dict containing the number of data points that fall 
        into each zone 

        output: index_data - an index is a summary of goodness of fit for a particular
        set of breakpoint values. There is more than one proposed index and they are
        similar. Calculate index by a few methods and return them all in a dict.
        
        """

        index_data = {
            "S"   : 0,
            "R"   : 0,
            "I"   : 0,
            "total" : 0,
            "range" :  dia_br2 - dia_br1,
            "minor_error" : 0,
            "major_error" : 0,
            "very_major_error" : 0,
            "dBETS"            : 0,  # dBETs scoring behavior
            "BZK"              : 0,  # naive scoring from Brunden, Zurenko, and Kapik (1992)
            "BZK_weighted"     : 0,  # BZK with major and minor weights (a + b = 1)
            "max_err"          : 0   # max(false R / all S, false S / all R) + min/2 + (minor error / all data)**2  
        }

        for category in category_counts:
            mic_call, dia_call, weight_type = category
            weights = self.params["weights"][weight_type]

            # track totals
            index_data[mic_call] += category_counts[category]
            index_data["total"] += category_counts[category]

            if mic_call == 'R':
                if dia_call == 'S':
                    index_data["very_major_error"] += category_counts[category] # false succeptible
                    index_data["dBETS"] += weights["VM"] * category_counts[category]
                    
                elif dia_call == 'I':
                    index_data["minor_error"] += category_counts[category]
                    index_data["dBETS"] += weights["m"] * category_counts[category]

            elif mic_call == 'S':
                if dia_call == 'R':
                    index_data["major_error"] += category_counts[category] # false resistant
                    index_data["dBETS"] += weights["VM"] * category_counts[category]
                elif dia_call == 'I':
                    index_data["minor_error"] += category_counts[category]
                    index_data["dBETS"] += weights["m"] * category_counts[category]

            elif mic_call == "I":
                index_data["minor_error"] += 1
                index_data["dBETS"] += weights["m"]

        # all scores adjusted so that lower = less error

        # dBETs - scores based on a tiered weighting system
        index_data["dBETS"] # calculated in the above loop

        # BZK scores based on total error and range size
        index_data['BZK'] = 1 / (index_data['range'] / ((index_data["minor_error"] + index_data["major_error"] + index_data["very_major_error"]) / index_data["total"]))
        
        # weighted BZK scores increase the impact of major and very major errors
        em = (index_data["minor_error"] * (1 - self.params["bzk_a"]))
        eM = ((index_data["major_error"] + index_data["very_major_error"]) * self.params["bzk_a"])
        index_data['BZK_weighted'] = 1 / (index_data['range'] / ((em + eM) / index_data["total"]))

        # index based on the max (worst) of major and very major error. minor error is a small term
        index_data["FS"] = index_data["very_major_error"] / index_data["R"]
        index_data["FR"] = index_data["major_error"] / index_data["S"]
        index_data["max_err"] = max(index_data["FS"], index_data["FR"]) + (index_data["minor_error"]/index_data["total"])**2

        return(index_data)

        

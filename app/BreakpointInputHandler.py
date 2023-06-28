import sys

class BreakpointInputHandler:

    def __init__(self, params):

        self.params = params

        # all unique pairs of MIC/DIA values counted
        self.value_pairs = {}

        # dash plotting data stuctures
        self.grid = []
        self.columns = []

        # row and column names
        self.dia_names = set()
        self.mic_names = set()

    def read_scores(self, csv_scores):

        for md in csv_scores.split("\n")[1:]:
            if self.params['delim'] in md:
                m, d = md.rstrip().split(self.params['delim'])
                m = int(m)
                d = int(d)

                self.mic_names.add(m)
                self.dia_names.add(d)

                if not (m, d) in self.value_pairs:
                    self.value_pairs[(m, d)] = 0
                self.value_pairs[(m, d)] += 1
        
        self.make_dash_grid_data()

    def load_file(self, path):

        with open(path) as mic_dia_file:
            mic_dia_file.readline() # skip the header

            for md in mic_dia_file:
                if self.params['delim'] in md:
                    m, d = md.rstrip().split(self.params['delim'])
                    m = int(m)
                    d = int(d)

                    self.mic_names.add(m)
                    self.dia_names.add(d)

                    if not (m, d) in self.value_pairs:
                        self.value_pairs[(m, d)] = 0
                    self.value_pairs[(m,d)] += 1

        self.make_dash_plot_data()

    def make_dash_grid_data(self):

        self.columns = [{"name":"", "id":"MIC"}]  # start with just the leftmost column
        
        if len(self.value_pairs) > 0:

            for d in range(min(self.dia_names), max(self.dia_names) + 1):
                
                self.columns.append({"name":str(d), "id":str(d)})

            for m in reversed(list(range(min(self.mic_names), max(self.mic_names)+1))):
                row = {"MIC":str(m)}
                for d in range(min(self.dia_names), max(self.dia_names) + 1):
                    col_name = str(d)
                    v = None
                    if (m,d) in self.value_pairs:
                        v = self.value_pairs[(m,d)]
                    row[col_name] = v
                self.grid.append(row)

        else:
            print("Load file before making plot data")
            sys.exit()
                        

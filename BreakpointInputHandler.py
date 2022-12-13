class BreakpointInputHandler:

    def __init__(self):
        self.value_pairs = {}
        self.grid = []
        self.columns = [{"name":"", "id":"MIC"}]  # start with just the leftmost column
        self.dia_names = set()
        self.mic_names = set()
        self.delim = ","

    def load_file(self, path):

        with open(path) as mic_dia_file:
            mic_dia_file.readline() # skip the header

            for md in mic_dia_file:
                m, d = md.rstrip().split(self.delim)
                m = int(m)
                d = int(d)

                self.mic_names.add(m)
                self.dia_names.add(d)

                if not (m, d) in self.value_pairs:
                    self.value_pairs[(m, d)] = 0
                self.value_pairs[(m,d)] += 1

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
                    

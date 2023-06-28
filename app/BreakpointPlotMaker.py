import plotly.express as px
from dash import Dash, dash_table

class BreakpointPlotMaker:

    def __init__(self, params):
        self.params = params

    def build_table(self, input_handler, breakpoints_by_score):

        k = sorted(list(breakpoints_by_score.keys()))
        br1, br2, fs, fr = breakpoints_by_score[k[0]][0]

        br_col_names = {"S" : [], "I" : [], "R" : []}
        for c in input_handler.columns[1:]:
            if int(c["id"]) < br1:
                br_col_names["S"].append(c["id"])
            elif int(c["id"]) >= br1 and int(c["id"]) <= br2:
                br_col_names["I"].append(c["id"])
            elif int(c["id"]) > br2:
                br_col_names["R"].append(c["id"])

        idx = 0 
        br_row_idx = {"S" : [], "I" : [], "R" : []}
        for row in input_handler.grid:
            if int(row["MIC"]) > self.params["mr2"]:
                br_row_idx["S"].append(idx)
            elif int(row["MIC"]) <= self.params["mr2"] and int(row["MIC"]) >= self.params["mr1"]:
                br_row_idx["I"].append(idx)
            elif int(row["MIC"]) < self.params["mr1"]:
                br_row_idx["R"].append(idx)
            idx += 1

        header_formatting = [
            {'if': 
                {'column_id': br_col_names["S"]},
            'backgroundColor': "tomato",
            'color': "white"},
            {'if': 
                {'column_id': br_col_names["I"]},
            'backgroundColor': "yellow",
            'color': "blue"},
            {'if': 
                {'column_id': br_col_names["R"]},
            'backgroundColor': "blue",
            'color': "white"}
        ]
        
        table = dash_table.DataTable(
            columns=input_handler.columns,
            data=input_handler.grid,
            style_data_conditional=[
                {
                    'if': {
                        'column_id': 'MIC',
                    },
                    'backgroundColor': 'yellow',
                    'color': 'blue'
                },
                {
                'if': {
                    'filter_query': '{MIC} > ' + str(self.params['mr2']),
                    'column_id': 'MIC'
                    },
                    'backgroundColor': 'tomato',
                    'color': 'white'
                },
                {
                'if': {
                    'filter_query': '{MIC} < ' + str(self.params['mr1']),
                    'column_id': 'MIC'
                    },
                    'backgroundColor': 'blue',
                    'color': 'white'
                },
                {
                'if' : {
                    'column_id': br_col_names["S"],
                    'row_index': br_row_idx["R"]
                    },
                    'backgroundColor': 'pink',
                    'color' : 'red'
                },
                {
                'if' : {
                    'column_id': br_col_names["R"],
                    'row_index': br_row_idx["S"]
                    },
                    'backgroundColor': 'pink',
                    'color' : 'red'
                },
                {
                'if' : {
                    'column_id': br_col_names["I"],
                    'row_index': br_row_idx["S"] + br_row_idx["R"]
                    },
                    'backgroundColor': 'lightgrey',
                    'color' : 'orange'
                },
                {
                'if' : {
                    'column_id': br_col_names["S"] + br_col_names["R"],
                    'row_index': br_row_idx["I"]
                    },
                    'backgroundColor': 'lightgrey',
                    'color' : 'orange'
                }
            ],
            style_header_conditional=header_formatting
        )
        return(table)

    def build_plot(self, input_handler, breakpoints_by_score):

        key_list = sorted(list(breakpoints_by_score.keys()))

        # chosen breakpoints 
        x = []
        y = []
        s = []

        for k in key_list:
            for bp in breakpoints_by_score[k]:
                br1, br2, fs, fr = bp
                x.append(br2)
                y.append(br1)
                s.append(k**-1)

        plot = px.scatter(x=x, y=y, color=s, color_continuous_scale="blues", 
            labels=dict(x="Resistant Breakpoint", y="Senstive Breakpoint", color="Fit Quality"))
        return(plot)




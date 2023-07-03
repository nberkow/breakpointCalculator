from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import io
import base64
import plotly.express as px

from BreakpointInputHandler import BreakpointInputHandler
from BreakpointPlotMaker import BreakpointPlotMaker
from PartitionFinder import PartitionFinder

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

slider = dcc.RangeSlider( id='mic-range-slider', step=1,
    min=-10, max=10, value=[params["mr1"], params["mr2"]])

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div([
        html.Div(html.Img(src="assets/breakpoint_logo.png"), style={'display': 'inline-block'}),
        html.Div(html.H1("Resistance Calculator"), style={'display': 'inline-block'})]),
        dcc.Markdown(open("assets/text1.md").read()),
        html.A("data1.csv", href="assets/data1.csv"),
        dcc.Upload(
            id='upload-file',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '50%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
        multiple=False),
        dcc.Markdown(open("assets/text2.md").read()),
        html.Div(id='table-container'),
        dcc.Markdown(open("assets/text3.md").read()),
        dcc.Graph(id='scatter-plot'),
        dcc.Markdown(open("assets/text4.md").read()),       
        dcc.Markdown(open("assets/text5.md").read()),
        slider,
        dcc.Markdown(open("assets/text6.md").read())
        ])

@app.callback([
    Output('table-container', 'children'), 
    Output('scatter-plot', 'figure')],
    [
    Input('upload-file', 'contents'),
    Input('mic-range-slider', 'value')])
def show_table_plot_and_slider(contents, value):

    if contents:
        content_type, content_string = contents.split(',')

        decoded = base64.b64decode(content_string)
        csv_scores = decoded.decode('utf-8')

        input_handler = BreakpointInputHandler(params)
        input_handler.read_scores(csv_scores)     

        params['mr1'] = value[0]
        params['mr2'] = value[1]   

        slider = dcc.RangeSlider(id='mic-range-slider', 
            min=min(input_handler.mic_names), max=max(input_handler.mic_names), step=1,
            value=[params["mr1"], params["mr2"]])

        table, plot = make_table_and_plot(input_handler)
        
        return([[table], plot])

    plot = px.scatter(x=[0,1],y=[0,1])
    return([[],plot])


def make_table_and_plot(input_handler):

    pf = PartitionFinder(params, input_handler)
    breakpoints_by_score = pf.score_all_breakpoints()

    plot_maker = BreakpointPlotMaker(params)
    breakpoint_table = plot_maker.build_table(input_handler, breakpoints_by_score)
    breakpoint_plot = plot_maker.build_plot(input_handler, breakpoints_by_score)
    return([breakpoint_table, breakpoint_plot])

#if __name__ == '__main__':
#    app.run_server(debug=True)

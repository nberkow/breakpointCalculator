from dash import Dash, dash_table

from BreakpointInputHandler import BreakpointInputHandler

input_handler = BreakpointInputHandler()
input_handler.load_file("mini_test.csv")
print(input_handler.grid)
print(input_handler.columns)

app = Dash(__name__)

app.layout = dash_table.DataTable(
    columns=input_handler.columns,
    data=input_handler.grid

)

if __name__ == '__main__':
    app.run_server(debug=True)
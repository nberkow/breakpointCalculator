import plotly.express as px

class BreakpointPlotMaker:

    def make_desnity_plot(self, data):
        grid, mic_lab, dia_lab = data
        fig = px.imshow(grid, text_auto=True, x=dia_lab, y=mic_lab)
        print(fig)
        fig.show()

    def make_optimization_plot(self):
        plot = ""
        return(plot)




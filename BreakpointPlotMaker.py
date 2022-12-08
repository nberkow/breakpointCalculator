import plotly.express as px

class BreakpointPlotMaker:

    def make_desnity_plot(self, data):
        grid, mic_lab, dia_lab = data
        mic_lab.reverse()
        fig = px.imshow(grid,
            labels=dict(x="DIA", y="MIC", color="count"),
            text_auto=True, aspect="auto",
            x=dia_lab,
            y=mic_lab
            )

        #fig.update_yaxes(autorange="reversed")
        fig.show()

    def make_optimization_plot(self):
        plot = ""
        return(plot)




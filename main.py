import pandas as pd
import sys
import os
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


library_data = pd.read_csv(resource_path("libraries_in_Poland.csv"),sep=";")
print(library_data)

fig = make_subplots(rows=1, cols=1, subplot_titles=("Number of libraries in each Voivodeship",),vertical_spacing=0.2, )

fig.add_trace(
    go.Bar(y=library_data["Number of libraries"],x=library_data["Voivodeship"],
           orientation="v", name="Number of libraries by Voivodeship",marker_color="#e6a39e", hoverlabel=
            dict(
               bgcolor="#fae8e6",font=dict(family="comfortaa")
            )
    ),
    row=1, col=1
)

fig.update_layout(
    plot_bgcolor="#fae3e1"
)
fig.update_annotations(font_size=35, font_family="comfortaa")
fig.update_xaxes(tickangle=-75, title="Voivodeships", title_font_size = 25, tickfont_size=14, title_font_family="comfortaa", tickfont_family="comfortaa")
fig.update_yaxes(title="Number of libraries", title_font_size = 25, tickfont_size=14, title_font_family="comfortaa", tickfont_family="comfortaa")


fig.show()
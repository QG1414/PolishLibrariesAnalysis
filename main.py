import pandas as pd
import sys
import os
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


library_data = pd.read_csv(resource_path("libraries_in_Poland.csv"),sep=";")


fig = make_subplots(
    rows=6, cols=2, 
    subplot_titles=("Number of libraries in each Voivodeship",),
    vertical_spacing=0.2,
    horizontal_spacing=0.2,
    specs=[
        [{"colspan":2,"rowspan":2,"type": "bar"},None], #"colspan":2,"rowspan":2,
        [None,None],
        [{"rowspan":2,"type": "bar"}, {"rowspan":2,"type": "bar"}],#"rowspan":2,"rowspan":2,
        [None,None],
        [{"type":"pie","colspan":2,"rowspan":2},None],
        [None,None]
    ]
)

#Visualization of number of libraries

fig.add_trace(
    go.Bar(y=library_data["Number of libraries"],x=library_data["Voivodeship"],
           orientation="v", name="Number of libraries by Voivodeship",marker_color="#e6a39e", hoverlabel=
            dict(
               bgcolor="#fae8e6",font=dict(family="comfortaa")
            )
    ),
    col=1, row = 1
)

fig.update_layout(
    plot_bgcolor="#fae3e1",
    autosize=True,
    height=2000
)
fig.update_annotations(font_size=35, font_family="comfortaa")
fig["layout"]["xaxis1"].update(tickangle=-75, title="Voivodeships", title_font_size = 25, tickfont_size=14, title_font_family="comfortaa", tickfont_family="comfortaa")
fig["layout"]["yaxis1"].update(title="Number of libraries", title_font_size = 25, tickfont_size=14, title_font_family="comfortaa", tickfont_family="comfortaa")


#Visualization of librarians and books


number_of_librarians = round(library_data["Number of librarians"] / library_data["Number of libraries"],2)
number_of_books = round(library_data["Amount of books"] / library_data["Number of libraries"],2)

librarians_data = pd.DataFrame({
    "Voivodeship":library_data["Voivodeship"],
    "Number of librarians per library" : number_of_librarians.values
})

books_data = pd.DataFrame({
    "Voivodeship":library_data["Voivodeship"],
    "Number of books per library":number_of_books.values
})

librarians_data.sort_values(by="Number of librarians per library",ascending=False,inplace=True)
books_data.sort_values(by="Number of books per library",ascending=False,inplace=True)

librarians_data.reset_index(inplace=True, drop=True)
books_data.reset_index(inplace=True, drop=True)

fig.add_trace(
    go.Bar(
        x=librarians_data["Number of librarians per library"], y=librarians_data["Voivodeship"],
        orientation="h",name="number of librarians per library in each voivodeship",text=librarians_data["Number of librarians per library"],
        hovertext="sd"
    ),
    row = 3, col = 1
)

fig.add_trace(
    go.Bar(
        x=books_data["Number of books per library"] ,y=books_data["Voivodeship"],
        orientation="h",name="Number of books per library in each voivodeship",text=books_data["Number of books per library"]
    ),
    row = 3, col=2
)

fig["layout"]["xaxis2"].update(title="Number of librarians", title_font_size = 25, tickfont_size=14, dtick=0.25)
fig["layout"]["xaxis3"].update(title="Number of books", title_font_size = 25, tickfont_size=14, dtick=2500)

customdata  = np.stack((librarians_data["Voivodeship"],librarians_data["Number of librarians per library"]), axis=-1)


print(customdata)
hovertemplate="<br>".join([
        "Voivodeship: %{customdata[0][0]}",
        "number of librarians: %{customdata[0][1]}",
    ])
fig.add_trace(
    go.Pie(
        values=librarians_data["Number of librarians per library"],
        labels=librarians_data["Voivodeship"],
        name="",
        customdata=customdata,
        hovertemplate=hovertemplate
        ),
    row = 5, col = 1
)

fig.show()
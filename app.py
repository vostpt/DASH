from datetime import date

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash_bootstrap_templates import load_figure_template

import dataset

# Get template for layout

load_figure_template("slate")

# --------------------- DATA TREATMENT --------------------------

df = dataset.create_dataset_top10(None)

# Create a new dataframe for the bar graph

df_bar = df

# Change the hour column to DType Date / Time 

df_bar['hour'] = pd.to_datetime(df_bar.hour)

# Sort values in the dataframe by Date / Time 

df_bar.sort_values(by=['hour'])

# Create dataframe for table 

df_table = df[["hour", "district", "natureza", "status", "total_meios"]].tail(10)

# --------------------- Create Elements  --------------------------

# Create table 

table = dbc.Table.from_dataframe(df_table, striped=True, bordered=True, hover=True)

# Create Graphs for the layout

fig = px.pie(df, names='district', values='total_meios', hole=0.7,
             color_discrete_sequence=px.colors.sequential.Viridis_r)
fig1 = px.pie(df, names='concelho', values='total_meios', hole=0.7,
              color_discrete_sequence=px.colors.sequential.Viridis_r)
fig2 = px.pie(df, names='district', values='total_meios', hole=0.7,
              color_discrete_sequence=px.colors.sequential.Viridis_r)
fig3 = px.bar(df_bar, x='hour', y='total_meios', color='natureza',
              color_discrete_sequence=px.colors.sequential.Viridis_r)

# --------------------- DASH APP STARTS HERE  --------------------------

# Define app 

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE], title='VOST Portugal - DASHOARD', update_title=None,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}]
                )
# start server 

server = app.server

# app layout 

app.layout = dbc.Container(
    [
        # set update intervals for the three graphs 
        dcc.Interval(
            id='interval-component',
            interval=60 * 1000  # in milliseconds
        ),
        html.Hr(),
        dbc.Row(
            [
                dcc.DatePickerSingle(
                    clearable=True,
                    id='incidents-date-picker',
                    min_date_allowed=date(2018, 1, 1),
                    max_date_allowed=date.today(),
                    initial_visible_month=date.today(),
                    date=date.today()
                )
            ]
        ),

        # create row
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id='graph_actual', figure=fig, className="h-100"), lg=3),  # First Graph
                dbc.Col(dcc.Graph(id='graph_all', figure=fig1, className="h-100"), lg=3),  # Second Graph
                dbc.Col(id='table_one', children=table)  # Table
            ],

        ),
        # Create Second row
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id='graph', figure=fig2, className="h-100"), lg=6),  # Third Graph
                dbc.Col(dcc.Graph(id='timeline', figure=fig3, className="h-100"), lg=6),  # Fourth Graph

            ],

        ),
    ],
    # set fluid to true to make the layout mobile ready
    fluid=True,
)


# --------------------- CREATE APP CALLBACK  --------------------------


# Define the outputs (graphs and table) and define the input (time interval)

@app.callback(
    Output('graph_actual', 'figure'),
    Output('graph_all', 'figure'),
    Output('graph', 'figure'),
    Output('table_one', 'children'),
    Output('timeline', 'figure'),
    [
        Input('incidents-date-picker', 'date'),
    ]
)
# Define what happens when the callback is triggered
def update_figs(date_updated):
    df_new = dataset.create_dataset_top10(date_updated)

    df_new_table = df_new[["hour", "district", "natureza", "status", "total_meios"]]

    # Create a new dataframe for the br graph

    df_new_bar = df_new

    # Change DType of hour to Date Time

    df_new_bar['hour'] = pd.to_datetime(df_bar.hour)

    # Sort dataframe by Date Time (hour column )

    df_new_bar.sort_values(by=['hour'])

    # --------------------- CREATE GRAPHS AND TABLES   --------------------------

    fig_new = px.pie(df_new, names='district', values='total_meios', hole=0.7,
                     color_discrete_sequence=px.colors.sequential.Viridis_r)
    fig_all = px.pie(df_new, names='concelho', values='total_meios', hole=0.7,
                     color_discrete_sequence=px.colors.sequential.Viridis_r)
    fig_total = px.pie(df_new, names='district', values='total_meios', hole=0.7,
                       color_discrete_sequence=px.colors.sequential.Viridis_r)
    table_new = dbc.Table.from_dataframe(df_new_table, striped=True, bordered=True, hover=True)
    fig_timeline = px.bar(df_new_bar, x='hour', y='total_meios', color='district',
                          color_discrete_sequence=px.colors.sequential.Viridis_r)

    # fig_new layout changes

    fig_new.update_layout({
        'plot_bgcolor': '#282b2f',
        'paper_bgcolor': '#282b2f',
    }
    )

    fig_new.update_layout(showlegend=False)

    fig_new.update_layout(
        title="Recursos Alocados - Top 10 Distritos",
        legend_title="Tipo de Ocorrência",
        font=dict(
            color="white",
            size=12
        )
    )
    fig_new.update_traces(textposition='outside', textinfo='percent+label')

    fig_new.update_layout(
        {
            'plot_bgcolor': '#282b2f',
            'paper_bgcolor': '#282b2f',
        }
    )

    # fig_all layout changes

    fig_all.update_layout({
        'plot_bgcolor': '#282b2f',
        'paper_bgcolor': '#282b2f',
    }
    )

    fig_all.update_layout(showlegend=False)

    fig_all.update_layout(
        title="Recursos Alocados - Top 10 Concelhos",
        legend_title="Tipo de Ocorrência",
        font=dict(
            color="white",
            size=12
        )
    )
    fig_all.update_traces(textposition='outside', textinfo='percent+label')

    fig_all.update_layout(
        {
            'plot_bgcolor': '#282b2f',
            'paper_bgcolor': '#282b2f',
        }
    )

    # fig_total layout changes

    fig_total.update_layout({
        'plot_bgcolor': '#282b2f',
        'paper_bgcolor': '#282b2f',
    }
    )

    fig_total.update_layout(showlegend=False)

    fig_total.update_layout(
        title="Recursos Alocados - Histórico",
        legend_title="Tipo de Ocorrência",
        font=dict(
            color="white",
            size=12
        )
    )
    fig_total.update_traces(textposition='outside', textinfo='percent+label')

    fig_total.update_layout(
        {
            'plot_bgcolor': '#282b2f',
            'paper_bgcolor': '#282b2f',
        }
    )

    fig_timeline.update_layout(
        {
            'plot_bgcolor': '#282b2f',
            'paper_bgcolor': '#282b2f',
        }
    )

    # Return these elements to the output

    return fig_new, fig_all, fig_total, table_new, fig_timeline


# --------------------- MAKE APP LIVE   --------------------------

# launch app

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8052, debug=True)

# --------------------- APP ENDS HERE  --------------------------

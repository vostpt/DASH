# import main libraries
import pandas as pd 
import plotly.express as px 
import time 
import json
import urllib
import urllib.request

# import dash libraries  
import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output


# import dash bootstrap components 

import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table

from dash_bootstrap_templates import load_figure_template

# Get template for layout

load_figure_template("slate")

# --------------------- DATA TREATMENT --------------------------

# Read CSV file
data_cols = ["id","hour","aerial","terrain","man","district","concelho","familiaName","naturezaName","especieName","status"]
df_csv =pd.read_csv('112.csv', usecols=data_cols)

# Get JSon 

url = "https://emergencias.pt/data"
response  = urllib.request.urlopen(url).read()

jsonResponse = json.loads(response.decode('utf-8'))

# Create dataframe with pandas from json response 

sourcedata = pd.json_normalize(jsonResponse['data'])

# Slim down dataset by creating a dataframe with only the columns we need 

df_source = sourcedata.loc[:, data_cols]

# Change the DType of id to a integer 

df_source["id"] = df_source["id"].astype(int)

# Merge both dataframes 

df= df_csv.merge(df_source, on=list(df_csv), how='outer')

# Remove Duplicates if any 

df.drop_duplicates(subset=['id'], inplace=True, keep='last')

# Save CSV file from resulting dataframe 

df.to_csv('112.csv', index=False)

# Create new columns that sums the values of resources for each event 

df['total_meios'] = df['man'] + df['terrain']+df['aerial']

# Create a dataframe with only the last 10 events 

df_10=df.tail(10)

# Create a new dataframe for the bar graph 

df_bar=df

# Change the hour column to DType Date / Time 

df_bar['hour'] =pd.to_datetime(df_bar.hour)

# Sort values in the dataframe by Date / Time 

df_bar.sort_values(by=['hour'])

# Create dataframe for table 

df_table=df_10[["hour", "district","naturezaName","status","total_meios"]]

# --------------------- Create Elements  --------------------------

# Create table 

table = dbc.Table.from_dataframe(df_table.tail(10), striped=True, bordered=True, hover=True)


# Create Graphs for the layout 

fig = px.pie(df_10,names='district',values='total_meios',hole=0.7,color_discrete_sequence=px.colors.sequential.Viridis_r)
fig1= px.pie(df_10,names='concelho',values='total_meios',hole=0.7,color_discrete_sequence=px.colors.sequential.Viridis_r)
fig2= px.pie(df,names='district',values='total_meios',hole=0.7,color_discrete_sequence=px.colors.sequential.Viridis_r)
fig3=px.bar(df_bar,x='hour',y='total_meios', color='naturezaName',color_discrete_sequence=px.colors.sequential.Viridis_r)


# --------------------- DASH APP STARTS HERE  --------------------------

# Define app 

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE],title='VOST Portugal - DASHOARD',update_title=None,
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
           interval=60*1000, # in milliseconds
           n_intervals=0
        ),
    html.Hr(),
    # create row
    dbc.Row(
        [
            dbc.Col(dcc.Graph(id='graph_actual',figure=fig, className="h-100"),lg=3), # First Graph 
            dbc.Col(dcc.Graph(id='graph_all',figure=fig1, className="h-100"),lg=3), # Second Graph 
            dbc.Col(id='table_one', children=table) # Table 
        ], 
        
    ),
    # Create Second row 
    dbc.Row(
        [
            dbc.Col(dcc.Graph(id='graph',figure=fig2, className="h-100"),lg=6), # Third Graph 
            dbc.Col(dcc.Graph(id='timeline',figure=fig3, className="h-100"),lg=6), # Fourth Graph
            
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
    Output('table_one','children'),
    Output('timeline', 'figure'),
    [Input('interval-component', "n_intervals")]

 )
# Define what happens when the callback is triggered

def UpdateFigs(value):

	# Read CSV 

	df = pd.read_csv('112.csv')

	# Get JSon 

	url = "https://emergencias.pt/data"
	response  = urllib.request.urlopen(url).read()

	jsonResponse = json.loads(response.decode('utf-8'))

	# Create dataframe with pandas from json response 

	sourcedata_new = pd.json_normalize(jsonResponse['data'])

	# Slim down dataset by creating a dataframe with only the columns we need 

	df_new=sourcedata_new.loc[:, ['id', 'hour','aerial', 'terrain', 'man', 'district','concelho', 'familiaName','naturezaName', 'especieName','status']]

	# Change the DType of id to a integer 

	df_new["id"] = df_new["id"].astype(int)

	# Create new column that sums the values of resources for each event 

	df_new['total_meios'] = df_new['man'] + df_new['terrain']+df_new['aerial']

	# Merge both dataframes 

	df= df.merge(df_new, on=list(df), how='outer')

	# Merge duplicates if any 

	df.drop_duplicates(subset=['id'], inplace=True, keep='last')

	# Save resulting dataframe to the csv file 

	df.to_csv('112.csv', index=False)

	# Create a dataframe with only the last 10 events 

	df_new = df_new.tail(10)

	# Create a dataframe for the table 

	df_new_table=df_new[["hour", "district","naturezaName","status","total_meios"]]

	# Create a new dataframe for the br graph 

	df_new_bar=df

	# Change DType of hour to Date Time 

	df_new_bar['hour'] =pd.to_datetime(df_bar.hour)

	# Sort dataframe by Date Time (hour column )

	df_new_bar.sort_values(by=['hour'])

	# --------------------- CREATE GRAPHS AND TABLES   --------------------------

	fig_new = px.pie(df_new,names='district',values='total_meios',hole=0.7,color_discrete_sequence=px.colors.sequential.Viridis_r)
	fig_all = px.pie(df_new,names='concelho',values='total_meios',hole=0.7,color_discrete_sequence=px.colors.sequential.Viridis_r)
	fig_total = px.pie(df,names='district',values='total_meios',hole=0.7,color_discrete_sequence=px.colors.sequential.Viridis_r)
	table_new=dbc.Table.from_dataframe(df_new_table.tail(10), striped=True, bordered=True, hover=True)
	fig_timeline=px.bar(df_new_bar,x='hour',y='total_meios', color='district',color_discrete_sequence=px.colors.sequential.Viridis_r)

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
    app.run_server(port=8052, debug=True)

# --------------------- APP ENDS HERE  --------------------------
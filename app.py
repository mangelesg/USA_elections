import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

#import importlib
#import nbimporter
# import data_scraping
# import data_cleaning
# pd.options.display.min_rows = 20
from dash import Dash, dcc, html, Input, Output
import os


import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import json

app = Dash(__name__)
server = app.server


##******************** IMPORT DATA


datasets = pd.read_csv('datasets_all_branches.csv')



## this calculates the percentage of each party compared to the total
## it can be calculated for senate (_s), president (_p), house (_h),gobernors (_g)
## or any combination of those. the sufixs have to be inside a list ex: ['_h'] ex2: ['_p','_g']
def percentage_dominance(sufixs, datasets):
    cols = [b+s for b in ['D','R','O'] for s in sufixs]
    Dcols = ['D' + s for s in sufixs]
    Rcols = ['R' + s for s in sufixs]
    Ocols = ['O' + s for s in sufixs]

    DDs = 100*(datasets[Dcols].sum(axis=1)/datasets[cols].sum(axis=1))#.fillna(0)
    OOs = 100*(datasets[Ocols].sum(axis=1)/datasets[cols].sum(axis=1))#.fillna(0)
    RRs = 100*(datasets[Rcols].sum(axis=1)/datasets[cols].sum(axis=1))#.fillna(0)

    return(DDs, OOs, RRs)


# This functions multiply the republican values by -1, so when we plot in the map, 	they look red in the colorscale

def negative_value_republicans(datasets, percents=['D_prcnt','R_prcnt','O_prcnt']): 
    # branches must be a list in order : democrats, others, republicans
    # choose from: %D_total, %D_p, %D_h, %D_
    
    
    winner = datasets[percents].max(axis=1)
    
    conditions = [
   (datasets[['D_prcnt','O_prcnt','R_prcnt']].idxmax(axis=1)=='D_prcnt') & 	(datasets[['D_prcnt','O_prcnt','R_prcnt']].max(axis=1)!=0),
    (datasets[['D_prcnt','O_prcnt','R_prcnt']].idxmax(axis=1)=='R_prcnt') & 	(datasets[['D_prcnt','O_prcnt','R_prcnt']].max(axis=1)!=0),
                ]
    choices = [1,-1]

    datasets['branches_winner'] = np.select(conditions, choices, default=0)
    datasets['value_branches'] = winner*datasets['branches_winner']
	
	
	


trend_title = html.P(className="chart-header", children='Evolution of parties dominance')


##*********************************
@app.callback(Output('trend-graph', 'figure'), 
              [Input('map-graph', 'clickData'),
                  
             #Input('state-dropdown', 'value'),
               Input('checklist-branch1', 'value'),
              Input('dropdown-mode', 'value')])
def update_trend_graph(clickData,branches, modelplt):
    statecode = 'AL'
    if clickData:
        statecode = clickData['points'][0]['location']

    datasets2 = 0
    if statecode == 'All':
        cols = [b+s for b in ['D','R','O'] for s in branches]
        datasets1 = datasets[['Year']+cols].groupby(['Year']).sum().reset_index()
        dd,oo,rr = percentage_dominance(branches, datasets1)
        subset = datasets1.assign( D_prcnt = dd, O_prcnt = oo, R_prcnt = rr )
    else:      
        dd,oo,rr = percentage_dominance(branches, datasets)
        datasets2 = datasets.assign( D_prcnt = dd, O_prcnt = oo, R_prcnt = rr )
        subset = datasets2.query(f"code == '{statecode}'")
        
    fig = go.Figure()#fig = go.Figure(layout=layout)
    
##**************************** add rolling mean plot ************************    
    if modelplt == 'rolling':
        
        subset2 = subset.rolling(5,axis=0).mean()
        fig.add_trace(go.Scatter(x=subset2['Year'], y=subset2['D_prcnt'],
                        line = dict(color='royalblue', width=2),
                        mode='lines',
                        connectgaps = True,
                        showlegend =False
                        ))
        fig.add_trace(go.Scatter(x=subset2['Year'], y=subset2['R_prcnt'],
                        line = dict(color='firebrick', width=2),
                        mode='lines',
                        connectgaps = True,
                        showlegend =False
                        ))
        fig.add_trace(go.Scatter(x=subset2['Year'], y=subset2['O_prcnt'],
                        line = dict(color='teal', width=2),
                        mode='lines',
                        connectgaps = True,
                        showlegend =False
                        )) 
        modelplt = 'markers'
##***************************************************************************    
        
    
    fig.add_trace(go.Scatter(x=subset['Year'], y=subset['D_prcnt'],
                    line = dict(color='royalblue', width=2),
                    mode=modelplt,
                    connectgaps = True,
                    name='Democrats'))
    fig.add_trace(go.Scatter(x=subset['Year'], y=subset['R_prcnt'],
                    line = dict(color='firebrick', width=2),
                    mode=modelplt,
                    connectgaps = True,
                    name='Republicans'))
    fig.add_trace(go.Scatter(x=subset['Year'], y=subset['O_prcnt'],
                    line = dict(color='teal', width=2),
                    mode=modelplt,
                    connectgaps = True,
                    name='Others')) 
    
    
    
    fig.update_layout(paper_bgcolor = "rgba(0,0,0,0)",
                  plot_bgcolor = "rgba(0,0,0,0)",
                     title=datasets[datasets['code']==statecode]['State'].unique()[0],
                xaxis_title="Year",
                yaxis_title="Dominance",
                legend_title="Party",
                font=dict(
                    family="Sans Serif",
                    size=16,
                    color="black"
                    ))

    del datasets2
    return fig
	
	
	
##*******************************************

@app.callback(
    Output('hover-data', 'children'),
    Input('trend-graph', 'hoverData'),
    Input('map-graph', 'clickData'),)
def display_hover_data(hoverData, clickData):
    year = hoverData['points'][0]['x']
    statecode = "AL" # default is alabama
    if clickData:
        statecode = clickData['points'][0]['location']
   
    if statecode != 'All':
    

        subset = datasets.query(f'Year == {year} & code == "{statecode}"')[['D_p','R_p','O_p','D_s','R_s','O_s','D_h','R_h','O_h','D_g','R_g','O_g']]


        president = 'No elections'
        if subset['D_p'].item() == 1:
            president = "Democrat"
        elif subset['R_p'].item() == 1:
            president = 'Republican'
        elif subset['O_p'].item() == 1:
            president = 'Other'

        gobernor = 'No elections'
        if subset['D_g'].item() >= 1:
            gobernor = "Democrat"
        elif subset['R_g'].item() >= 1:
            gobernor = 'Republican'
        elif subset['O_g'].item() >= 1:
            gobernor = 'Other'

        senator = 'No elections'
        if subset['D_s'].item() >= 1:
            senator = "Democrat"
        elif subset['R_s'].item() >= 1:
            senator = 'Republican'
        elif subset['O_s'].item() >= 1:
            senator = 'Other'

        house_other = str(subset['O_h'].item()) + ' Other'
        house_democrat = str(subset['D_h'].item()) + ' Democrats'
        house_republican = str(subset['R_h'].item() ) + ' Republicans' 


        chunks = [
            'Year:' + str(year),
            'President (state total): '+ president,
            'Senator: ' + senator,
            'House: ' + str(house_democrat),
            '       ' + str(house_republican),
            '       ' + str(house_other),
            'Gobernor: ' + gobernor
            ]

    else:
        subset = datasets.query(f'Year == {year}')[['D_p','R_p','O_p','D_s','R_s','O_s','D_h','R_h','O_h','D_g','R_g','O_g']]

        chunks = [
            'Year:' + str(year),
            'President: '+ str(subset['D_p'].sum()) + ' Democrats',
            '           '+ str(subset['R_p'].sum()) + ' Republicans',
            '           '+ str(subset['O_p'].sum()) + ' Others',
            '                     ',
            'Senator: ' + str(subset['D_s'].sum()) + ' Democrats',
            '         ' + str(subset['R_s'].sum()) + ' Republicans',
            '         ' + str(subset['O_s'].sum()) + ' Others',
            '                     ',
            'House: ' + str(subset['D_h'].sum()) + ' Democrats',
            '       ' + str(subset['R_h'].sum()) + ' Republicans',
            '       ' + str(subset['O_h'].sum()) + ' Others',
            '                     ',
            'Gobernor: ' + str(subset['D_g'].sum()) + ' Democrats',
            '          ' + str(subset['R_g'].sum()) + ' Republicans',
            '          ' + str(subset['O_g'].sum()) + ' Others',
            ]
        
        
    return [html.P(children=chunk) for chunk in chunks]



##**********************************

@app.callback(Output('map-graph', 'figure'), 
              [Input('year-dropdown', 'value'),
               Input('checklist-branch1', 'value')])
def update_map_graph(year, branches):


    
    datasets2 = 0
    dd,oo,rr = percentage_dominance(branches, datasets)
    datasets2 = datasets.assign( D_prcnt = dd, O_prcnt = oo, R_prcnt = rr )
    negative_value_republicans(datasets2)
    
    fig = px.choropleth(datasets2[datasets2.Year == year], 
                        color='value_branches',
                        locations='code',
                        locationmode='USA-states', 
                        color_continuous_scale=px.colors.sequential.RdBu,
                           #range_color=(0, 12),
                        scope="usa",
                        labels={'unemp':'unemployment rate'}
                          )
    fig.update_layout(
        coloraxis_colorbar=dict(
        title="% Dominance",
        dtick=25,
        tickmode="array",
        tickvals=[100, 75, 50, 25, 0, -25, -50, -75, -100],
        ticktext=["100","75", "50", '25', "0",'25', "50", "75", "100" ],
            )
        )

    
#     fig = go.Figure(data=go.Choropleth(
#         locations=datasets['code'],
#         z=datasets[datasets.Year == year][['code','value_branches']],
#         locationmode='USA-states',
#         colorscale=px.colors.diverging.RdBu,
#         #color_continuous_scale=px.colors.diverging.RdBu,
#         #color_continuous_midpoint=0,
#         autocolorscale=False,
#         #text=df['text'], # hover text
#         marker_line_color='white', # line markers between states
#         colorbar_title="Millions USD"
#     ))
#     fig.update_layout(
#         title_text=f'{year}',
#         geo = dict(
#             scope='usa',
#             projection=go.layout.geo.Projection(type = 'albers usa'),
#             showlakes=True, # lakes
#             lakecolor='rgb(255, 255, 255)',
#             margin={"r":0,"t":0,"l":0,"b":0}),
#    )

    return fig
	
##******************* LAYOUT

app.layout = html.Div([

#***** header
    html.Div(
        id = 'header',
        children = [
        html.H4("Political distribution of government branches"),
        html.P(id = 'description',
            children = 'This application displays the evolution of the Democratic and Republican parties distribution on the Presidens, Senators, House of Representatives and Gobernors.'
              )   
                ]),
#***** second row    
    
    html.Div(className='graph-row',
        
        children = [html.Div(className='graph-container',
        
                            children = [html.Div(children=[dcc.Dropdown(
                                                id = 'year-dropdown',
                                                placeholder = 'Filter by Year',
                                                options = sorted(datasets.Year.unique().tolist()),
                                                value=2018),

                                                dcc.Checklist(
                                                   id = 'checklist-branch1',
                                                   options=[{'label':'Presidential elections', 'value':'_p'},
                                                            {'label':'Senate', 'value':'_s'},
                                                            {'label':'House of Rep.', 'value':'_h'},
                                                            {'label':'Gobernor', 'value':'_g'}],
                                                   value=['_p','_h','_s','_g'],
                                                    inline=True
                                                           ),]
                                                    , style={'width': '40%',  'color':'#6f807b'}),

                                        html.Div(
                                            children = [dcc.Graph(id='map-graph',className='graph')    
                                            ], style={'width': '100%', 'display': 'inline-block', 'color':'#6f807b'}),

                                                   ]),

                    html.Div( className='graph-container',
                            
                            children = [     

                                html.Div([ 
                                    dcc.Dropdown(
                                   id = 'dropdown-mode',
                                   options=[{'label':'line', 'value':'lines'},
                                            {'label':'markers', 'value':'markers'},
                                            {'label':'markers+lines', 'value':'lines+markers'},
                                            {'label':'rolling mean (5 election periods)', 'value':'rolling'}],
                                   value='lines+markers',
                                           )], style={'width': '40%',  'color':'#6f807b'}),
                                html.Div([    
                                    html.Div([
                                        dcc.Graph(id='trend-graph',className='row', hoverData={'points': [{'x': 1850}]})
                                                  ],             
                                
                                        style={'width': '100%', 'display': 'inline-block', 'color':'#6f807b'},
                                            ),
                                    html.Div([
                                            dcc.Markdown("""
                                                **Elections results**

                                                Move mouse over values in the graph.
                                            """),
                                            html.Pre(id='hover-data',)
                                        ], className='row',
                                        style={'width': '60%', 'display': 'inline-block', 'padding': '0 20'}
                                        ),
                                            ]),

                           ]),
    
        
        ])
    
   ])
   
 
 
##********************* RUN APP
#
if __name__ == '__main__':
    app.run_server(debug=True)
# app.run_server(debug=True,host='0.0.0.0', port=8015
#                 , mode="external")

# being called in __init__.py
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import pandas as pd
#import geopandas as gpd
import json
import requests
import plotly.graph_objects as go
import plotly.express as px # for the 2nd graph
#import plotly.offline as py --------- using when debugging in jupyter notebook

#import numpy as np
#import pyproj as pj
#import datetime as dt
#from collections import Counter
#import matplotlib.pyplot as plt
#import matplotlib as mpl
#import seaborn as sns
#import shapely
#import descartes #to plotting polygons in geopandas
#import plotly.express as px
#from plotly.subplots import make_subplots

#import io
#import base64




# Flask app into Dash as server
def init_dashboard(server): # or create_dashboard
    
    # didn't need to be assets folder, static works well
    # I changed the name to assets to see if it sees all files in it
    external_stylesheets = ["/static/assets/style_withdash.css"]
    #external_stylesheets = [dbc.themes.BOOTSTRAP] ############ try later

    # try to create a function that call another file with this function

    # assume you have a "long-form" data frame # see https://plotly.com/python/px-arguments/ for more options
    #df = pd.DataFrame({
    #"Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    #"Amount": [4, 1, 2, 2, 4, 5],
    #"City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    #})
    #fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

    #-------------------------------------------------------------------------
    """Create a Plotly Dash dashboard."""
    # Single function which contains the entirety of a Plotly Dash app in itself
    dash_app = dash.Dash(
        server=server,
        # Creating a route for Dash # of course, we could always pass / as our prefix
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=external_stylesheets
        )
    #dash_app.css.append_css({
        #"external_url":'dbc.themes.BOOTSTRAP'
        #"external_url":'https://codepen.io/chriddyp/pen/bWLwgP.css',
        #"external_url":"/static/assets/style_withdash.css"
        #})
    #""""""""""""""""""""""""""""""""""""""""""""""""""""
 
    #""""""""""""""""""""""""""""""""""""""""""""""""""""DATA GRAPHS"""""""""""""""""""""""""""""""
    # 2nd - Creating the body
    # Individuals components of the Graphs first
    ##urlDataPath = ('https://github.com/Juunicacio/Track-Turtle-App/tree/gh-pages/flask_plotlydash/static/data/')
    
    # url of the shapefiles as csv 
    ##url_depthPointsDegree = 'https://raw.githubusercontent.com/Juunicacio/Track-Turtle-App/gh-pages/flask_plotlydash/static/data/%7B4%7D.degree_Acquisition_Time_Depth_Points_Tag_333A_Sept.csv'
    ##url_gpsPoints = 'https://raw.githubusercontent.com/Juunicacio/Track-Turtle-App/gh-pages/flask_plotlydash/static/data/%7B5%7D.reproj_Track_GPS_Points_Tag_333A_Sept.csv'

    # path for the Json files
    #path_depthPointsDegree = "/static/data/{7}.depthPointsDegree.json"
    #path_gpsPoints = "/static/data/{8}.gpsPointsDegree.json"

    # url (raw) path for Json files
    url_depthPointsDegree = 'https://raw.githubusercontent.com/Juunicacio/Track-Turtle-App/gh-pages/flask_plotlydash/static/data/%7B7%7D.depthPointsDegree.json'
    url_gpsPoints = 'https://raw.githubusercontent.com/Juunicacio/Track-Turtle-App/gh-pages/flask_plotlydash/static/data/%7B8%7D.gpsPointsDegree.json'

    #___________Not json file__________
    #depthPointsDegree = pd.read_csv(path_depthPointsDegree)
    #gpsPoints = pd.read_csv(path_gpsPoints)
    # Depth Lon and Lat in degrees
    #xDegreeDepth = depthPointsDegree.geometry.x
    #yDegreeDepth = depthPointsDegree.geometry.y
    # GPS Lon and Lat in degrees
    #xDegreeGps = gpsPoints['GPS Longit']
    #yDegreeGps = gpsPoints['GPS Latitu']
    # Converted Decimals to Percentage just to use in the hovertext, for visualization, it don't work with the markers
    #layer1DepthsInPercentage = layer1Depths.apply(lambda x: '{:1.2f}%'.format(100 * x))
    #----------------------------------

    # Reading the Json files   
    #with open(path_depthPointsDegree) as geofile:
        #jdata_depthPointsDegree = json.load(geofile)
    #with open(path_gpsPoints) as geofile:
        #jdata_gpsPointsDegree = json.load(geofile)

    # Reading the Json files from url
    responseDegree = requests.get(url_depthPointsDegree)
    responseGps = requests.get(url_gpsPoints)

    jdata_depthPointsDegree = responseDegree.json()
    jdata_gpsPointsDegree = responseGps.json()

    # FIRST ROW - Depth Lon and Lat in degrees (4326)
    #jdata_depthPointsDegree['features'][0]['geometry']['coordinates'][0]
    #jdata_depthPointsDegree['features'][0]['geometry']['coordinates'][1]

    # FIRST ROW - GPS Lon and Lat in degrees (4326)
    #jdata_gpsPointsDegree['features'][0]['geometry']['coordinates'][0]
    #jdata_gpsPointsDegree['features'][0]['geometry']['coordinates'][1]

    # FIRST ROW - Depth Acquisition time
    #jdata_depthPointsDegree['features'][0]['properties']['Acquisitio']
    # FIRST ROW - GPS Acquisition time
    #jdata_gpsPointsDegree['features'][0]['properties']['Acquisitio']

    # FIRST ROW - Depth Layer 1
    #jdata_depthPointsDegree['features'][0]['properties']['Layer 1 Pe']

    # CREATE A loop through Depth Lon[0] and Lat[1]--------
    jxDegreeDepth = []
    jyDegreeDepth = []
    for i in jdata_depthPointsDegree['features']:
        lonDepth = i['geometry']['coordinates'][0]
        latDepth = i['geometry']['coordinates'][1]
        jxDegreeDepth.append(lonDepth)
        jyDegreeDepth.append(latDepth)

    # CREATE A loop through GPS Lon[0] and Lat[1]
    jxDegreeGps = []
    jyDegreeGps = []
    for i in jdata_gpsPointsDegree['features']:
        lonGps = i['geometry']['coordinates'][0]
        latGps = i['geometry']['coordinates'][1]
        jxDegreeGps.append(lonGps)
        jyDegreeGps.append(latGps)

    # Creating a loop for Depth Acquisition time ----------
    jacquisitionDepth = []
    for i in jdata_depthPointsDegree['features']:
        aquisDepth = i['properties']['Acquisitio']
        jacquisitionDepth.append(aquisDepth)

    # Creating a loop for GPS Acquisition time
    jacquisitionGps = []
    for i in jdata_gpsPointsDegree['features']:
        aquisGps = i['properties']['Acquisitio']
        jacquisitionGps.append(aquisGps)

    # Looping through Layer 1 -----------------------------
    jlayer1Depths = []
    for i in jdata_depthPointsDegree['features']:
        layer1 = i['properties']['Layer 1 Pe']
        jlayer1Depths.append(layer1)

    # Assigning variables for max and min float values in layer 1 percentage
    jminPercLay1 = min(feature["properties"]['Layer 1 Pe'] for feature in jdata_depthPointsDegree['features'])
    jmaxPercLay1 = max(feature["properties"]['Layer 1 Pe'] for feature in jdata_depthPointsDegree['features'])
 
    # Converted Decimals to Percentage just to use in the hovertext, for visualization, it don't work with the markers
    jlayer1DepthsInPercentage = []
    for i in jdata_depthPointsDegree['features']:
        intNum = i['properties']['Layer 1 Pe']*100
        percSymbol = '{:.2f}%'.format( intNum )
        jlayer1DepthsInPercentage.append(percSymbol)
     

    # Making an histogram data for layer 1 --------------------------------------------------------
    jgohistlayer1 = [go.Histogram(x=jlayer1DepthsInPercentage, #x = layer1Depths, #y=layer1Depths,
                         opacity=0.4,
                         marker=dict(color='orange'))]
    jlayout = go.Layout(barmode='overlay',
                                 title='Layer 1 histogram',
                                 yaxis_title='Count',
                                 xaxis_title='Layer 1 occurrence in %') # or 'Percentage (%) of occurrence in Layer 1'
    jfig = go.Figure(
            {"data": jgohistlayer1,
             "layout": jlayout})
    #py.iplot(jfig, filename='Layer 1 histogram') --------- using when debugging in jupyter notebook


    # Making Box Plot with plotly.express - didn't work
    # Making Go Map for Layer 1 -------------------------------------------------------------------
    jgomaptraceLayer1 = go.Figure(go.Scattermapbox(
                                    lat=jyDegreeGps,
                                    lon=jxDegreeGps,
                                    name = 'GPS Data',
                                    mode="markers+lines",
                                    marker = {'size': 8, 'color': 'yellow'}, # changed the size
                                    text = jacquisitionGps,
                                    hoverinfo='text'
                                ))
    jgomaptraceLayer1.add_trace(go.Scattermapbox(
                                    lat=jyDegreeDepth,
                                    lon=jxDegreeDepth,
                                    name = 'Depth data from 0 to -5 meters deep',
                                    mode = "markers+lines",
                                    text = jlayer1Depths,
                                    marker = {        
                                        'colorscale':[[0, 'green'], [1, 'rgb(0, 0, 255)']],
                                        'color': jlayer1Depths,
                                        'cmax':jmaxPercLay1,
                                        'cmin':jminPercLay1,
                                        'size': jlayer1Depths,
                                        'sizemin':0.1,
                                        'sizemode': 'area',
                                        'sizeref': jmaxPercLay1 / 6 **2,
                                        'showscale':True,
                                        'colorbar': {
                                            'title': 'Layer 1 occurrence in %', # including a colorbar
                                            'titleside':'top',
                                            'x': 0,
                                            'y': 0.5,
                                            'tickformat': ".0%", # Formating tick labels to percentage on color bar
                                            'tickfont': {
                                                'color': '#000000',
                                                'family':"Open Sans",
                                                'size': 14
                                            }
                                        }
                                    },   
                                    hoverinfo='text',
                                    hovertext = jlayer1DepthsInPercentage,  #100 * x), #(lambda x: '{0:1.2f}%'.format(x)#{:. n%} 
                                    opacity = 1
                                ))
    jgomaptraceLayer1.update_layout(
                margin ={'l':0,'t':0,'b':0,'r':0},
                showlegend=False, # change if you want to see the legend *
                mapbox = {        
                    'style': "stamen-terrain",
                    'center': {'lon': 10, 'lat': 37},
                    'zoom': 5})


    # the "fig" is jgomaptraceLayer1

    # Making Go Scatter for Layer 1 -------------------------------------------------------------------
    jgoscattermap = go.Figure()
    #for vender in temp.columns:
    jgoscattermap.add_trace(
        go.Scatter(
            x = jacquisitionDepth,
            y = jlayer1DepthsInPercentage,
            name='Layer 1: between 0 to -5 meters deep',
            showlegend=True,
            marker = dict(
                line = dict(
                width = 1,
                color = 'DarkSlateGrey')
            )
        )
    )

    jgoscattermap.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1h", step="hour", stepmode="backward"),
                dict(count=1, label="1d", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=2, label="2m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    jgoscattermap.update_layout(title='Depth Occurrence',
                        legend = {'orientation': 'h', 'x': 0.1 ,'y':1.4},
                        xaxis={'title': 'Datetime'},
                        yaxis={'title': 'Occurrence in %'}
    )

    # the "fig" is jgoscattermap



    ######################################################## END DATA GRAPHS ######################

    #dash_app.layout = html.Div ([
        #dcc.Upload(
            #id='upload-data',
            #children=html.Div([
                #'Drag and Drop or', #################### see it on my page
                #html.A('Select Files')
                #]),
                #style={
                #'with': '100%',
                #'height': '60px', #etc
                #},
                # Allow multiple files to be uploaded
                #multiple=True
        #),
        #html.Div(id='output-data-upload'),
        #]
    #)
    #html.Div([
        #html.H1(children='Hello Dash'),
        #html.Div(children= 'Dash: A web application framework for Python'),
        #dcc.Graph(
            #id='example-graph',
            #figure=jfig
        #)],
        #id='dash-container'
    #)
    #############################################################
    #def parse_data(contents, filename):
    #content_type, content_string = contents.split(',')
    #decoded = base64.b64decode(content_string)
    #try:
        #if 'csv' in filename:
            # Assume that the user uploaded a CSV or TXT file
            #df = pd.read_csv(
                #io.StringIO(decoded.decode('utf-8')))
        #elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            #df = pd.read_excel(io.BytesIO(decoded))
        #elif 'txt' or 'tsv' in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            #df = pd.read_csv(
                #io.StringIO(decoded.decode('utf-8')), delimiter = r'\s+')
    #except Exception as e:
        #print(e)
        #return html.Div([
            #'There was an error processing this file.'
       #])
    #return df #html.Div([
        #dcc.Graph(
            #id='example-graph',
            #figure=fig
            #)
        #])
    ###############################################################################################
    # Create Dash Layout # Page Layout stuff ------------------------------------------------------
       # The final Layout of the page will be NavBar + Body
    # Before the Layout let's create separately each of them
    #""""""""""""""""""""""""""""""""""""""""""""""""""""
    # 1st - Creating a NavBar with dropdown Items
    # Create the components that goes in the NavBar
    # make a reusable navitem for the different examples
    nav_item = dbc.NavItem(dbc.NavLink("example - Dash Udemy Course", href="https://www.udemy.com"))

    # make a reusable dropdown for the different examples
    dropdown = dbc.DropdownMenu(children=[
        dbc.DropdownMenuItem("Plotly / Dash", href='https://dash.plot.ly/'),
        dbc.DropdownMenuItem("Dash Bootstrap", href='https://dash-bootstrap-components.opensource.faculty.ai/')
        ],
        nav=True,
        in_navbar=True,
        label="Important Links"
        )
    # Navbar Layout
    navbar = dbc.Navbar([
        #dbc.Container([
            dbc.Col(html.H1("Track Turtle App", className= 'ml-5')),           

            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav([
                    nav_item, 
                    dropdown
                    ],
                    className="ml-auto",
                    navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,                
            ),

             # A is a link element
            html.A(
                dbc.Row([
                    #dbc.Col(html.H2("Track Turtle App", className= 'ml-2 left_column')),
                    dbc.Col(html.Img(src="/static/images/{2}.loggerhead_turtle.jpg", alt="Caretta caretta", height="50px")),
                    ],
                    align='center',
                    no_gutters=True
                ), 
                href=('/'),
                className= 'ml-4 mr-5'                
            ),
        #]), #id="top_banner"),
        #color="dark",
        #dark=True,
        #className="banner"# mb-5"
    ])
    ###############################################################################################

    dash_app.layout = html.Div([

        #html.Link(rel='stylesheet', href='/static/assets/style_withdash.css'),
        html.Link(rel='stylesheet', href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"),        

        html.Div([navbar
            #html.Div([html.H2("Track Turtle App")
                #], className= 'left_column'),
            #html.Div([html.Img(src="/static/images/{2}.loggerhead_turtle.jpg", alt="Caretta caretta")
                #], className= 'right_column')
            ]), #className='banner'),
        
        # ----------------------- GRAPHS -------------------------------
        html.Div(className= 'content-dash-container ml-5 mr-5 clear', children=[

            #html.H1(className= 'text-center' ,children='Hello Dash'),

            #html.Div(id='top', className= 'row', children=[
            dbc.Row([

                dbc.Col(html.Div(className= 'graph_text col-xl', children=[                
                        html.Div(className= 'graph_description', children=[
                            html.H1(className= 'text-center' ,children='Hello Dash'),
                            html.P('Layer 1 Description'),                            
                        ]),
                    ]),
                ),            

                dbc.Col(html.Div(className= 'graph_graph col-sm', children=[ #calling histogram graph layer 1 ------------------                
                        dcc.Graph(
                            id='hist_graph',
                            figure=jfig
                        ) # ------------------- end histogram)
                    ]),
                #html.Div(className= 'clear'),
                )
            ]),        
        #]),

            # ----------------------- calling histogram graph layer 1 -------------------------------
            #html.Div(id='div_hist_graph', children=[

                #html.H1(children='Hello Dash'),
                #html.Div(children= 'Dash: A web application framework for Python'),
                #dcc.Graph(
                #id='hist_graph',
                #figure=jfig
                #) # ------------------- end histogram
            #]),

            # ----------------------- calling Map graph layer 1 -------------------------------
            dbc.Row([
                dbc.Col(html.Div(id='div_map_graph clear', children=[

                        html.H2(children='Layer 1 Map'),
                        html.Div(children= 'Turtle Track Map - Occurrence between 0 to -5 meters deep'),
                        dcc.Graph(
                            id='map_graph',
                            figure=jgomaptraceLayer1
                        )  # ------------------- end Map
                    ])
                )
            ]),

            dbc.Row([
                dbc.Col(html.Div(id='div_scatter_graph clear', children=[

                        html.H2(children='Scatter'),
                        html.Div(children= 'Depth Occurrence in %'),
                        dcc.Graph( # calling Scatter graph layer 1 -------------------------------
                                id='scatter_graph',
                                figure=jgoscattermap
                                ) # ------------------- end Scatter
                    ])
                )
            ]),




            
        ])

    ], className=' container_dashpage')


    # Initialize callbacks after our app is loaded
    # Pass dash_app as a parameter
    ##init_callbacks(dash_app)

    return dash_app.server # app is loaded

#def init_callbacks(dash_app):
    #@app.callback(
    # Callback input/output
    #)

    #def update_graph(rows):
        # Callback logic
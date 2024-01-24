from dash import dcc, html
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import pandas as pd


def build_layout():
    dataset = pd.read_csv("sensor_data_hours_updated.csv")
    years = set(dataset["Year"])
    load_figure_template('MORPH')

    return html.Div([
        html.Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css"),
        # Titlebar Segment
        dbc.Row([
            dbc.Col([
                html.H1('Beehive Visualizer'),
                html.Div([
                    html.A(href="https://github.com/Karidus-423", 
                        children=[
                            html.I(className="fab fa-github-alt fa-lg", style={"color": "#b3a100"})
                        ]
                    )
                ])
            ],
            className="titlebar",        
            width=12)
        ]),    
    

        # Graph and Upload data Segment
        # Graph and Upload data Segment
        dbc.Row([
            dbc.Col([
                html.H2("Graph"),
                html.Div(
                    dcc.Graph(id='isograph'),
                    className="graph"
                )
            ], lg=10, md=11),
            dbc.Col([
                dbc.Row([
                    html.Div([
                        html.H2("Upload Data", className="file_upload_header"),
                        dcc.Upload(
                            ['Drag and Drop or ', html.A('Select a File')],
                            className="upload_button",
                            id='upload-data',
                        ),
                    ]),
                    html.Div(id='upload-output')
                ]),
            ],lg=2, md=12)
        ], style={'padding-top': '50px', 'padding-left': '70px',
                  'max-width':'1080px'}),

        # Sliders Segment
        dbc.Row([
            dbc.Col([
                dbc.Row([
                        html.Div(
                            dcc.Input(id='submit',
                                      type='text',
                                      placeholder= "28, 40")), #layout and variables for button and input collection
                            html.Button('Submit',
                                        id='submit-val'),
                            html.Div(
                                        id='container-button-basic',
                                        children='Enter the temperatures you wish to see, seperated with a comma (,)'),
                ])
            ])
            ])
            # Year Column
            dbc.Col([
                dbc.Row([
                    html.Div([
                        html.H4("Years:"),
                        dcc.Slider(
                            id='years-slider',
                            min=min(years),
                            max=max(years),
                            step=1,
                            marks={year: str(year) for year in years},
                            value=min(years),
                            tooltip={
                                "placement": "bottom",
                                "always_visible": True
                            }
                        )
                    ])
                    
                ],style={
                    'padding-bottom':'30px'
                    }),
            
                # Month Column
                dbc.Row([
                    html.Div([
                        html.H4("Months:"),
                        dcc.Slider(
                            id='months-slider',
                            step=1,
                            value=1,  # Initial value for months (1 to 12)
                            tooltip={
                                "placement": "bottom",
                                "always_visible": True
                            },
                            included=True,
                            marks={
                                1:'1',
                                4:'4',
                                9:'9',
                                12:'12'
                            }
                        )
                    ])
                ])
            ],width=6),
        
            dbc.Col([
                dbc.Row([
                    html.H4("Days:"),
                    dcc.RangeSlider(
                        id='days-range-slider',
                        step=1,
                        tooltip={"placement": "bottom",
                                 "always_visible": True},
                        value=[1, 1],
                        allowCross= False
                    )
                ],style={
                    'padding-bottom':'30px'
                    }
                ),
                dbc.Row([
                    html.H4("Hours:"),
                    dcc.RangeSlider(
                        id='hours-range-slider',
                        step=1,
                        value=[0, 23],
                        marks={
                            0:'0',
                            6:'6',
                            12:'12',
                            18:'18',
                            23:'23',
                            },
                        tooltip={"placement": "bottom",
                                 "always_visible": True},
                    )
                ])
            ],width=6),
            # Footer Segment
            dbc.Row()
        ],style={#Style for sliders
                 'padding':'50px',
            }
        ),
    
    


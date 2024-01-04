import dash
import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.MORPH],
                meta_tags=[
                {"name": "viewport", "content": "width=device-width, initial-scale=1"}
                ]
                
)
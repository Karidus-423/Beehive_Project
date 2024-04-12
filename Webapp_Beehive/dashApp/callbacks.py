from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from scipy.interpolate import griddata
from datetime import datetime
import base64
from io import BytesIO
from maindash import app
from layout import build_layout



def initialize_variables():
    global years, months, days, hours, sensor_numbers,dataset  # Declare the variables as global
    dataset = pd.read_csv("../sensor_data_hours_updated.csv")
    years = set(dataset["Year"])
    months = set(dataset["Month"])
    days = set(dataset["Day"])
    hours = set(dataset["Hour"])
    sensor_numbers = set(dataset["Sensor_number"])
    
initialize_variables()
month_list = list(months)
    

datetime_objects = [datetime(year, month, day, hour) for year, month, day, hour in zip(years, months, days, hours)]
date_strings = [datetime(year, month, day, hour).strftime("%Y-%m-%d %H:%M:%S") for year, month, day, hour in zip(dataset["Year"], dataset["Month"], dataset["Day"], dataset["Hour"])]

unique_date_strings = set(date_strings)
unique_date_strings_list = list(unique_date_strings)

def custom_key(date_string):
    dt = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    return dt.strftime("%Y-%m-%d %H:%M:%S")

dates = sorted(unique_date_strings_list, key=custom_key)

initial_camera = dict(
    up=dict(x=0, y=0, z=1),
    center=dict(x=0, y=0, z=-1),
    eye=dict(x=6, y=5, z=3),
)

files_uploaded_count = 0

#Update Dataset
@app.callback(Output('upload-output','children'),
              [Input('upload-data','contents')],
              
)

def update_dataset_and_figures(contents):
    global dataset, years, months, days, hours, sensor_numbers, files_uploaded_count
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            # Load new dataset from uploaded contents
            new_data = pd.read_csv(BytesIO(decoded))
            dataset = new_data
            
            # Reinitialize global variables based on the new dataset
            years = set(dataset["Year"])
            months = set(dataset["Month"])
            days = set(dataset["Day"])
            hours = set(dataset["Hour"])
            sensor_numbers = set(dataset["Sensor_number"])
            
            files_uploaded_count += 1
            return 'Data Uploaded Successfully'
        except Exception as e:
            print(e)
            return 'Error processing the uploaded file.'
    return ''


@app.callback(
    Output('months-slider', 'min'),
    Output('months-slider', 'max'),
    Input('days-range-slider', 'value')
)
def update_hours_range_slider_marks(day_range):
    if len(month_list) == 1:
        minimum_month = maximum_month = month_list[0]
    else:
        minimum_month = min(month_list)
        maximum_month = max(month_list)
        
    return minimum_month, maximum_month


days_per_month = {
    1: 31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:30, 9:30, 10:31, 11:30, 12:31,
}
days_marks_dict = {
    28:{'1':'0', '15':'15' , '28':'28'},
    30: {'1':'0', '15':'15' , '30':'30'} , 
    31:{'1':'0', '15':'15' , '31':'31'}
}
@app.callback(
    Output('days-range-slider', 'marks'),
    Input('months-slider', 'value')
)
def update_days_range_slider_marks(value):
    num_days = days_per_month[value]
    days_marks = days_marks_dict[num_days]
    return days_marks


@app.callback(
    Output('hours-range-slider', 'min'),
    Output('hours-range-slider', 'max'),
    Input('days-range-slider', 'value')
)
def update_hours_range_slider_marks(day_range):
    minimum_hours = min(hours)
    maximum_hours = max(hours)
    return minimum_hours, maximum_hours


camera_params = initial_camera

@app.callback(
    Output('isograph', 'figure'),
    [Input('years-slider', 'value'),
    Input('months-slider', 'value'),
    Input('days-range-slider', 'value'),
    Input('hours-range-slider', 'value')]
)
def update_selected_dates(year_value, month_value, day_range, hour_range):
    selected_year = year_value
    selected_month = month_value
    
    # Convert the range slider values to datetime objects
    min_date = datetime(selected_year, selected_month, day_range[0], hour_range[0])
    max_date = datetime(selected_year, selected_month, day_range[1], hour_range[1])

    # Convert the dates in the 'dates' list to datetime objects
    dates_as_datetime = [datetime.strptime(date, "%Y-%m-%d %H:%M:%S") for date in dates]

    # Filter the dates within the selected range
    global selected_dates
    selected_dates = [date.strftime("%Y-%m-%d %H:%M:%S") for date in dates_as_datetime if min_date <= date <= max_date]
    
    
    first_timestamp = selected_dates[0]
    recording = dataset[dataset['Timestamp'] == first_timestamp]
    
    X = np.linspace(recording['X'].min(), recording['X'].max(), 50)
    Y = np.linspace(recording['Y'].min(), recording['Y'].max(), 50)
    Z = np.linspace(recording['Z'].min(), recording['Z'].max(), 20)
    
    x, y, z = np.meshgrid(X, Y, Z)

    points = np.array((recording['X'], recording['Y'], recording['Z'])).T
    temps = recording['Temperature']
    
    newdata = griddata(points, temps, (x, y, z), method='linear')
    
    # 3D graph content settings
    trace = go.Isosurface(
        x=x.flatten(),
        y=y.flatten(),
        z=z.flatten(),
        value=newdata.flatten(),
        colorscale= 'plasma',
        opacity=0.6,
        isomin=recording['Temperature'].min(),
        isomax=recording['Temperature'].max(),
        surface_count=5,
        caps=dict(x_show=False, y_show=False),
        colorbar=dict(
            title ="Temp:"
        )
    )
    
    # Create the figure dictionary
    figure = {
        'data': [trace],
        'frames': [],# List of traces
        'layout': {}  # Your layout settings (if any)
    }
    
    #Graph Slider
    sliders_dict = {
    'active': 0,
    'yanchor': 'top',
    'xanchor': 'left',
    'currentvalue': {
        'font': {'size': 20},
        'prefix': 'Date: ',
        'visible': True,
        'xanchor': 'right'
    },
    'transition': {'duration': 100, 'easing': 'cubic-in-out'},
    'pad': {'b': 10, 't': 50},
    'len': 0.9,
    'x': 0.1,
    'y': 0,
    'steps': []
    }
    
    figure['layout']['updatemenus'] = [
    {
        'buttons': [
            {
                'args': [None, {'frame': {'duration': 100, 'redraw': True},
                         'fromcurrent': True, 'transition': {'duration': 300, 'easing': 'quadratic-in-out'}}],
                'label': '▶',
                'method': 'animate'
            },
            {
                'args': [[None], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate',
                'transition': {'duration': 0}}],
                'label': '▐▐',
                'method': 'animate'
            }
        ],
        'direction': 'left',
        'pad': {'r': 10, 't': 87},
        'showactive': False,
        'type': 'buttons',
        'x': 0.1,
        'xanchor': 'right',
        'y': 0,
        'yanchor': 'top'
    }
]
    
    for date in selected_dates:
        frame = {'data': [], 'name': str(date)}
        recording = dataset[dataset['Timestamp'] == date]
        
        X = np.linspace(recording['X'].min(), recording['X'].max(), 50)
        Y = np.linspace(recording['Y'].min(), recording['Y'].max(), 50)
        Z = np.linspace(recording['Z'].min(), recording['Z'].max(), 20)
        
        x, y, z = np.meshgrid(X, Y, Z)

        points = np.array((recording['X'], recording['Y'], recording['Z'])).T
        temps = recording['Temperature']
        
        
        newdata = griddata(points, temps, (x, y, z), method='linear')
        
        # 3D graph content settings
        trace = go.Isosurface(
            x=x.flatten(),
            y=y.flatten(),
            z=z.flatten(),
            value=newdata.flatten(),
            opacity=0.6,
            colorscale='plasma',
            isomin=recording['Temperature'].min(),
            isomax=recording['Temperature'].max(),
            surface_count=5,
            caps=dict(x_show=False, y_show=False)
        )
        
        frame['data'].append(trace)
        
        figure['frames'].append(frame)
        
        slider_step = {
            'args': [
                [str(date)],
                {
                    'frame': {'duration': 10, 'redraw': True},
                    'mode': 'next',
                    'transition': {'duration': 10}
                }
            ],
            'label': str(date),
            'method': 'animate'
        }
        sliders_dict['steps'].append(slider_step)

        figure['layout']['sliders'] = [sliders_dict]
        
        
        
            
    return figure

# Refesh Graph
selected_day = [1,1]
@app.callback(
    Output('days-range-slider', 'value'),  
    [Input('upload-output', 'children')],
)
def update_selected_day(current_day):
    global selected_day, files_uploaded_count
    
    files_submitted = 0
    update_value = files_uploaded_count - files_submitted
    
    if update_value == 1:
        # Toggle the selected day between 1 and 2
        selected_day = [2,2] if current_day == [1,1] else [1,1]
        files_submitted += 1
    return selected_day

if __name__ == '__main__':
    app.layout = build_layout()
    app.run_server(debug=True)

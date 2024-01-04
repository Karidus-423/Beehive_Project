import pandas as pd
dataset = pd.read_csv("sensor_data_hours_updated.csv")

years = set(dataset["Year"])
months = set(dataset["Month"])
days = set(dataset["Day"])
hours = set(dataset["Hour"])
sensor_numbers = set(dataset["Sensor_number"])

years_list = list(years)


print(len(years_list))


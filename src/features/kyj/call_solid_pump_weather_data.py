import pandas as pd

def load_solid_pump_data():
    solid_pump_df = pd.read_csv('../../../data/processed/solid_pump_data.csv')
    return solid_pump_df

def load_weather_rain_data():
    weather_rain_df = pd.read_csv('../../../data/processed/weather_rain_data.csv')
    return weather_rain_df
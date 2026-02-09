import pandas as pd

def load_solid_pump_data():
    solid_pump_df = pd.read_csv('./data/solid_pump_data.csv')
    return solid_pump_df
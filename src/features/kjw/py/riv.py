# features/kjw/py/riv.py
# py/riv.py

#import 함수 생성
# src/features/kjw/py/riv.py
from pathlib import Path
import pandas as pd

def load_river_df():
    base_dir = Path(__file__).resolve().parents[4]
    file_path = base_dir / "data" / "processed" / "riv_pro_df.csv"
    return pd.read_csv(file_path)

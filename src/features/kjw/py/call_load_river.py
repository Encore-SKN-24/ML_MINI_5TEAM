# src/features/kjw/py/call_load_river.py

# 테스트용 파일
# riv.py에 정의된 load_river_df() 함수가
# 정상적으로 import 및 실행되는지 확인하기 위한 파일

# 실행 방법 (프로젝트 루트에서):
# python -m src.features.kjw.py.call_load_river

from src.features.kjw.py.riv import load_river_df

if __name__ == "__main__":
    river_df = load_river_df()
    print(river_df.head())


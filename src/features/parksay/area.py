import pandas as pd
import os
from pathlib import Path

def get_merged_area_csv():
    
    # 루트 디렉토리 경로 
    _PROJECT_ROOT = Path(__file__).resolve().parent
    while not (_PROJECT_ROOT / ".git").exists() and _PROJECT_ROOT != _PROJECT_ROOT.parent:
        _PROJECT_ROOT = _PROJECT_ROOT.parent


    # 경로 선언
    _PATH_SIDO = _PROJECT_ROOT/"data/raw/sido.txt"
    _PATH_SIGUNGU = _PROJECT_ROOT/"data/raw/sigungu.txt"
    _PATH_OUTPUT = _PROJECT_ROOT/"data/processed/area.csv"
    
    # 피처 이름 선언
    _SIDO = "SIDO"
    _SIGUNGU = "SIGUNGU"
    _SIDO_NAME = "SIDO_NAME"
    _SIGUNGU_NAME = "SIGUNGU_NAME"


    # 1. 시도 데이터 로드
    df_sido = pd.read_csv(_PATH_SIDO, 
                         header=None, 
                         names=[_SIDO, _SIDO_NAME], 
                         quotechar="'", 
                         skipinitialspace=True)

    # 2. 시군구 데이터 로드
    df_sigungu = pd.read_csv(_PATH_SIGUNGU, 
                             header=None, 
                             names=[_SIGUNGU, _SIDO, _SIGUNGU_NAME], 
                             quotechar="'", 
                             skipinitialspace=True)

    # 3. 데이터 병합 ( _SIDO 기준)
    df_merged = pd.merge(df_sido, df_sigungu, on=_SIDO, how='inner')

    # 4. 전체 지역명 피처 추가 (시도 + 시군구)
    df_merged['AREA_NAME'] = df_merged[_SIDO_NAME] + " " + df_merged[_SIGUNGU_NAME]

    # 5. CSV 파일로 저장 
    os.makedirs(os.path.dirname(_PATH_OUTPUT), exist_ok=True) # 저장 폴더가 없다면 생성
    df_merged.to_csv(_PATH_OUTPUT, index=False) # csv 파일에 인덱스 제외

    # 6. 인덱스 초기화된 데이터프레임 반환
    return df_merged.reset_index(drop=True)

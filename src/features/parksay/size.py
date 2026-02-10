
from pathlib import Path
from area import get_merged_area_csv
from normalize_area import normalize_area_name
import pandas as pd
import numpy as np

def add_size_feature(df_main=None):

    # 루트 디렉토리 경로 
    _PROJECT_ROOT = Path(__file__).resolve().parent
    while not (_PROJECT_ROOT / ".git").exists() and _PROJECT_ROOT != _PROJECT_ROOT.parent:
        _PROJECT_ROOT = _PROJECT_ROOT.parent
    # 상수 선언
    _PATH_SIZE = _PROJECT_ROOT/"data/raw/size.csv"
    _SIDO = "SIDO_NAME"
    _SIGUNGU = "SIGUNGU_NAME"

    # 넣어주는 파라미터 없으면 area 불러오기
    if df_main is None:
        df_main = get_merged_area_csv()
    # size csv 파일 불러오기
    df_size = pd.read_csv(_PATH_SIZE, index_col=False) 
    # 면적 값에서 콤마를 제거하고 자료형을 문자열에서 float 자료형으로 변경
    df_size["AREA_SIZE"] = ( df_size["AREA_SIZE"].str.replace(",", "", regex=False) ).astype(float)
    # '전체' 항목 이름 변경
    df_size[_SIGUNGU]  = np.where(df_size[_SIGUNGU] == df_size[_SIDO], "전체", df_size[_SIGUNGU] )
    # 시도 항목 이름 정규화
    df_size[_SIDO] = df_size[_SIDO].apply(normalize_area_name)
    # 시군구 항목 이름 정규화
    df_size[_SIGUNGU] = df_size[_SIGUNGU].str.replace(r".*시\s*(\S*구)", r"\1", regex=True)
    df_size[_SIGUNGU] = df_size[_SIGUNGU].str.replace(r"(.*시) 전체", r"\1", regex=True)

    # 예외 처리
    exceptions = {"세종특별자치시": "세종특별자치시"} # 더 추가 가능
    for sido, sigungu in exceptions.items(): 
        df_add = df_size.loc[(df_size[_SIDO] == sido) & (df_size[_SIGUNGU] == "전체")].copy()
        df_add[_SIGUNGU] = sigungu
        df_size = pd.concat([df_size, df_add], ignore_index=True)

    # df 합치기
    df_merged = pd.merge(df_main, df_size, on=[_SIDO, _SIGUNGU], how='left')

    return df_merged

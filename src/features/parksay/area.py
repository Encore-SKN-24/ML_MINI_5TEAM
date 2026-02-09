import pandas as pd
import os

def get_merged_area_csv():
    
    sido_path="./data/raw/sido.txt"
    sigungu_path="./data/raw/sigungu.txt"
    save_path="./data/processed/area.csv"
    
    # 1. 시도 데이터 로드
    df_sido = pd.read_csv(sido_path, 
                         header=None, 
                         names=['CTPRVN_CD', 'CTPRVN_NAME'], 
                         quotechar="'", 
                         skipinitialspace=True)

    # 2. 시군구 데이터 로드
    df_sigungu = pd.read_csv(sigungu_path, 
                             header=None, 
                             names=['SGG_CD', 'CTPRVN_CD', 'SGG_NAME'], 
                             quotechar="'", 
                             skipinitialspace=True)

    # 3. 데이터 병합 (CTPRVN_CD 기준)
    df_merged = pd.merge(df_sido, df_sigungu, on='CTPRVN_CD', how='inner')

    # 4. 전체 지역명 피처 추가 (시도 + 시군구)
    df_merged['AREA_NAME'] = df_merged['CTPRVN_NAME'] + " " + df_merged['SGG_NAME']

    # 5. CSV 파일로 저장 
    os.makedirs(os.path.dirname(save_path), exist_ok=True) # 저장 폴더가 없다면 생성
    df_merged.to_csv(save_path, index=False) # csv 파일에 인덱스 제외

    # 6. 인덱스 초기화된 데이터프레임 반환
    return df_merged.reset_index(drop=True)

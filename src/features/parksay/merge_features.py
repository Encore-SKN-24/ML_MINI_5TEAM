import pandas as pd
from pathlib import Path


# 각 csv 파일 뽑아서 df 하나에 피처 통합하기
def load_and_merge_data():
    # 루트 디렉토리 경로 
    _PROJECT_ROOT = Path(__file__).resolve().parent
    while not (_PROJECT_ROOT / ".git").exists() and _PROJECT_ROOT != _PROJECT_ROOT.parent:
        _PROJECT_ROOT = _PROJECT_ROOT.parent

    # dict 선언: key는 데이터셋 이름, value는 path와 features를 가진 dict
    file_dict = {
        # "rain": {"path": _PROJECT_ROOT/"data/raw/rain.csv", "features": ["DAM_DAY_RNFL", "DATE"]},
        "river": {"path": _PROJECT_ROOT/"data/raw/river.csv", "features": ["RIVER_SE", "DISTANCE"]},
        # "soil": {"path": _PROJECT_ROOT/"data/raw/soil.csv", "features": ["SOILDRA", "AREA"]},
        "area": {"path": _PROJECT_ROOT/"data/processed/area.csv", "features": ["SIDO","SIDO_NAME","SIGUNGU","SIGUNGU_NAME","AREA_NAME",]}
    }

    # 최종 완성한 csv 파일 저장할 경로
    output_path = _PROJECT_ROOT/"data/processed/data.csv"

    # 최종 완성할 df
    merged_df = None

    # 공통 변수 이름
    SIDO, SIGUNGU = "SIDO", "SIGUNGU"

    # 각 파일을 불러와서 필요한 변수만 추출 후 병합
    for key, file_item in file_dict.items():
        file_path = file_item["path"]
        file_features = file_item["features"]

        # 기본적으로 CTPRVN_CD, SGG_CD는 항상 포함
        cols_to_use = [SIDO, SIGUNGU] + file_features
        df = pd.read_csv(file_path, usecols=cols_to_use)

        # 최초 실행 때는 df 가 null인 상태라 초기화 넣어줌
        if merged_df is None:
            merged_df = df
        else:
            # CTPRVN_CD, SGG_CD 기준으로 병합
            merged_df = pd.merge(merged_df, df, on=[SIDO, SIGUNGU], how="outer")
    merged_df.reset_index(drop=True)
    merged_df.to_csv(output_path, index=False)
    return merged_df

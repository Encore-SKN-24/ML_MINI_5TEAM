"""
침수 데이터 로더 (Flood Data Loader)

sklearn.datasets 스타일의 데이터 로딩 함수를 제공합니다.

Functions:
    save_flood_simple_data: 원본 데이터에서 간소화 데이터셋 생성 및 저장
    load_flood_data: 저장된 간소화 데이터셋 로드

Examples:
    >>> from src.features.ljh.flood.loader import save_flood_simple_data, load_flood_data
    >>>
    >>> # 데이터 저장
    >>> save_flood_simple_data()
    >>>
    >>> # 데이터 로드
    >>> data = load_flood_data()
    >>> X, y = load_flood_data(return_X_y=True)
"""

import os
import pandas as pd

# 기본 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_FILE_PATH = os.path.join(BASE_DIR, '../../../../data/raw/flood_area.csv')
PROCESSED_DIR = os.path.join(BASE_DIR, '../../../../data/processed')
START_YEAR = 2016


def save_flood_simple_data(input_file=None, output_file=None):
    """
    원본 침수 데이터에서 핵심 컬럼만 추출하여 간소화 데이터셋 생성 및 저장

    Parameters
    ----------
    input_file : str, optional
        입력 CSV 파일 경로 (기본값: data/raw/flood_area.csv)

    output_file : str, optional
        출력 CSV 파일 경로 (기본값: data/processed/flood_area.csv)

    Returns
    -------
    DataFrame
        저장된 간소화 데이터셋
        컬럼: SIGUNGU, FLOOD_YEAR, FLOOD_MONTH, FLOOD_AREA

    Examples
    --------
    >>> # 기본 경로로 저장
    >>> data = save_flood_simple_data()

    >>> # 커스텀 경로로 저장
    >>> data = save_flood_simple_data(
    ...     input_file='./my_flood_data.csv',
    ...     output_file='./output/flood_area.csv'
    ... )
    """

    # 기본 경로 설정
    if input_file is None:
        input_file = RAW_FILE_PATH

    if output_file is None:
        os.makedirs(PROCESSED_DIR, exist_ok=True)
        output_file = os.path.join(PROCESSED_DIR, 'flood_area.csv')

    # 원본 데이터 로드
    print(f"📂 원본 데이터 로딩: {input_file}")
    raw_data = pd.read_csv(input_file)

    # 연도 필터링 (2016년 이후)
    raw_data['FLDN_YR_num'] = pd.to_numeric(raw_data['FLDN_YR'], errors='coerce')
    filtered_data = raw_data[raw_data['FLDN_YR_num'] >= START_YEAR].copy()

    # 날짜 변환
    filtered_data['FLDN_BGNG_DATE'] = pd.to_datetime(
        filtered_data['FLDN_BGNG_YMD'],
        format='%Y%m%d',
        errors='coerce'
    )

    # 필요한 컬럼만 추출
    simple_data = pd.DataFrame({
        'SIGUNGU': filtered_data['STDG_SGG_CD'].astype('int32'),
        'FLOOD_YEAR': filtered_data['FLDN_YR_num'].astype('int16'),
        'FLOOD_MONTH': filtered_data['FLDN_BGNG_DATE'].dt.month.fillna(0).astype('int8'),
        'FLOOD_AREA': filtered_data['FLDN_AREA'].astype('float32')
    })

    # 중복 제거 (동일 시군구/연도/면적)
    dedup_keys = ['SIGUNGU', 'FLOOD_YEAR', 'FLOOD_AREA']
    simple_data = simple_data.drop_duplicates(subset=dedup_keys, keep='first')

    # CSV 저장
    simple_data.to_csv(output_file, index=False, encoding='utf-8-sig')

    print(f"✅ 저장 완료: {output_file}")
    print(f"   - 레코드 수: {len(simple_data):,}개")
    print(f"   - 파일 크기: {os.path.getsize(output_file) / 1024:.2f} KB")
    print(f"   - 시군구 수: {simple_data['SIGUNGU'].nunique()}개")
    print(f"   - 연도 범위: {simple_data['FLOOD_YEAR'].min()}~{simple_data['FLOOD_YEAR'].max()}")

    return simple_data


def load_flood_data(data_file=None, return_X_y=False, as_frame=True):
    """
    침수 데이터를 로드하는 함수 (sklearn.datasets.load_iris 스타일)

    Parameters
    ----------
    data_file : str, optional
        데이터 파일 경로 (기본값: data/processed/flood_area.csv)

    return_X_y : bool, default=False
        True일 경우 (X, y) 튜플 반환
        False일 경우 전체 DataFrame 반환

    as_frame : bool, default=True
        True일 경우 pandas DataFrame 반환
        False일 경우 numpy array 반환

    Returns
    -------
    data : DataFrame or ndarray
        return_X_y=False일 때 전체 데이터 반환

    (X, y) : tuple of DataFrame or ndarray
        return_X_y=True일 때 반환
        X: SIGUNGU, FLOOD_YEAR, FLOOD_MONTH
        y: FLOOD_AREA

    Examples
    --------
    >>> # 전체 데이터 로드
    >>> data = load_flood_data()
    >>> print(data.head())

    >>> # 학습용 X, y 분리
    >>> X, y = load_flood_data(return_X_y=True)
    >>> print(X.shape, y.shape)

    >>> # NumPy 배열로 로드
    >>> X, y = load_flood_data(return_X_y=True, as_frame=False)
    >>> print(type(X), type(y))
    """

    # 기본 경로 설정
    if data_file is None:
        data_file = os.path.join(PROCESSED_DIR, 'flood_area.csv')

    # CSV 파일 로드
    if not os.path.exists(data_file):
        raise FileNotFoundError(
            f"❌ 데이터 파일을 찾을 수 없습니다: {data_file}\n"
            f"save_flood_simple_data()를 먼저 실행하세요."
        )

    df = pd.read_csv(data_file)

    if return_X_y:
        # Feature와 Target 분리
        X = df[['SIGUNGU', 'FLOOD_YEAR', 'FLOOD_MONTH']]
        y = df['FLOOD_AREA']

        if not as_frame:
            return X.values, y.values
        return X, y

    else:
        # 전체 데이터 반환
        if not as_frame:
            return df.values
        return df


if __name__ == "__main__":
    # 스크립트로 직접 실행 시 테스트
    print("="*60)
    print("침수 데이터 유틸리티 함수 테스트")
    print("="*60)

    # 1. 데이터 저장
    print("\n[1] 데이터 저장")
    simple_data = save_flood_simple_data()

    # 2. 데이터 로드
    print("\n[2] 데이터 로드")
    data = load_flood_data()
    print(f"✓ Shape: {data.shape}")
    print(data.head())

    # 3. X, y 분리
    print("\n[3] X, y 분리")
    X, y = load_flood_data(return_X_y=True)
    print(f"✓ X shape: {X.shape}, y shape: {y.shape}")

    print("\n" + "="*60)
    print("✅ 테스트 완료!")
    print("="*60)

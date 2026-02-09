import os
import requests
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_URL = 'https://www.safetydata.go.kr/V2/api/DSSP-IF-00117'
SERVICE_KEY = os.getenv('FLOOD_API_KEY')

PROJECT_ROOT = Path(__file__).resolve().parents[4]
OUTPUT_PATH = PROJECT_ROOT / 'data' / 'raw' / 'flood_area.csv'


def _parse_response(payload):
    """
    API 응답 JSON 파싱

    Args:
        payload: API 응답 JSON

    Returns:
        items: 데이터 리스트
        total_count: 전체 데이터 수
    """
    items = payload.get('body')
    total_cnt = payload.get('totalCount')
    return items, total_cnt


def fetch_flood_data(page_no=1, num_of_rows=200):
    """
    행안부 침수 데이터 수집

    Args:
        page_no: 페이지 번호 (기본값: 1)
        num_of_rows: 한 페이지 결과 수 (기본값: 100)

    Returns:
        tuple: (pd.DataFrame, total_count) - 침수 데이터와 전체 데이터 수
    """
    if not SERVICE_KEY:
        raise ValueError('[CRAWL_FLOOD] FLOOD_API_KEY 환경변수 설정 필요')
  
    params = {
        'serviceKey': SERVICE_KEY,
        'returnType': 'json',
        'pageNo': page_no,
        'numOfRows': num_of_rows,
    }

    # 1. API 호출
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        payload = response.json()

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f'[CRAWL_FLOOD] API 호출 오류: {e}')
    except ValueError as e:
        raise RuntimeError(f'[CRAWL_FLOOD] JSON 파싱 오류: {e}')

    # 2. 응답 파싱
    items, total_cnt = _parse_response(payload)

    return pd.DataFrame(items), total_cnt


def save_flood_data(output_path=OUTPUT_PATH, max_rows=None):
    """
    침수 데이터를 수집하여 data/raw/ 에 CSV로 저장

    Args:
        output_path: 저장 경로 (default: 기본 OUTPUT_PATH 사용)
        fetch_all: True면 모든 데이터 수집, False면 첫 페이지만 (default: True)
        max_rows: 최대 수집 행 수 (default: None)
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    print(f'[CRAWL_FLOOD] 침수 데이터 수집 시작: {output_path}')
    
    ROWS_PER_PAGE = 1000
    df_init, total_cnt = fetch_flood_data(page_no=1, num_of_rows=ROWS_PER_PAGE)
    all_dfs = [df_init]

    print(f'[CRAWL_FLOOD] 전체 데이터 수: {total_cnt}')

    # 마지막 페이지 수집
    if not max_rows or len(df_init) < max_rows:
        total_pages = (total_cnt + ROWS_PER_PAGE - 1) // ROWS_PER_PAGE

        # 나머지 페이지 수집
        for page_no in range(2, total_pages + 1):
            try:
                df_page, _ = fetch_flood_data(page_no=page_no, num_of_rows=ROWS_PER_PAGE)
                all_dfs.append(df_page)

                current_total = sum(len(d) for d in all_dfs)
                print(f'[CRAWL_FLOOD] 페이지 {page_no}/{total_pages} 수집 완료 (누적: {current_total}개)')

                # 최대 행 수 제한 적용
                if max_rows and current_total >= max_rows:
                    break
            except Exception as e:
                raise RuntimeError(f'[CRAWL_FLOOD] 페이지 {page_no} 수집 실패: {e}')

    df = pd.concat(all_dfs, ignore_index=True)

    if max_rows:
        df = df.head(max_rows)

    df.to_csv(path, index=False, encoding='utf-8-sig')
    print(f'[CRAWL_FLOOD] 침수 데이터 수집 완료: {path}')


if __name__ == '__main__':
    save_flood_data()
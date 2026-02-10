
import re

def normalize_area_name(param):
    param = re.sub(r"서울.*", '서울특별시', param)
    param = re.sub(r"부산.*", '부산광역시', param)
    param = re.sub(r"대구.*", '대구광역시', param)
    param = re.sub(r"인천.*", '인천광역시', param)
    param = re.sub(r"광주.*", '광주광역시', param)
    param = re.sub(r"대전.*", '대전광역시', param)
    param = re.sub(r"울산.*", '울산광역시', param)
    param = re.sub(r"세종.*", '세종특별자치시', param)
    param = re.sub(r"경기.*", '경기도', param)
    param = re.sub(r"강원.*", '강원도', param)
    param = re.sub(r"충.*?북.*", '충청북도', param)
    param = re.sub(r"충.*?남.*", '충청남도', param)
    param = re.sub(r"전.*?북.*", '전라북도', param)
    param = re.sub(r"전.*?남.*", '전라남도', param)
    param = re.sub(r"경.*?북.*", '경상북도', param)
    param = re.sub(r"경.*?남.*", '경상남도', param)
    param = re.sub(r"제주.*", '제주특별자치도', param)
    return param


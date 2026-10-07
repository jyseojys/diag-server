import csv
import json
import urllib.request
import os
from datetime import datetime
import io

# 💡 설정 경로 (현재 환경에 맞춤)
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1Mp29BiPkXHhx072zapWP6Z7oHK62MzLcYAL2OLjDJ0g/export?format=csv&gid=0"
BASE_DIR = "/Users/seojaeyong/projects/dart_project/diagbox_extract_file/diag-server"
I18N_DIR = os.path.join(BASE_DIR, "i18n")
VERSION_FILE = os.path.join(BASE_DIR, "version_i18n.txt")

def update_i18n():
    print("🌐 구글 시트 다운로드 중...")
    response = urllib.request.urlopen(SHEET_CSV_URL)
    lines = [l.decode('utf-8') for l in response.readlines()]
    reader = list(csv.reader(lines))
    
    headers = reader[0]
    
    # C열(인덱스 2)부터 언어 코드 읽기
    for col in range(2, len(headers)):
        lang_code = headers[col].strip()
        if not lang_code: continue
        
        json_obj = {}
        for row in range(1, len(reader)):
            if len(reader[row]) <= col: continue
            key = reader[row][0].strip()
            value = reader[row][col].strip()
            
            if key:
                json_obj[key] = value
                
        # JSON 파일 저장
        file_path = os.path.join(I18N_DIR, f"{lang_code}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(json_obj, f, ensure_ascii=False, indent=2)
        print(f"✅ 생성 완료: {lang_code}.json")

    # 버전 파일 업데이트 (예: 20261007_1530)
    new_version = datetime.now().strftime("%Y%m%d_%H%M")
    with open(VERSION_FILE, 'w', encoding='utf-8') as f:
        f.write(new_version)
    print(f"🚀 버전 업데이트 완료: i18n_version.txt ({new_version})")

if __name__ == "__main__":
    if not os.path.exists(I18N_DIR):
        os.makedirs(I18N_DIR)
    update_i18n()
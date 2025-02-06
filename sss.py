import sys
import argparse
from datetime import datetime, timedelta

# Jupyter Notebook에서 실행할 때 sys.argv 처리
if "--f" in sys.argv:
    sys.argv = [sys.argv[0]]  # Jupyter가 추가한 불필요한 인수 제거

parser = argparse.ArgumentParser()
parser.add_argument('--date', type=str, help="날짜 입력 (예: 24_06_01)")

# 입력 값이 없으면 오늘 날짜 기본값 사용
args, unknown = parser.parse_known_args()
today_date = args.date if args.date else datetime.today().strftime("%y_%m_%d")

print(f"오늘 날짜: {today_date}")

# 이전 달 확인 로직
check_last_month = False
if int(today_date[-2:]) < 7:
    check_last_month = True

print(f"Check last month: {check_last_month}")
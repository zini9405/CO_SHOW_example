import os
import datetime
import paramiko
from datetime import datetime, timedelta
from argparse import ArgumentParser
import sys

# Jupyter Notebook에서 실행할 때 sys.argv 문제 해결
if "--f" in sys.argv:
    sys.argv = [sys.argv[0]]  # Jupyter 자동 추가 인수 제거

parser = ArgumentParser()
parser.add_argument('--date', type=str, help="조회할 날짜 입력 (예: 24_06_01)")
args, unknown = parser.parse_known_args()

# 오늘 날짜 가져오기 (기본값: 오늘 날짜)
today_date = args.date if args.date else datetime.today().strftime("%y_%m_%d")

# SSH 설정
host = "10.150.9.121" 
port = 22 
userId = "sksl_ds02"  
password = 'sksl_ds02!'  

SSH_Client = paramiko.SSHClient()
SSH_Client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
SSH_Client.connect(
    hostname=host,
    port=port,
    username=userId,
    password=password,
    look_for_keys=False
)

sftp_client = SSH_Client.open_sftp()

# ✅ 3개월 전까지 조회하도록 변경
x_dir_list = []

for i in range(3):  # 3개월 전까지 반복
    month_date = datetime.strptime(today_date, '%y_%m_%d') - timedelta(weeks=4 * i)  # 한 달씩 감소
    month_folder = month_date.strftime('%y_%m')  # "YY_MM" 형식으로 변환

    remote_x_path = f'/home/sksl_ds02/ANALYSIS_DATA_SET/X_TEMP/3200_WIRE_SAW/{month_folder}'
    
    try:
        dirs = sftp_client.listdir(remote_x_path)
        x_dir_list.extend(dirs)
        print(f"📂 {month_folder} 폴더에서 {len(dirs)}개 디렉토리 가져옴")
    except FileNotFoundError:
        print(f"⚠️ {month_folder} 폴더 없음 (건너뜀)")

sftp_client.close()
SSH_Client.close()

# 결과 출력
print(f"\n📌 총 {len(x_dir_list)}개 디렉토리 조회 완료")
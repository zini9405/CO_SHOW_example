import re

# 자연스러운 정렬을 위한 키 생성 함수
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)', s)]

# JSON 파일 읽기
with open("EQP_ID_MODULE_NAME.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

# 리스트 데이터 추출
eqp_id_module_list = data["EQP_ID_MODULE_NAME"]

# 자연스러운 정렬
sorted_list = sorted(eqp_id_module_list, key=natural_sort_key)

# 결과 출력
print("정렬된 리스트:")
print(sorted_list)
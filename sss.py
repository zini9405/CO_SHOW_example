6100_process 디렉토리
6300_process 디렉토리
const_dataset_process 디렉토리
각 디렉토리에 24_01, 24_02, 24_03, ... 25_02까지 csv 파일이 존재해.

3개의 디렉토리를 확인하고 csv 파일명이 같으면, 6300_process 디렉토리의 csv 파일은 WAFER_ID, GBIR_AFS2열만 추출함.
6100_process의 csv 파일의 WAF_ID열과 6300_process 디렉토리의 csv 파일의 WAFER_ID(WAF_ID)과 동일한 행만 합쳐서 선택함.
그리고 6100_process과 6300_process 합쳐진 데이터 파일의 WAF_ID와 const_dataset_process 디렉토리의 csv 파일 WAF_ID랑 동일한 행을 합쳐서 최종파일로 만들어줘.

예시) 6100_process의 24_01, 6300_process의 24_01, const_dataset_process의 24_01을 선택함.
6300_process의 24_01 csv 파일 WAFER_ID, GBIR_AFS2열만 추출함.
6100_process의 24_01 csv 파일  WAF_ID열과 6300_process 24_01 csv 파일의 WAFER_ID(WAF_ID)과 동일한 행만 합쳐서 선택함(com_x).
그리고 (com_x) WAF_ID열 값과 const_dataset_process 24_01 csv 파일의  WAF_ID열 값과 동일한 행을 합쳐서 최종파일로 만들어줘.

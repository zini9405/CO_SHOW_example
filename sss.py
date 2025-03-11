dataloader 만들기

1. STEP.csv를 읽기
2. BASE_DT열을 오름차순으로 정렬하고 WAF_ID열도 오름차순으로 정렬
3. WAF_ID열을 그룹화하여 STEP_ID를 오름차순으로 정렬
4. 그 후, 순서섞지 말고 데이터를 90:10 비율로 데이터 나눠죠
5. WAF_ID로 그룹화하고 그룹화가 하나의 데이터 입력으로 구성돼. (단 GBIR_AFS2열은 label, WAF_ID, BASE_DT, PAD_TEMP_STEP_MEAN열은 제거, EQP_ID는 text라서 숫자로 변경)
6. EQP_ID는 따로 만들어서 임베딩할거야. nn.Embedding
7. 그럼 입력 사이즈는 (B, L, 변수열 수)로 나오게 데이터 로더 만들어줘.

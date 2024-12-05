STEP 순서

0	Prestep
1	PURGE
2	RAMP_UP
3	BAKE1
4	BAKE2
5	PRE_ETCH
6	PRE_DEPO
7	DEPO
8	POST_PURGE
9	COOL1
10	COOL2
11	COOL3
12	Poststep

위에는 STEP 순서야.
나는 불필요한 값을 제거하고 잘못된 값들을 수정할거야. 그리고 WAP_ID열로 그룹해서 STEP 순서대로 정렬할거야. 만약에 STEP 순서인 0에서 12까지 값이 없으면 채워줘.

1. WAP_ID열로 그룹
2. 그룹된 값에 'STEP_NAME'열에 'BAKE3', 'COOL', 'COOL 1', 'COOL 2', 'COOL 3', 'PURGE 1', 'PURGE 2', 'PURGE1', 'PURGE2', 'PURGE3', 'PURGE4', 'STAB' 하나라도 포함되어 있으면 그룹 삭제
3. 'POST PURGE' -> 'POST_PURGE' / 'PRE DEPO' -> PRE_DEPO / 'PREDEPO' -> 'PRE_DEPO' / 'Pre DEPO' -> 'PRE_DEPO' / 'PRE_VENT' -> 'PRE_DEPO' / 'PRE_VETN' -> 'PRE_DEPO' / 'PRE ETCH' -> 'PRE_ETCH' / 'PRE ETCH1' -> 'PRE_ETCH' / 'PRE_ETCH1' -> 'PRE_ETCH' / 'PRE_ETCH2' -> 'PRE_ETCH'
 / 'ETCH' -> 'PRE_ETCH' / 'RAMP UP' -> 'RAMP_UP'로  이름 변경
4. 정리된 그룹별로  'STEP_NAME'에 STEP 순서인 0에서 12까지 값이 없으면 채워줘. 단, 'EQP_ID','MODULE_NAME','WAF_ID','RECIPE_ID,'HST_REG_DTTM' 값은 동일하게 채워주고 나머지 열은 -20으로 채워줘
5. 그룹으로 나눠진 값들을 다시 하나로 합쳐줘

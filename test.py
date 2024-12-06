import pandas as pd
import os

# STEP 순서 정의
step_order = {
    0: 'Prestep',
    1: 'PURGE',
    2: 'RAMP_UP',
    3: 'BAKE1',
    4: 'BAKE2',
    5: 'PRE_ETCH',
    6: 'PRE_DEPO',
    7: 'DEPO',
    8: 'POST_PURGE',
    9: 'COOL1',
    10: 'COOL2',
    11: 'COOL3',
    12: 'Poststep'
}

생성된 그룹을 보면, 0부터 12까지 순서가 안 맞아.

0   CENC17           A  3KKLD133SAF0      1.0    S14_CA        0     Prestep   
1   CENC17           A  3KKLD133SAF0      1.0    S14_CA        1       PURGE   
2   CENC17           A  3KKLD133SAF0      1.0    S14_CA        2     RAMP_UP   
3   CENC17           A  3KKLD133SAF0      1.0    S14_CA        3       BAKE1   
4   CENC17           A  3KKLD133SAF0      1.0    S14_CA        4       BAKE2   
5   CENC17           A  3KKLD133SAF0      1.0    S14_CA        5    PRE_DEPO   
6   CENC17           A  3KKLD133SAF0      1.0    S14_CA        6        DEPO   
7   CENC17           A  3KKLD133SAF0      1.0    S14_CA        7  POST_PURGE   
8   CENC17           A  3KKLD133SAF0      1.0    S14_CA        8       COOL1   
9   CENC17           A  3KKLD133SAF0      1.0    S14_CA        9       COOL2   
10  CENC17           A  3KKLD133SAF0      1.0    S14_CA       10       COOL3   
11  CENC17           A  3KKLD133SAF0      1.0    S14_CA       11    Poststep   
12  CENC17           A  3KKLD133SAF0    -20.0    S14_CA       12    Poststep  

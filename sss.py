a.csv 파일에 name이라는 열에 동일한 값이 있어. 하지만 code열은 달라 그리고 나머지 열은 다른 값을 가져. 그래서 나는 이걸 한 행으로 표현하고 싶어서 code열 값을 나머지 열 이름 앞에 추가해서 새로운 열을 만들거야.

예시) 
name code var1 var2 var3 ...
abc a 1 2, 4
abc b 1.1, 2.2, 4.4
abc c 2.3, 4.5, 1.3

이걸 
name a_code a_var1 a_var2 a_var3, b_var1, b_var2, b_var3 
abc a, 1, 2, 4 1.1, 2.2, 4.4

이런식으로 만들고 싶어 코드 구현해줘.

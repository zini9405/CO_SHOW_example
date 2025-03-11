if "step" in df.columns:
                df["step"] = pd.to_numeric(df["step"], errors="coerce")  # 변환 불가능한 값은 NaN 처리
                df = df[df["step"].isin(valid_steps)]
            else:
                print(f"[경고] {file_name}: 'step' 컬럼 없음, 필터링 건너뜀.")

            # 필요한 컬럼만 선택
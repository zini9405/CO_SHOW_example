   if "STEP_ID" in df.columns:
                df = df.drop_duplicates(subset=["WAF_ID", "STEP_ID"], keep="first")

            # 파일 저장
            output
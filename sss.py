import pandas as pd
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def visualize_and_save_eqp_embedding(model, eqp_mapping, csv_file):
    """
    EQP_ID_MODULE_NAME 임베딩 시각화 및 결과 저장
    """
    # 1. EQP_ID_MODULE_NAME의 임베딩 벡터를 추출
    embedding_weights = model.eqp_embedding.weight.detach().cpu().numpy()

    # 2. t-SNE를 사용하여 2D로 차원 축소
    tsne = TSNE(n_components=2, random_state=42)
    reduced_embeddings = tsne.fit_transform(embedding_weights)

    # 3. X, Y 값을 0과 1 사이로 변환
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_embeddings = scaler.fit_transform(reduced_embeddings)

    # 4. EQP_ID_MODULE_NAME 레이블 가져오기
    eqp_labels = list(eqp_mapping.keys())

    # 5. 결과를 데이터프레임으로 저장
    embedding_df = pd.DataFrame({
        "EQP_NM": eqp_labels,
        "X": scaled_embeddings[:, 0],
        "Y": scaled_embeddings[:, 1]
    })

    # 6. all.csv 파일 읽기
    all_df = pd.read_csv(csv_file)

    # 7. 각 EQP_NM의 ZDDFRONTMEAN_01_AFS2 평균값 계산 후 ZDD 열 추가
    zdd_values = all_df.groupby("EQP_ID_MODULE_NAME")["ZDDFRONTMEAN_01_AFS2"].mean().rename("ZDD")
    embedding_df = embedding_df.merge(zdd_values, left_on="EQP_NM", right_index=True, how="left")

    # 8. 결과를 저장
    output_csv = "embedding_results.csv"
    embedding_df.to_csv(output_csv, index=False)
    print(f"Embedding results saved to '{output_csv}'.")

    # 9. 시각화
    plt.figure(figsize=(12, 8))
    for i, row in embedding_df.iterrows():
        plt.scatter(row["X"], row["Y"], label=row["EQP_NM"])
        plt.text(row["X"], row["Y"], row["EQP_NM"], fontsize=9)

    plt.title("EQP_ID_MODULE_NAME Embedding Visualization")
    plt.xlabel("Dimension 1 (scaled)")
    plt.ylabel("Dimension 2 (scaled)")
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()

# 사용 예시
csv_file = "all.csv"  # all.csv 파일 경로
visualize_and_save_eqp_embedding(model, eqp_mapping, csv_file)
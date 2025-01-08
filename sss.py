def visualize_eqp_embedding(model, eqp_mapping):
    """
    EQP_ID_MODULE_NAME 임베딩 시각화
    """
    # EQP_ID_MODULE_NAME의 임베딩 벡터를 추출
    embedding_weights = model.eqp_embedding.weight.detach().cpu().numpy()

    # t-SNE를 사용하여 2D로 차원 축소
    tsne = TSNE(n_components=2, random_state=42)
    reduced_embeddings = tsne.fit_transform(embedding_weights)

    # EQP_ID_MODULE_NAME 레이블 가져오기
    eqp_labels = list(eqp_mapping.keys())

    # 시각화
    plt.figure(figsize=(12, 8))
    for i, label in enumerate(eqp_labels):
        print(reduced_embeddings[i, 0], reduced_embeddings[i, 1], label)
        plt.scatter(reduced_embeddings[i, 0], reduced_embeddings[i, 1], label=label)
        plt.text(reduced_embeddings[i, 0], reduced_embeddings[i, 1], label, fontsize=9)
    
    plt.title("EQP_ID_MODULE_NAME Embedding Visualization")
    plt.xlabel("Dimension 1")
    plt.ylabel("Dimension 2")
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()

visualize_eqp_embedding(model, eqp_mapping)

위에 나온 결과를 아래의 형식으로 저장해줘. 그리고 x y 범위를 0과 1사이로 바꿔죠.
추가로, all.csv 파일에 EQP_NM에 해당하는 ZDDFRONTMEAN_01_AFS2열 평균값을 ZDD열에 추가해줘.

print() 예시 결과 -1.6444485 0.5937629 CENC12A


EQP_NM	X	Y ZDD
CENC12A -1.6444485 0.5937629

def train_val_split(data, val_ratio=0.2, shuffle=True):
    """
    데이터를 Train/Validation으로 나누는 함수.

    Args:
        data: 전체 데이터 (리스트, DataFrame, 배열 등)
        val_ratio: Validation 데이터 비율 (기본값: 0.2)
        shuffle: 데이터를 섞을지 여부 (기본값: True)

    Returns:
        train_data, val_data: Train/Validation 데이터
    """
    # 데이터 길이 계산
    n_total = len(data)
    split_idx = int(n_total * (1 - val_ratio))

    # 인덱스 생성
    indices = list(range(n_total))

    if shuffle:
        # 데이터를 섞는 경우
        import random
        random.seed(42)  # 재현 가능성을 위해 시드 고정
        random.shuffle(indices)

    # 섞인 인덱스를 기준으로 데이터 분리
    train_indices = indices[:split_idx]
    val_indices = indices[split_idx:]

    # Train/Validation 데이터 분리
    train_data = [data[i] for i in train_indices]
    val_data = [data[i] for i in val_indices]

    return train_data, val_data
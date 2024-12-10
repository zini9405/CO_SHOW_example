import torch
import numpy as np
import random

def set_seed(seed: int):
    """
    학습의 재현 가능성을 위해 시드를 고정합니다.
    Args:
        seed (int): 고정할 시드 값
    """
    random.seed(seed)                      # Python의 random 모듈 시드 고정
    np.random.seed(seed)                   # NumPy 시드 고정
    torch.manual_seed(seed)                # PyTorch CPU 시드 고정
    torch.cuda.manual_seed(seed)           # PyTorch CUDA 시드 고정
    torch.cuda.manual_seed_all(seed)       # 모든 GPU의 CUDA 시드 고정 (멀티 GPU 사용 시)
    torch.backends.cudnn.deterministic = True  # CuDNN을 deterministic 모드로 설정
    torch.backends.cudnn.benchmark = False     # CuDNN의 최적화 비활성화 (속도는 느릴 수 있음)

# 시드 설정 예시
set_seed(42)
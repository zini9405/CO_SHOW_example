---------------------------------------------------------------------------
RuntimeError                              Traceback (most recent call last)
Cell In[4], line 178
    175 X = torch.rand(batch_size, num_steps, input_dim)  # 입력 데이터
    177 # 모델 실행
--> 178 y, step_scores = model(X)
    180 # 결과 출력
    181 print("Predicted Output (y):", y)  # (batch_size, output_dim)

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\torch\nn\modules\module.py:1532, in Module._wrapped_call_impl(self, *args, **kwargs)
   1530     return self._compiled_call_impl(*args, **kwargs)  # type: ignore[misc]
   1531 else:
-> 1532     return self._call_impl(*args, **kwargs)

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\torch\nn\modules\module.py:1541, in Module._call_impl(self, *args, **kwargs)
   1536 # If we don't have any hooks, we want to skip the rest of the logic in
   1537 # this function, and just call forward.
   1538 if not (self._backward_hooks or self._backward_pre_hooks or self._forward_hooks or self._forward_pre_hooks
   1539         or _global_backward_pre_hooks or _global_backward_hooks
   1540         or _global_forward_hooks or _global_forward_pre_hooks):
-> 1541     return forward_call(*args, **kwargs)
   1543 try:
   1544     result = None

Cell In[4], line 67
...
    158 H_step, step_scores = self.step_attention(H_local, H_local, H_local, need_weights=True)
--> 159 H_selected = torch.cat([H_global, torch.sum(step_scores.unsqueeze(-1) * H_local, dim=1)], dim=-1)
    160 return H_selected, step_scores

RuntimeError: The size of tensor a (12) must match the size of tensor b (8) at non-singleton dimension 1

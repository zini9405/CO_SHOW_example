Cell In[4], line 1
----> 1 for batch in dataloader:
      2     data, labels = batch
      3     print(data, labels)

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\torch\utils\data\dataloader.py:631, in _BaseDataLoaderIter.__next__(self)
    628 if self._sampler_iter is None:
    629     # TODO(https://github.com/pytorch/pytorch/issues/76750)
    630     self._reset()  # type: ignore[call-arg]
--> 631 data = self._next_data()
    632 self._num_yielded += 1
    633 if self._dataset_kind == _DatasetKind.Iterable and \
    634         self._IterableDataset_len_called is not None and \
    635         self._num_yielded > self._IterableDataset_len_called:

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\torch\utils\data\dataloader.py:675, in _SingleProcessDataLoaderIter._next_data(self)
    673 def _next_data(self):
    674     index = self._next_index()  # may raise StopIteration
--> 675     data = self._dataset_fetcher.fetch(index)  # may raise StopIteration
    676     if self._pin_memory:
    677         data = _utils.pin_memory.pin_memory(data, self._pin_memory_device)

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\torch\utils\data\_utils\fetch.py:51, in _MapDatasetFetcher.fetch(self, possibly_batched_index)
...
Cell In[1], line 17
     16 def __getitem__(self, idx):
---> 17     return torch.tensor(self.features[idx], dtype=torch.float32), torch.tensor(self.labels[idx], dtype=torch.float32)

TypeError: must be real number, not str

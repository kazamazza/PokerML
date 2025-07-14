class HandRangeDataset:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.samples = self._load_data()

    def _load_data(self):
        # TODO: Load JSONL, CSV, or DB with labeled (context → hand) samples
        return []

    def to_tensors(self):
        # TODO: Encode inputs and labels for training
        pass
        return
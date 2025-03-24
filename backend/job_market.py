import os
import pandas as pd

class JobMarket:
    def __init__(self, data_path):
        abs_path = os.path.abspath(data_path)
        print(f"Looking for dataset at: {abs_path}")

        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"File not found: {abs_path}")

        self.data = pd.read_csv(abs_path)

    def get_trends(self):
        return self.data.to_dict(orient='records')

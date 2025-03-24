import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go one level up
DATASET_PATH = os.path.join(BASE_DIR, "data", "dataset.csv")
JOB_MARKET_PATH = os.path.join(BASE_DIR, "data", "job_market_data.csv")

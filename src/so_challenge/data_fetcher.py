"""
Data collection module for the SO Challenge project.

This module handles fetching and processing data from various sources.
"""

import os
import time
import csv
import pandas as pd
import requests
from datetime import datetime


def fetch_question_counts(cache_file="so_question_counts.csv", max_retries=3):
    """
    Fetch monthly Stack Overflow question counts from 2008 to 2024.

    Args:
        cache_file (str): Path to cache file
        max_retries (int): Maximum number of retries for network errors

    Returns:
        pd.DataFrame: DataFrame with columns 'year_month', 'question_count'
    """
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            lines = f.read().splitlines()
            reader = csv.reader(lines)
            next(reader)  # skip header
            data = [{"year_month": row[0], "question_count": int(row[1])} for row in reader]
            return pd.DataFrame(data)

    base_url = "https://api.stackexchange.com/2.3/questions"

    for attempt in range(max_retries):
        try:
            response = requests.get(base_url, timeout=10)
            response.raise_for_status()
            items = response.json()["items"]
            data = []
            for item in items:
                dt = datetime.fromtimestamp(item["creation_date"])
                year_month = dt.strftime("%Y-%m")
                data.append({"year_month": year_month, "question_count": item["question_count"]})
            df = pd.DataFrame(data)
            df.to_csv(cache_file, index=False)
            return df
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(2 ** attempt)  # Exponential backoff
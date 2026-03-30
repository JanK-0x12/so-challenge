"""
Tests for the data_fetcher module.
"""

import os
import tempfile
import pandas as pd
import pytest
from unittest.mock import patch, MagicMock
from so_challenge.data_fetcher import fetch_question_counts


class TestDataFetcher:
    """Test cases for data fetching functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.cache_file = os.path.join(self.temp_dir, "so_question_counts.csv")

    def teardown_method(self):
        """Clean up test fixtures."""
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)
        os.rmdir(self.temp_dir)

    @patch('so_challenge.data_fetcher.requests.get')
    def test_successful_data_fetch_returns_correct_dataframe_shape(self, mock_get):
        """Test that successful API call returns DataFrame with correct shape."""
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "items": [
                {"creation_date": 1199145600, "question_count": 100},  # Jan 2008
                {"creation_date": 1201824000, "question_count": 150},  # Feb 2008
            ]
        }
        mock_get.return_value = mock_response

        # Call function
        df = fetch_question_counts(cache_file=self.cache_file)

        # Assertions
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ['year_month', 'question_count']
        # 17 years * 12 months = 204 months, but mock returns 2
        assert len(df) == 2  # Based on mock data
        assert df.iloc[0]['year_month'] == '2008-01'
        assert df.iloc[0]['question_count'] == 100

    @patch('so_challenge.data_fetcher.requests.get')
    @patch('so_challenge.data_fetcher.os.path.exists')
    @patch('builtins.open')
    def test_cached_data_returned_without_network_call(self, mock_open, mock_exists, mock_get):
        """Test that cached data is returned without making network call."""
        # Mock cache exists
        mock_exists.return_value = True

        # Mock cached data
        cached_data = "year_month,question_count\n2008-01,100\n2008-02,150\n"
        mock_file = MagicMock()
        mock_file.read.return_value = cached_data
        mock_open.return_value.__enter__.return_value = mock_file

        # Call function
        df = fetch_question_counts(cache_file=self.cache_file)

        # Assertions
        mock_get.assert_not_called()  # No network call
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert df.iloc[0]['year_month'] == '2008-01'

    @patch('so_challenge.data_fetcher.requests.get')
    @patch('so_challenge.data_fetcher.time.sleep')
    def test_network_error_triggers_retry_logic(self, mock_sleep, mock_get):
        """Test that network errors trigger retry logic."""
        # Mock network failure then success
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "items": [{"creation_date": 1199145600, "question_count": 100}]
        }

        mock_get.side_effect = [Exception("Network error"), mock_response]

        # Call function
        df = fetch_question_counts(cache_file=self.cache_file, max_retries=2)

        # Assertions
        assert mock_get.call_count == 2  # One failure, one success
        assert mock_sleep.call_count == 1  # One retry delay
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
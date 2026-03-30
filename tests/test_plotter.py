"""
Tests for the plotter module.
"""

import pandas as pd
import pytest
from unittest.mock import patch, MagicMock
from so_challenge.plotter import plot_data


class TestPlotter:
    """Test cases for plotting functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        # Sample data similar to data_fetcher output
        self.sample_df = pd.DataFrame({
            'year_month': ['2008-01', '2008-02', '2009-01', '2009-02'],
            'question_count': [100, 150, 200, 250]
        })

    @patch('so_challenge.plotter.plt')
    def test_plot_data_creates_line_chart_with_correct_data(self, mock_plt):
        """Test that plot_data creates a line chart with the correct x and y data."""
        # Call the function
        plot_data(self.sample_df)

        # Check that plt.plot was called
        mock_plt.plot.assert_called_once()
        call_args, call_kwargs = mock_plt.plot.call_args
        expected_x = ['2008-01', '2008-02', '2009-01', '2009-02']
        expected_y = [100, 150, 200, 250]
        assert list(call_args[0]) == expected_x
        assert list(call_args[1]) == expected_y
        assert call_kwargs == {'marker': 'o'}

    @patch('so_challenge.plotter.plt')
    def test_plot_data_sets_correct_axis_labels(self, mock_plt):
        """Test that plot_data sets correct x and y axis labels."""
        # Call the function
        plot_data(self.sample_df)

        # Check axis labels
        mock_plt.xlabel.assert_called_once_with('Date (Year-Month)')
        mock_plt.ylabel.assert_called_once_with('Question Count')

    @patch('so_challenge.plotter.plt')
    def test_plot_data_sets_title_and_grid(self, mock_plt):
        """Test that plot_data sets title and enables grid."""
        # Call the function
        plot_data(self.sample_df)

        # Check title
        mock_plt.title.assert_called_once_with('Stack Overflow Monthly Question Counts (2008-2024)')

        # Check grid
        mock_plt.grid.assert_called_once_with(True, alpha=0.3)

    @patch('so_challenge.plotter.plt')
    def test_plot_data_configures_x_axis_labels(self, mock_plt):
        """Test that plot_data configures x-axis labels for readability."""
        # Call the function
        plot_data(self.sample_df)

        # Check xticks rotation
        mock_plt.xticks.assert_called_once_with(rotation=45, ha='right')

    @patch('so_challenge.plotter.plt')
    def test_plot_data_shows_plot(self, mock_plt):
        """Test that plot_data displays the plot."""
        # Call the function
        plot_data(self.sample_df)

        # Check that show is called
        mock_plt.show.assert_called_once()

    @patch('so_challenge.plotter.plt')
    def test_plot_data_handles_empty_dataframe(self, mock_plt):
        """Test that plot_data handles empty DataFrame gracefully."""
        empty_df = pd.DataFrame(columns=['year_month', 'question_count'])

        # Call the function
        plot_data(empty_df)

        # Should still call plot but with empty data
        mock_plt.plot.assert_called_once()
        call_args, call_kwargs = mock_plt.plot.call_args
        assert call_args[0] == []
        assert call_args[1] == []
        assert call_kwargs == {'marker': 'o'}
        mock_plt.title.assert_called_once_with('Stack Overflow Monthly Question Counts (2008-2024)')
        mock_plt.show.assert_called_once()
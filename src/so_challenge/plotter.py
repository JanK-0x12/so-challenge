"""
Visualization module for the SO Challenge project.

This module provides functions for plotting and visualizing data.
"""

import matplotlib.pyplot as plt


def plot_data(df):
    """
    Plot Stack Overflow monthly question counts as a line chart.

    Args:
        df (pd.DataFrame): DataFrame with 'year_month' and 'question_count' columns
    """
    plt.figure(figsize=(12, 6))

    # Handle empty dataframe
    if df.empty:
        x_data = []
        y_data = []
    else:
        x_data = df['year_month']
        y_data = df['question_count']

    # Plot the data
    plt.plot(x_data, y_data, marker='o')

    # Set labels and title
    plt.xlabel('Date (Year-Month)')
    plt.ylabel('Question Count')
    plt.title('Stack Overflow Monthly Question Counts (2008-2024)')

    # Configure grid and x-axis
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha='right')

    # Save the plot
    plt.savefig('src/so_challenge/plot.png', dpi=300, bbox_inches='tight')

    # Show the plot
    plt.show()
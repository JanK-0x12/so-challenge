# SO Challenge

A Python project for collecting and visualizing data related to Stack Overflow challenges.

## Project Structure

- `src/so_challenge/data_fetcher.py`: Handles data collection from various sources.
- `src/so_challenge/plotter.py`: Provides visualization functions for the data.
- `src/so_challenge/milestones.py`: Defines project milestones and their criteria.
- `tests/`: Contains unit tests for each module.

## Dependencies

Managed via `uv` and `pyproject.toml`. Key dependencies include:
- pandas: Data manipulation
- matplotlib: Plotting and visualization
- requests: HTTP requests for data fetching
- pytest: Testing framework

## Setup

1. Install uv (from Astral).
2. Clone the repository.
3. Run `uv sync` to install dependencies.
4. Run `pytest` to execute tests.
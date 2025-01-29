# Portfolio Analysis Web App

## Overview

The Portfolio Analysis Web App is a Streamlit-based application that allows users to track, analyze, and visualize the performance of their investment portfolio. The app integrates Yahoo Finance API to fetch stock and ETF data and Plotly to generate interactive financial charts.

## Features

**Portfolio Builder**: Search and select stocks or ETFs to add to your portfolio.

**Stock Data Retrieval**: Fetch historical closing prices from Yahoo Finance.

**Visualizations**: Interactive line charts to track stock performance over time.

**Key Stock Metrics**: Display important statistics like 50-Day Average, 1-Year Low, and 1-Year High.

**Investment Calculator**: Input investment amounts per stock and visualize the portfolio's future growth.

**Goal Tracking**: Set investment goals and visualize the estimated timeline to achieve them.

## Tech Stack

**Python**: Primary programming language.

**Streamlit**: Web framework for interactive UI.

**Yahoo Finance (yfinance)**: Fetch financial data.

**FinanceDatabase (financedatabase)**: Retrieve stock and ETF symbols.

**Plotly**: Create interactive financial charts.

**Pandas & NumPy**: Data handling and manipulation.

## Installation

## Prerequisites

Ensure you have Python 3.8+ installed and install the required dependencies using:

`pip install streamlit yfinance financedatabase plotly pandas numpy`

## Running the App

To start the Streamlit app, run the following command in the terminal:

`streamlit run stockapp.py`

Replace stockapp.py with the actual filename of your script.

## How to Use

1. **Select Tickers**: Use the sidebar to search and add stock tickers to your portfolio.

2. **Choose Date Range**: Select the start and end date for historical price data.

3. **View Portfolio Performance**: The "Portfolio" tab displays stock performance and metrics.

4. **Use Investment Calculator**: In the "Calculator" tab, enter investment amounts and set financial goals.

5. **Analyze Projections**: View estimated growth and goal achievement timeline.

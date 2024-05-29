# Helper Modules
A repository with the modules containing helper modules for specific tasks within our projects. 
As for the required libraries, they're all listed in `requirements.txt`. This repository is made to be used as a submodule, read more on how to use them [here](https://www.git-tower.com/learn/git/ebook/en/command-line/advanced-topics/submodules/).
Here's an overview of what you'll find in each module: 

## Correlation Study Module

The `correlation_study` module is designed for conducting correlation analysis on stock data. It includes a class named `CorrelationAnalysis` that facilitates the following tasks:

### Initialization

```python
CorrelationAnalysis(dataframe, tickers, start_datetime, end_datetime)
```

Initializes the correlation analysis with the provided DataFrame containing stock data, a list of ticker symbols representing the stocks, and start/end date and time for the data.

### Functionality
- get_correlated_stocks(): Calculates correlation coefficients and p-values for the given stocks within the specified time period and stores the results internally.
- plot_corr_matrix(): Plots a heatmap of the correlation matrix using seaborn and matplotlib, displaying correlations between different stocks.
- corr_stocks_pair(): Identifies the pair of stocks with the maximum correlation coefficient, filters based on p-values, and saves the result. Additionally, it plots the stock price data of the identified pair.
### Attributes
- dataframe: Pandas DataFrame containing the stock data.
- tickers: List of ticker symbols representing the stocks.
- start_datetime: Start date and time of the data.
- end_datetime: End date and time of the data.
- corrvalues: Array containing correlation coefficients.
- pvalues: Array containing p-values.
- winner: List containing ticker symbols of the stocks with the highest correlation coefficient.

## Machine Learning Module

The LSTM model training module provides functionality to preprocess stock data, split it into training and testing sets, and build/train an LSTM (Long Short-Term Memory) model for forecasting.

### Functionality

- hashing_and_splitting(adj_close_stocks_dataframe): Splits the given DataFrame of adjusted close prices into training and testing sets based on checksum hashing.
- xtrain_ytrain(adj_close_stocks_dataframe): Splits the DataFrame into training and testing sets, normalizes the data, and prepares it for LSTM model training.
- lstm_model(xtrain, ytrain): Builds and trains an LSTM model using the training data.

## DataFrameHelper Module

The `DataFrameHelper` module provides functionality for managing and preprocessing stock price data in a DataFrame format. The `DataFrameHelper` class offers methods to load, clean, and manage stock price data.

### Initialization

```python
DataFrameHelper(filename, link, years, interval)
```

Initializes a `DataFrameHelper` object with the specified parameters:
- `filename`: The name of the file to save/load the DataFrame.
- `link`: The URL link to retrieve ticker symbols.
- `years`: Number of years of historical data to load.
- `interval`: Time interval for historical data (e.g., '1d' for daily).

### Functionality

- `load()`: Loads a DataFrame of stock price data from a pickle file if it exists; otherwise, creates a new DataFrame by downloading data using `yfinance`.
- `get_stockex_tickers()`: Retrieves ticker symbols from a specified link containing stock exchange information.
- `loaded_df()`: Downloads stock price data for the specified number of years and tickers using `yfinance` and returns a pandas DataFrame.
- `clean_df(percentage)`: Cleans the DataFrame by dropping stocks with NaN values exceeding a specified percentage threshold and serializes the cleaned DataFrame.

### Attributes

- `filename`: Name of the file associated with the DataFrame.
- `link`: URL link to retrieve ticker symbols.
- `years`: Number of years of historical data to load.
- `interval`: Time interval for historical data.
- `dataframe`: Pandas DataFrame containing the stock price data.
- `tickers`: List of ticker symbols representing the stocks.

## Memory Handling Module


## PickleHelper Module

The `PickleHelper` module provides functionality for serializing and deserializing objects using the `pickle` module.

### Initialization

```python
PickleHelper(obj)
```

Initializes a `PickleHelper` object with the object `obj` to be serialized.

### Functionality

- `pickle_dump(filename)`: Serializes the given object and saves it to a file using `pickle`.
- `pickle_load(filename)`: Loads a serialized object from a file using `pickle` and returns a `PickleHelper` object with the loaded object accessible through its `.obj` attribute.

### Attributes

- `obj`: The object to be serialized or deserialized.

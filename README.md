# Python - Meta Trader 5 point-to-dollar conversion

This project is a CLI utility for Forex point-to-dollar conversion. It integrates with Meta Trader 5 (MT5) to fetch live data and calculate the value (in USD) of a specified number of points for any Forex symbol for a volume of 0.01 lot.

> There is an improved version of this utility built as a web application. Make sure to check the [web app project](https://github.com/aguiarjv/fastapi-mt5-forex-values).

## Features

- **Real-Time Data Fetching**: Fetches live trading data directly from Meta Trader 5.
- **Forex Point-to-Dollar Conversion**: Converts a given number of points to USD value for a specified Forex symbol.

## Prerequisites
### Meta Trader 5
- Install Meta Trader 5.
- Ensure it is running before you start the application.
- Ensure you have an account connected to a trading server.

### Python Environment
- Python 3.8+
- Git
- Virtualenv

## Installation and Setup
1. Clone this repository:
    ```bash
    git clone https://github.com/aguiarjv/python-mt5-forex-values-cli
    ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Change the names of the symbols in the ```main.py``` file to the ones you want to fetch data from.
2. Make sure your Meta Trader 5 is open and connected.
3. Run ```python main.py```

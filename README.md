# alpha-factor-research
This README assumes the existence of the ManageData.py, TransformData.py, and FactorTester.py modules, as their code was not provided.

Markdown

# Quantitative Factor Analysis Script

This project provides a Python script for performing quantitative analysis on financial factors across different market capitalization ranges. It loads factor and return data, cleans and transforms the factors, analyzes their individual alpha potential, ranks them, and then optimizes multi-factor combinations to find those with the highest inter-temporal Information Ratio (IRitp).

## Features

* **Data Loading:** Loads financial data from Excel files based on specified market capitalization ranges (All, High, Mid, Low).
* **Data Preprocessing:** Includes steps for cleaning and transforming raw factor data (e.g., handling outliers, Z-scoring, cross-sectional scaling).
* **Single Factor Analysis:** Calculates key metrics like the Information Coefficient (IC) for individual factors (`AnalyzeFactor`).
* **Factor Ranking:** Ranks factors based on their performance (specifically using the inter-temporal IC, `ICitp`).
* **Multi-Factor Optimization:** Finds optimal weightings for combinations of the top-ranked factors (2, 3, 4, and 5 factors) to maximize the inter-temporal Information Ratio (`Optimize_IRitp_X`).
* **Reporting:** Prints the top-performing factors and the best IRitp achieved for different model sizes.

## Requirements

* Python 3.x
* `numpy`
* `pandas`
* `itertools`
* `openpyxl` (for reading `.xlsm` files with pandas)
* Custom modules: `ManageData`, `TransformData`, `FactorTester` (These Python files must be present in your project directory).

You can install the required libraries using pip:

```bash
pip install numpy pandas openpyxl
File Structure
The project expects a structure similar to this:

.
├── main_script.py  # The provided code goes here
├── ManageData.py   # Custom module for data loading/saving
├── TransformData.py # Custom module for data cleaning/transformation
├── FactorTester.py # Custom module for factor analysis and optimization
├── DataAllCap.xlsm  # Input data file for All Cap (example)
├── DataHighCap.xlsm # Input data file for High Cap (example)
├── DataMidCap.xlsm  # Input data file for Mid Cap (example)
├── DataLowCap.xlsm  # Input data file for Low Cap (example)
└── ... (other potential data files or scripts)
Data Format
The script expects input data in specific Excel files (.xlsm) named according to the market capitalization range, e.g., DataAllCap.xlsm, DataHighCap.xlsm, etc.

The exact format required by ManageData.loaddataFormat1 is not detailed in the provided code. However, based on the script's usage, the data within these files should contain columns for:

Forward stock returns (ForwardReturns_AP).
Stock returns (Returns_AP).
Various financial factors (e.g., Price_Book, STMomentum, SurpriseMomentum, Month12ChangeF12MEarningsEstimate, etc.). The script processes columns ending in _AP after loading, but get_factors suggests raw factor names might be in a 'Variable' column in an Excel sheet named "data". The LoadData function loads from the main Excel file directly. You should consult the ManageData.py module for the precise expected Excel sheet and column structure.
Likely requires identifiers for stocks (tickers, security IDs) and dates/time periods.
The script primarily works with factor data that has an _AP suffix after being loaded and potentially processed by ManageData.

Usage
Ensure all required libraries are installed (pip install -r requirements.txt if you create one, or install individually).

Place the ManageData.py, TransformData.py, FactorTester.py files, and your input data .xlsm files in the same directory as the main script (main_script.py).

Run the script from your terminal:

Bash

python main_script.py
The script is currently configured to run the single_factor_alpha_test function for each of the market capitalization categories: "All", "High", "Mid", and "Low". It will print the results for each category to the console.

You can modify the main execution block at the end of the script to:

Run only specific market cap ranges.
Call the Run_Lab function with specific data and a save file name (note that Run_Lab currently processes a fixed set of factors, not the top-ranked ones dynamically).
Save the results list to a file if needed.
Understanding the Code
LoadData(CapRange): Handles the initial loading of data for a given market cap range.
single_factor_alpha_test(cap_range): The core function that performs the factor analysis pipeline (loading, cleaning, transforming, single-factor analysis, ranking, multi-factor optimization).
Run_Lab(D, SaveFile): A separate function that performs analysis and optimization on a pre-defined set of factors from a loaded dataset D. It also saves intermediate results to pickle files.
get_first_n_keys_as_list(dictionary, n): Helper to get the top N keys from a dictionary (assumes the dictionary is already ordered, as is the case after sorting factor_ranking).
get_factors(excel_file): A utility function (not directly used in the main analysis flow shown) to extract potential factor names from an Excel file.
The script relies heavily on the functionality provided by the imported ManageData, TransformData, and FactorTester modules.

Output
The script prints the following for each market cap range analyzed by single_factor_alpha_test:

The list of top 5 factors based on their ICitp.
The highest IRitp found for the 2-factor, 3-factor, 4-factor, and 5-factor optimized models using combinations of the top factors.
The Run_Lab function, if called, saves the transformed data (TD), factor analysis results (FA), and optimization results (S2, S3) to pickle files named TD[SaveFile].pkl, FA[SaveFile].pkl, S2[SaveFile].pkl, and S3[SaveFile].pkl.

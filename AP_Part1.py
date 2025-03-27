import pandas as pd
import numpy as np

def explore_dataset(df, name):
    """
    Comprehensive dataset exploration function

    Parameters:
    df (pandas.DataFrame): Input dataframe
    name (str): Name of the dataset

    Returns:
    dict: Detailed dataset information
    """
    print(f"\n--- {name} Dataset Analysis ---")

    # Basic information
    info = {
        'name': name,
        'shape': df.shape,
        'columns': list(df.columns),
        'data_types': df.dtypes.to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'missing_percentage': (df.isnull().sum() / len(df) * 100).to_dict()
    }

    # Detailed printing
    print(f"Shape: {info['shape']}")
    print("\nColumns:")
    for col in info['columns']:
        print(f"- {col}: {info['data_types'][col]}")

    print("\nMissing Values:")
    for col, count in info['missing_values'].items():
        if count > 0:
            print(f"- {col}: {count} ({info['missing_percentage'][col]:.2f}%)")

    # Sample basic statistics for numeric columns
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    if len(numeric_columns) > 0:
        print("\nNumeric Columns Summary:")
        print(df[numeric_columns].describe())

    return info


def preprocess_data(df):
    """
    Generic data preprocessing function

    Parameters:
    df (pandas.DataFrame): Input dataframe

    Returns:
    pandas.DataFrame: Preprocessed dataframe
    """
    # Handle missing values
    df_cleaned = df.copy()

    # Fill numeric columns with median
    numeric_columns = df_cleaned.select_dtypes(include=[np.number]).columns
    df_cleaned[numeric_columns] = df_cleaned[numeric_columns].fillna(df_cleaned[numeric_columns].median())

    # Fill categorical columns with mode
    categorical_columns = df_cleaned.select_dtypes(include=['object']).columns
    df_cleaned[categorical_columns] = df_cleaned[categorical_columns].fillna(
        df_cleaned[categorical_columns].mode().iloc[0])

    # Convert date columns to datetime if applicable
    date_columns = df_cleaned.select_dtypes(include=['object']).columns
    for col in date_columns:
        try:
            df_cleaned[col] = pd.to_datetime(df_cleaned[col], errors='coerce')
        except:
            pass

    return df_cleaned


# Load datasets
canadian_funds = pd.read_csv('canadian_funds_data_long.csv')
us_etfs = pd.read_csv('us_etfs_data_wide.csv')
macro_data = pd.read_excel('Macro.xlsx')
ff_factors = pd.read_excel('FF_Factors.xlsx')

# Explore each dataset
datasets = {
    'Canadian Funds': canadian_funds,
    'US ETFs': us_etfs,
    'Macro Data': macro_data,
    'Fama French Factors': ff_factors
}

dataset_info = {}
for name, df in datasets.items():
    dataset_info[name] = explore_dataset(df, name)

# Optional: Preprocessing demonstration
preprocessed_canadian_funds = preprocess_data(canadian_funds)
preprocessed_us_etfs = preprocess_data(us_etfs)
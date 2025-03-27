#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 10:57:11 2025

@author: isaacabheek
"""

import pandas as pd
import numpy as np

#Canadian funds
canadian_funds = pd.read_csv('canadian_funds_data_long.csv')
canadian_funds['date'] = pd.to_datetime(canadian_funds['date'], format='%Y%m%d')
canadian_funds['return'] = canadian_funds['return'].replace('missing', pd.NA)
canadian_funds = canadian_funds.pivot(index='date', columns='name', values='return')
canadian_funds.reset_index(inplace=True)


#US ETFS
us_etfs = pd.read_csv('us_etfs_data_wide.csv')
headers_etf = us_etfs.iloc[:4]
us_etfs = us_etfs.iloc[4:]
us_etfs = us_etfs.rename(columns={us_etfs.columns[0]: 'date'})
us_etfs['date'] = pd.to_datetime(us_etfs['date'], format='%Y%m%d')

#FF_factors
FF_factors = pd.read_excel('FF_Factors.xlsx')
FF_factors_header = FF_factors.iloc[:4]
FF_factors = FF_factors.iloc[4:]
FF_factors = FF_factors.rename(columns={FF_factors.columns[0]: 'date'})
FF_factors['date'] = pd.to_datetime(FF_factors['date'], format='%Y%m%d')

#Macro
Macro = pd.read_excel('Macro.xlsx')
Macro_header = Macro.iloc[:3]
Macro = Macro.iloc[3:]
Macro = Macro.rename(columns={Macro.columns[0]: 'date'})
Macro['date'] = pd.to_datetime(Macro['date'], format='%Y%m%d')

def preprocess_dataframe(df):
    
    df['date'] = pd.to_datetime(df['date']).dt.date  
    df.set_index('date', inplace=True) 
    df.fillna(0, inplace=True)  
    return df

dataframes = [canadian_funds, FF_factors, Macro, us_etfs]

dataframes = [preprocess_dataframe(df) for df in dataframes]

canadian_funds, FF_factors, Macro, us_etfs = dataframes

merged_df = canadian_funds.merge(us_etfs, left_index=True, right_index=True, how='inner')

merged_df.fillna(0, inplace=True)

# =============================================================================
# CAGR
# =============================================================================

cagr_df= merged_df
cagr_df = cagr_df.apply(pd.to_numeric, errors='coerce')

CAGR1 = ((cagr_df.iloc[-1] - cagr_df.iloc[-13])**1) - 1
CAGR3 = ((cagr_df.iloc[-1] - cagr_df.iloc[-25])**1/3) - 1
CAGR5 = ((cagr_df.iloc[-1] - cagr_df.iloc[-37])**1/5) - 1
CAGR7 = ((cagr_df.iloc[-1] - cagr_df.iloc[-49])**1/7) - 1
CAGR10 = ((cagr_df.iloc[-1] - cagr_df.iloc[-61])**1/10) - 1

cagr_df.loc["CAGR-1Y"] = CAGR1
cagr_df.loc["CAGR-3Y"] = CAGR3
cagr_df.loc["CAGR-5Y"] = CAGR5
cagr_df.loc["CAGR-7Y"] = CAGR7
cagr_df.loc["CAGR-10Y"] = CAGR10

# =============================================================================
# Volatility
# =============================================================================

volatility_df= merged_df
volatility_df = volatility_df.apply(pd.to_numeric, errors='coerce')

volatility1 = volatility_df.tail(12).std() * np.sqrt(12)
volatility3 = volatility_df.tail(36).std() * np.sqrt(36)
volatility5 = volatility_df.tail(60).std() * np.sqrt(60)
volatility7 = volatility_df.tail(84).std() * np.sqrt(84)
volatility10 = volatility_df.tail(120).std() * np.sqrt(120)

volatility_df.loc["Volatility-1Y"] = volatility1
volatility_df.loc["Volatility-3Y"] = volatility3
volatility_df.loc["Volatility-5Y"] = volatility5
volatility_df.loc["Volatility-7Y"] = volatility7
volatility_df.loc["Volatility-10Y"] = volatility10

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


# =============================================================================
# CVAR and AVAR
# =============================================================================
cvar_df= merged_df
cvar_df = cvar_df.apply(pd.to_numeric, errors='coerce')

def calculate_cvar(returns, confidence_level=0.95):

    var = np.percentile(returns, 100 * (1 - confidence_level))
    cvar = returns[returns <= var].mean() 
    return cvar

confidence_level1 = 0.95

cvar_values_95_1 = cvar_df.tail(12).apply(lambda col: calculate_cvar(col, confidence_level1))
cvar_values_95_3 = cvar_df.tail(36).apply(lambda col: calculate_cvar(col, confidence_level1))
cvar_values_95_5 = cvar_df.tail(60).apply(lambda col: calculate_cvar(col, confidence_level1))
cvar_values_95_7 = cvar_df.tail(84).apply(lambda col: calculate_cvar(col, confidence_level1))
cvar_values_95_10 = cvar_df.tail(120).apply(lambda col: calculate_cvar(col, confidence_level1))

cvar_df.loc["CVAR95-1Y"] = cvar_values_95_1
cvar_df.loc["CVAR95-3Y"] = cvar_values_95_3
cvar_df.loc["CVAR95-5Y"] = cvar_values_95_5
cvar_df.loc["CVAR95-7Y"] = cvar_values_95_7
cvar_df.loc["CVAR95-10Y"] = cvar_values_95_10

confidence_level2 = 0.90

cvar_values_90_1 = cvar_df.tail(12).apply(lambda col: calculate_cvar(col, confidence_level2))
cvar_values_90_3 = cvar_df.tail(36).apply(lambda col: calculate_cvar(col, confidence_level2))
cvar_values_90_5 = cvar_df.tail(60).apply(lambda col: calculate_cvar(col, confidence_level2))
cvar_values_90_7 = cvar_df.tail(84).apply(lambda col: calculate_cvar(col, confidence_level2))
cvar_values_90_10 = cvar_df.tail(120).apply(lambda col: calculate_cvar(col, confidence_level2))

cvar_df.loc["CVAR90-1Y"] = cvar_values_90_1
cvar_df.loc["CVAR90-3Y"] = cvar_values_90_3
cvar_df.loc["CVAR90-5Y"] = cvar_values_90_5
cvar_df.loc["CVAR90-7Y"] = cvar_values_90_7
cvar_df.loc["CVAR90-10Y"] = cvar_values_90_10

confidence_level3 = 0.99

cvar_values_99_1 = cvar_df.tail(12).apply(lambda col: calculate_cvar(col, confidence_level3))
cvar_values_99_3 = cvar_df.tail(36).apply(lambda col: calculate_cvar(col, confidence_level3))
cvar_values_99_5 = cvar_df.tail(60).apply(lambda col: calculate_cvar(col, confidence_level3))
cvar_values_99_7 = cvar_df.tail(84).apply(lambda col: calculate_cvar(col, confidence_level3))
cvar_values_99_10 = cvar_df.tail(120).apply(lambda col: calculate_cvar(col, confidence_level3))

cvar_df.loc["CVAR99-1Y"] = cvar_values_99_1
cvar_df.loc["CVAR99-3Y"] = cvar_values_99_3
cvar_df.loc["CVAR99-5Y"] = cvar_values_99_5
cvar_df.loc["CVAR99-7Y"] = cvar_values_99_7
cvar_df.loc["CVAR99-10Y"] = cvar_values_99_10

avar1 =  (cvar_values_95_1 + cvar_values_90_1 +cvar_values_99_1)/3
avar3 =  (cvar_values_95_3 + cvar_values_90_3 +cvar_values_99_3)/3
avar5 =  (cvar_values_95_5 + cvar_values_90_5 +cvar_values_99_5)/3
avar7 =  (cvar_values_95_7 + cvar_values_90_7 +cvar_values_99_7)/3
avar10 =  (cvar_values_95_10 + cvar_values_90_10 +cvar_values_99_10)/3

cvar_df.loc["AVAR-1Y"] = avar1
cvar_df.loc["AVAR-3Y"] = avar3
cvar_df.loc["AVAR-5Y"] = avar5
cvar_df.loc["AVAR-7Y"] = avar7
cvar_df.loc["AVAR-10Y"] = avar10

# =============================================================================
# Maximum Drawdown
# =============================================================================

mdd_df= merged_df
mdd_df = mdd_df.apply(pd.to_numeric, errors='coerce')

def calculate_max_drawdown(returns):

    cumulative_returns = (1 + returns).cumprod()  
    peak = cumulative_returns.cummax()  
    drawdown = (cumulative_returns - peak) / peak  
    max_drawdown = drawdown.min() 
    
    return max_drawdown

mdd_values1 = mdd_df.tail(12).apply(calculate_max_drawdown)
mdd_values3 = mdd_df.tail(36).apply(calculate_max_drawdown)
mdd_values5 = mdd_df.tail(60).apply(calculate_max_drawdown)
mdd_values7 = mdd_df.tail(84).apply(calculate_max_drawdown)
mdd_values10 = mdd_df.tail(120).apply(calculate_max_drawdown)

mdd_df.loc["MDD-1Y"] = mdd_values1
mdd_df.loc["MDD-3Y"] = mdd_values3
mdd_df.loc["MDD-5Y"] = mdd_values5
mdd_df.loc["MDD-7Y"] = mdd_values7
mdd_df.loc["MDD-10Y"] = mdd_values10

# =============================================================================
# Downside Deviation
# =============================================================================

dd_df= merged_df
dd_df = dd_df.apply(pd.to_numeric, errors='coerce')

def calculate_downside_deviation(returns, target_return=0):

    downside_returns = returns[returns < target_return]
    downside_diff = downside_returns - target_return  
    downside_deviation = np.sqrt((downside_diff**2).sum() / len(returns))
    
    return downside_deviation

downside_dev_values1 = dd_df.tail(12).apply(calculate_downside_deviation)
downside_dev_values3 = dd_df.tail(36).apply(calculate_downside_deviation)
downside_dev_values5 = dd_df.tail(60).apply(calculate_downside_deviation)
downside_dev_values7 = dd_df.tail(84).apply(calculate_downside_deviation)
downside_dev_values10 = dd_df.tail(120).apply(calculate_downside_deviation)

dd_df.loc["DD-1Y"] = downside_dev_values1
dd_df.loc["DD-3Y"] = downside_dev_values3
dd_df.loc["DD-5Y"] = downside_dev_values5
dd_df.loc["DD-7Y"] = downside_dev_values7
dd_df.loc["DD-10Y"] = downside_dev_values10


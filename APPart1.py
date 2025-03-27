#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 10:57:11 2025

@author: isaacabheek
"""

import pandas as pd

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

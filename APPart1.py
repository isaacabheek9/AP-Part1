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
canadian_funds['date'] = canadian_funds['date'].dt.strftime('%Y-%m-%d')
canadian_funds = canadian_funds.fillna(0)

#US ETFS
us_etfs = pd.read_csv('us_etfs_data_wide.csv')
headers_etf = us_etfs.iloc[:4]
us_etfs = us_etfs.iloc[4:]
us_etfs = us_etfs.rename(columns={us_etfs.columns[0]: 'date'})
us_etfs['date'] = pd.to_datetime(us_etfs['date'], format='%Y%m%d')
us_etfs = us_etfs.reset_index(drop=True)

#FF_factors
FF_factors = pd.read_excel('FF_Factors.xlsx')
FF_factors_header = FF_factors.iloc[:4]
FF_factors = FF_factors.iloc[4:]
FF_factors = FF_factors.rename(columns={FF_factors.columns[0]: 'date'})
FF_factors['date'] = pd.to_datetime(FF_factors['date'], format='%Y%m%d')
FF_factors = FF_factors.reset_index(drop=True)

#Macro
Macro = pd.read_excel('Macro.xlsx')
Macro_header = Macro.iloc[:4]
Macro = Macro.iloc[4:]
Macro = Macro.rename(columns={Macro.columns[0]: 'date'})
Macro['date'] = pd.to_datetime(Macro['date'], format='%Y%m%d')
Macro = Macro.reset_index(drop=True)
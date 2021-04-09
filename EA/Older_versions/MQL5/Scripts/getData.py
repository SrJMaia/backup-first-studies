# Copyright 2021, MetaQuotes Software Corp.
# https://www.mql5.com

import MetaTrader5 as mt5
import pandas as pd
import datetime as dt
import numpy as np

if not mt5.initialize(login=40305620,password='x8dcteyv',server='MetaQuotes-Demo'):
   print('MT5 não iniciado.')
   mt5.shutdown()

def preprocess_mt5(symbol,mt5, init= dt.datetime(2018, 1, 28, 13),end=dt.datetime.now(dt.timezone.utc), time_frame=mt5.TIMEFRAME_H1):
   df_rates = pd.DataFrame(mt5.copy_rates_range(symbol, time_frame ,init, end))
   df_rates['time'] = pd.to_datetime(df_rates['time'], unit='s',utc=True)
   df_rates["symbol"]=symbol
   return(df_rates)
    
    
def diff_data(list_symbol):
   df2 = pd.DataFrame()
   for i in range(len(list_symbol)):
      df=preprocess_mt5(symbol=list_symbol[i], mt5=mt5, init= dt.datetime(2020,1,1),time_frame=mt5.TIMEFRAME_H1)
      df2[list_symbol[i]] = df['close'] - df['open']
      del df
   df2['sum'] = df2.sum(axis=1)
   #df2['sma'] = round(df2['sum'].rolling(sma_diff_period,min_periods=sma_min_period).mean() * 1000,0)
   df2['sma'] = round(df2['sum'].rolling(sma_diff_period,min_periods=sma_min_period).sum() * 1000,0)
   return df2['sma']
   
   
eur = ['EURCHF','EURGBP','EURJPY','EURNZD','EURUSD','EURAUD','EURCAD']
gbp = ['EURGBP','GBPAUD','GBPCHF','GBPJPY','GBPCAD','GBPUSD','GBPNZD']
usd = ['GBPUSD','USDCHF','USDJPY','AUDUSD','NZDUSD','USDCAD','EURUSD']
jpy = ['AUDJPY','CADJPY','CHFJPY','EURJPY','USDJPY','GBPJPY','NZDJPY']
chf = ['AUDCHF','CADCHF','CHFJPY','USDCHF','EURCHF','GBPCHF','NZDCHF']
nzd = ['AUDNZD','EURNZD','GBPNZD','NZDUSD','NZDCAD','NZDCHF','NZDJPY']
aud = ['AUDCAD','AUDCHF','AUDJPY','AUDUSD','AUDNZD','EURAUD','GBPAUD']
cad = ['AUDCAD','CADCHF','CADJPY','USDCAD','EURCAD','GBPCAD','NZDCAD']

data = pd.DataFrame()

data['eur'] = diff_data(eur)
data['gbp'] = diff_data(gbp)
data['usd'] = diff_data(usd)
data['jpy'] = diff_data(jpy)
data['chf'] = diff_data(chf)
data['nzd'] = diff_data(nzd)
data['aud'] = diff_data(aud)
data['cad'] = diff_data(cad)


df2.to_csv('C:\\Users\\johnk\\AppData\\Roaming\\MetaQuotes\\Terminal\\D0E8209F77C8CF37AD8BF550E51FF075\\MQL5\\Files\\prices.csv')

mt5.shutdown()

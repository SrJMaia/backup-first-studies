import pandas as pd
import MetaTrader5 as mt5
from erros import OnlyOneParamater

"""
Passar all_pairs e derivados como constantes
"""

def preprocess_mt5(symbol, start=0,end=70_000, time_frame=mt5.TIMEFRAME_H1,data_type='close', monte_carlo=False):
    df_rates = pd.DataFrame()
    if monte_carlo:
        df_rates = pd.DataFrame(mt5.copy_rates_from_pos(symbol, time_frame , start, end))
    else:
        df_rates = pd.DataFrame(mt5.copy_rates_from_pos(symbol, time_frame , start, end))
    return df_rates[data_type]


def get_data(start_pos,end_pos,time_frame, periods=1, monte_carlo_shuffle=False):

    diff_symbols = {
        'eur':['EURCHF','EURGBP','EURJPY','EURNZD','EURUSD','EURAUD','EURCAD'],
        'gbp':['EURGBP','GBPAUD','GBPCHF','GBPJPY','GBPCAD','GBPUSD','GBPNZD'],
        'usd':['GBPUSD','USDCHF','USDJPY','AUDUSD','NZDUSD','USDCAD','EURUSD'],
        'jpy':['AUDJPY','CADJPY','CHFJPY','EURJPY','USDJPY','GBPJPY','NZDJPY'],
        'chf':['AUDCHF','CADCHF','CHFJPY','USDCHF','EURCHF','GBPCHF','NZDCHF'],
        'nzd':['AUDNZD','EURNZD','GBPNZD','NZDUSD','NZDCAD','NZDCHF','NZDJPY'],
        'aud':['AUDCAD','AUDCHF','AUDJPY','AUDUSD','AUDNZD','EURAUD','GBPAUD'],
        'cad':['AUDCAD','CADCHF','CADJPY','USDCAD','EURCAD','GBPCAD','NZDCAD']
    }
    """
    
    AJUSTAR
    CALCULAR O PCT CHANGE COM OS DADOS PEGADOS E NÃO O PCT E DEPOIS PEGAR OS DADOS POIS IRA COMPUTAR VALROES DIFERENTES POR CONTA DO SHUFFLE
    
    """
    df = pd.DataFrame()
    for i in diff_symbols.items():
        df2 = pd.DataFrame()
        data = pd.DataFrame()
        for j in i[1]:
            data[j]=preprocess_mt5(symbol=j,start=start_pos,end=end_pos,time_frame=time_frame,data_type='open', monte_carlo=monte_carlo_shuffle)
            if i[0] == 'gbp':
                if j == 'EURGBP':
                    data[j] = 1 / data[j]
            if i[0] == 'usd':
                if j in ['GBPUSD','AUDUSD','NZDUSD','EURUSD']:
                    data[j] = 1 / data[j]
            if i[0] == 'jpy':
                data[j] = 1 / data[j]
            if i[0] == 'chf':
                if j in ['AUDCHF','CADCHF','USDCHF','EURCHF','GBPCHF','NZDCHF']:
                    data[j] = 1 / data[j]
            if i[0] == 'nzd':
                if j in ['AUDNZD','EURNZD','GBPNZD']:
                    data[j] = 1 / data[j]
            if i[0] == 'aud':
                if j in ['EURAUD','GBPAUD']:
                    data[j] = 1 / data[j]
            if i[0] == 'cad':
                if j in ['AUDCAD','USDCAD','EURCAD','GBPCAD','NZDCAD']:
                    data[j] = 1 / data[j]
        df[f'{i[0]}'] = data.pct_change(periods=periods).sum(axis=1)*100
#        df2[f'{i}_open'] = data.sum(axis=1)*100
#         for j in diff_symbols[i]:
#             data[j]=preprocess_mt5(symbol=j,start=start_pos,end=end_pos,time_frame=time_frame,data_type='high').pct_change(periods=periods)
#         df2[f'{i}_high'] = data.sum(axis=1)*100
#         for j in diff_symbols[i]:
#             data[j]=preprocess_mt5(symbol=j,start=start_pos,end=end_pos,time_frame=time_frame,data_type='low').pct_change(periods=periods)
#         df2[f'{i}_low'] = data.sum(axis=1)*100
#         for j in diff_symbols[i]:
#             data[j]=preprocess_mt5(symbol=j,start=start_pos,end=end_pos,time_frame=time_frame,data_type='close').pct_change(periods=periods)
#         df2[f'{i}_close'] = data.sum(axis=1)*100
#        df[f'{i}'] = df2.sum(axis=1)

    all_pairs_open = ['EURCHF_Open','EURGBP_Open','EURJPY_Open','EURNZD_Open','EURUSD_Open','EURAUD_Open','EURCAD_Open',
                      'GBPAUD_Open','GBPCHF_Open','GBPJPY_Open','GBPCAD_Open','GBPUSD_Open','GBPNZD_Open','USDCHF_Open',
                      'USDJPY_Open','AUDUSD_Open','NZDUSD_Open','USDCAD_Open','AUDJPY_Open','CADJPY_Open','CHFJPY_Open',
                      'NZDJPY_Open','AUDCHF_Open','CADCHF_Open','NZDCHF_Open','AUDNZD_Open','NZDCAD_Open','AUDCAD_Open']

    all_pairs_close = ['EURCHF_Close','EURGBP_Close','EURJPY_Close','EURNZD_Close','EURUSD_Close','EURAUD_Close','EURCAD_Close',
                      'GBPAUD_Close','GBPCHF_Close','GBPJPY_Close','GBPCAD_Close','GBPUSD_Close','GBPNZD_Close','USDCHF_Close',
                      'USDJPY_Close','AUDUSD_Close','NZDUSD_Close','USDCAD_Close','AUDJPY_Close','CADJPY_Close','CHFJPY_Close',
                      'NZDJPY_Close','AUDCHF_Close','CADCHF_Close','NZDCHF_Close','AUDNZD_Close','NZDCAD_Close','AUDCAD_Close']

    all_pairs_high = ['EURCHF_High','EURGBP_High','EURJPY_High','EURNZD_High','EURUSD_High','EURAUD_High','EURCAD_High',
                      'GBPAUD_High','GBPCHF_High','GBPJPY_High','GBPCAD_High','GBPUSD_High','GBPNZD_High','USDCHF_High',
                      'USDJPY_High','AUDUSD_High','NZDUSD_High','USDCAD_High','AUDJPY_High','CADJPY_High','CHFJPY_High',
                      'NZDJPY_High','AUDCHF_High','CADCHF_High','NZDCHF_High','AUDNZD_High','NZDCAD_High','AUDCAD_High']

    all_pairs_low = ['EURCHF_Low','EURGBP_Low','EURJPY_Low','EURNZD_Low','EURUSD_Low','EURAUD_Low','EURCAD_Low',
                      'GBPAUD_Low','GBPCHF_Low','GBPJPY_Low','GBPCAD_Low','GBPUSD_Low','GBPNZD_Low','USDCHF_Low',
                      'USDJPY_Low','AUDUSD_Low','NZDUSD_Low','USDCAD_Low','AUDJPY_Low','CADJPY_Low','CHFJPY_Low',
                      'NZDJPY_Low','AUDCHF_Low','CADCHF_Low','NZDCHF_Low','AUDNZD_Low','NZDCAD_Low','AUDCAD_Low']


    all_pairs = ['EURCHF','EURGBP','EURJPY','EURNZD','EURUSD','EURAUD','EURCAD',
                 'GBPAUD','GBPCHF','GBPJPY','GBPCAD','GBPUSD','GBPNZD','USDCHF',
                 'USDJPY','AUDUSD','NZDUSD','USDCAD','AUDJPY','CADJPY','CHFJPY',
                 'NZDJPY','AUDCHF','CADCHF','NZDCHF','AUDNZD','NZDCAD','AUDCAD']


    for i in range(len(all_pairs)):
        df[all_pairs[i]]=preprocess_mt5(symbol=all_pairs[i],start=start_pos,end=end_pos,time_frame=time_frame,data_type='open')
        #df[all_pairs_open[i]]=preprocess_mt5(symbol=all_pairs[i],start=start_pos,end=end_pos,time_frame=time_frame,data_type='open')
        #df[all_pairs_close[i]]=preprocess_mt5(symbol=all_pairs[i],start=start_pos,end=end_pos,time_frame=time_frame,data_type='close')
        #df[all_pairs_high[i]]=preprocess_mt5(symbol=all_pairs[i],start=start_pos,end=end_pos,time_frame=time_frame,data_type='high')
        #df[all_pairs_low[i]]=preprocess_mt5(symbol=all_pairs[i],start=start_pos,end=end_pos,time_frame=time_frame,data_type='low')

    return df


def walk_forward_split(data):

    tot_len = len(data)

    split1 = int(round(tot_len * 0.105, 0))
    split2 = int(round(tot_len * 0.14, 0))
    split3 = int(round(tot_len * 0.245, 0))
    split4 = int(round(tot_len * 0.28, 0))
    split5 = int(round(tot_len * 0.385, 0))
    split6 = int(round(tot_len * 0.42, 0))
    split7 = int(round(tot_len * 0.525, 0))
    split8 = int(round(tot_len * 0.56, 0))
    split9 = int(round(tot_len * 0.665, 0))
    split10 = int(round(tot_len * 0.7, 0))

    walk1 = data.iloc[:split1]
    test1 = data.iloc[split1:split2]
    walk2 = data.iloc[split2:split3]
    test2 = data.iloc[split3:split4]
    walk3 = data.iloc[split4:split5]
    test3 = data.iloc[split5:split6]
    walk4 = data.iloc[split6:split7]
    test4 = data.iloc[split7:split8]
    walk5 = data.iloc[split8:split9]
    test5 = data.iloc[split9:split10]
    final = data.iloc[split10:]

    x = len(walk1) + len(test1) + len(walk2) + len(test2) + len(walk3) + len(test3) + len(walk4) + len(test4) + len(walk5) + len(test5) + len(final)
    y = len(data)

    print(f'Dados tem len de {y} e o split tem len de {x}.')

    return walk1, test1, walk2, test2, walk3, test3, walk4, test4, walk5, test5, final

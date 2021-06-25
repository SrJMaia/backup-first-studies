def pmo_signals(data, signal=True):

    #smothing1 = 8
    #smothing2 = 8
    #smothing3 = 24
    #data['eur_pmo'], data['eur_signal'] = indi.PMO(data['eur'],smothing1,smothing2,smothing3)
    #data['usd_pmo'], data['usd_signal'] = indi.PMO(data['usd'],smothing1,smothing2,smothing3)
    #data['gbp_pmo'], data['gbp_signal'] = indi.PMO(data['gbp'],smothing1,smothing2,smothing3)
    #data['jpy_pmo'], data['jpy_signal'] = indi.PMO(data['jpy'],smothing1,smothing2,smothing3)
    #data['cad_pmo'], data['cad_signal'] = indi.PMO(data['cad'],smothing1,smothing2,smothing3)
    #data['aud_pmo'], data['aud_signal'] = indi.PMO(data['aud'],smothing1,smothing2,smothing3)
    #data['nzd_pmo'], data['nzd_signal'] = indi.PMO(data['nzd'],smothing1,smothing2,smothing3)
    #data['chf_pmo'], data['chf_signal'] = indi.PMO(data['chf'],smothing1,smothing2,smothing3)
    #data = sg.pmo_signals(data, signal=True)

    # PASSAR PARA NUMPY
    
    calc_list = []
    if signal:
        calc_list = SIGNAL_LIST
    else:
        calc_list = PMO_LIST

    for i in range(len(ALL_PAIRS_SELL)):

        results_sell = []
        results_buy = []
        #std1 = data[calc_list[i][0]].std()
        #std2 = data[calc_list[i][1]].std()
        
        single_up = data[calc_list[i][0]].quantile(0.75)
        single_down = data[calc_list[i][0]].quantile(0.25)
        second_up = data[calc_list[i][1]].quantile(0.75)
        second_down = data[calc_list[i][1]].quantile(0.25)

        outlier1_sell = single_up + (1.5 * (single_up - single_down))
        outlier2_sell = second_down - (1.5 * (second_up - second_down))
        outlier1_buy = single_down - (1.5 * (single_up - single_down))
        outlier2_buy = second_up + (1.5 * (second_up - second_down))

        for j in range(len(data)):

            #results_sell.append((data[calc_list[i][0]].iloc[j] > std1) and (data[calc_list[i][1]].iloc[j] < -std2))
            #results_buy.append((data[calc_list[i][0]].iloc[j] < -std1) and (data[calc_list[i][1]].iloc[j] > std2))
            results_sell.append((data[calc_list[i][0]].iloc[j] > outlier1_sell) and (data[calc_list[i][1]].iloc[j] < outlier2_sell))
            results_buy.append((data[calc_list[i][0]].iloc[j] < outlier1_buy) and (data[calc_list[i][1]].iloc[j] > outlier2_buy))

        data[ALL_PAIRS_SELL[i]] = pd.Series(results_sell)
        data[ALL_PAIRS_BUY[i]] = pd.Series(results_buy)

    return data

def pct_data_signals_outlier(data):
# Passar para numpy
    for i in range(len(ALL_PAIRS_BUY)):

        results_buy = []
        results_sell = []

        single_up = data[SPLIT_PAIRS[i][0]].quantile(0.75)
        single_down = data[SPLIT_PAIRS[i][0]].quantile(0.25)
        second_up = data[SPLIT_PAIRS[i][1]].quantile(0.75)
        second_down = data[SPLIT_PAIRS[i][1]].quantile(0.25)

        outlier1_sell = single_up + (1.5 * (single_up - single_down))
        outlier2_sell = second_down - (1.5 * (second_up - second_down))
        outlier1_buy = single_down - (1.5 * (single_up - single_down))
        outlier2_buy = second_up + (1.5 * (second_up - second_down))

        for j in range(len(data)):

            results_sell.append((data[SPLIT_PAIRS[i][0]].iloc[j] > outlier1_sell) and (data[SPLIT_PAIRS[i][1]].iloc[j] < outlier2_sell))
            results_buy.append((data[SPLIT_PAIRS[i][0]].iloc[j] < outlier1_buy) and (data[SPLIT_PAIRS[i][1]].iloc[j] > outlier2_buy))

        data[ALL_PAIRS_SELL[i]] = pd.Series(results_sell)
        data[ALL_PAIRS_BUY[i]] = pd.Series(results_buy)

    return data


def remove_outliers(serie, cut=1.5):

    x = serie.quantile(0.75) + (cut * (serie.quantile(0.75) - serie.quantile(0.25)))
    y = serie.quantile(0.25) - (cut * (serie.quantile(0.75) - serie.quantile(0.25)))
    copy_cat = deque()
    for i in serie:
        if x >= i >= y:
            copy_cat.append(i)
    copy_cat = pd.Series(copy_cat)
    z = copy_cat.std()
    
    return z

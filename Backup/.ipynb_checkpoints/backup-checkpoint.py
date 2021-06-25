    eurcad, euraud, eurnzd, eurgbp, eurjpy, eurchf, eurusd = [], [], [], [], [], [], []
    gbpnzd, gbpusd, gbpcad, gbpjpy, gbpchf, gbpaud = [], [], [], [], [], []
    usdcad, nzdusd, audusd, usdjpy, usdchf = [], [], [], [], []
    nzdjpy, chfjpy, cadjpy, audjpy = [], [], [], []
    nzdchf, cadchf, audchf = [], [], []
    nzdcad, audnzd = [], []
    audcad = []

    EVENTS = {
  'EURUSD':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'eur','second_currency':'usd',
            'symbol':'EURUSD_Open','flag_buy':'EURUSD_buy','flag_sell':'EURUSD_sell','preco_euro':'EURUSD_Open',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'EURCHF':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'eur','second_currency':'chf',
            'symbol':'EURCHF_Open','flag_buy':'EURCHF_buy','flag_sell':'EURCHF_sell','preco_euro':'EURCHF_Open',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'EURGBP':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'eur','second_currency':'gbp',
            'symbol':'EURGBP_Open','flag_buy':'EURGBP_buy','flag_sell':'EURGBP_sell','preco_euro':'EURGBP_Open',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'EURJPY':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'eur','second_currency':'jpy',
            'symbol':'EURJPY_Open','flag_buy':'EURJPY_buy','flag_sell':'EURJPY_sell','preco_euro':'EURJPY_Open',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'EURNZD':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'eur','second_currency':'nzd',
            'symbol':'EURNZD_Open','flag_buy':'EURNZD_buy','flag_sell':'EURNZD_sell','preco_euro':'EURNZD_Open',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'EURAUD':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'eur','second_currency':'aud',
            'symbol':'EURAUD_Open','flag_buy':'EURAUD_buy','flag_sell':'EURAUD_sell','preco_euro':'EURAUD_Open',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'EURCAD':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'eur','second_currency':'cad',
            'symbol':'EURCAD_Open','flag_buy':'EURCAD_buy','flag_sell':'EURCAD_sell','preco_euro':'EURCAD_Open',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},

  'GBPAUD':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'gbp','second_currency':'aud',
            'symbol':'GBPAUD_Open','flag_buy':'GBPAUD_buy','flag_sell':'GBPAUD_sell','preco_euro':'EURGBP_Open',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'GBPCHF':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'gbp','second_currency':'chf',
            'symbol':'GBPCHF_Open','flag_buy':'GBPCHF_buy','flag_sell':'GBPCHF_sell','preco_euro':'EURGBP_Open',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'GBPJPY':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'gbp','second_currency':'jpy',
            'symbol':'GBPJPY_Open','flag_buy':'GBPJPY_buy','flag_sell':'GBPJPY_sell','preco_euro':'EURGBP_Open',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'GBPCAD':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'gbp','second_currency':'cad',
            'symbol':'GBPCAD_Open','flag_buy':'GBPCAD_buy','flag_sell':'GBPCAD_sell','preco_euro':'EURGBP_Open',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'GBPUSD':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'gbp','second_currency':'usd',
            'symbol':'GBPUSD_Open','flag_buy':'GBPUSD_buy','flag_sell':'GBPUSD_sell','preco_euro':'EURGBP_Open',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'GBPNZD':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'gbp','second_currency':'nzd',
            'symbol':'GBPNZD_Open','flag_buy':'GBPNZD_buy','flag_sell':'GBPNZD_sell','preco_euro':'EURGBP_Open',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},

  'USDCHF':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'usd','second_currency':'chf',
            'symbol':'USDCHF_Open','flag_buy':'USDCHF_buy','flag_sell':'USDCHF_sell','preco_euro':'EURUSD_Open',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'USDJPY':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'usd','second_currency':'jpy',
            'symbol':'USDJPY_Open','flag_buy':'USDJPY_buy','flag_sell':'USDJPY_sell','preco_euro':'EURUSD_Open',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'AUDUSD':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'aud','second_currency':'usd',
            'symbol':'AUDUSD_Open','flag_buy':'AUDUSD_buy','flag_sell':'AUDUSD_sell','preco_euro':'EURAUD_Open',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'NZDUSD':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'nzd','second_currency':'usd',
            'symbol':'NZDUSD_Open','flag_buy':'NZDUSD_buy','flag_sell':'NZDUSD_sell','preco_euro':'EURNZD_Open',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'USDCAD':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'usd','second_currency':'cad',
            'symbol':'USDCAD_Open','flag_buy':'USDCAD_buy','flag_sell':'USDCAD_sell','preco_euro':'EURUSD_Open',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},

  'AUDJPY':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'aud','second_currency':'jpy',
            'symbol':'AUDJPY_Open','flag_buy':'AUDJPY_buy','flag_sell':'AUDJPY_sell','preco_euro':'EURAUD_Open',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'CADJPY':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'cad','second_currency':'jpy',
            'symbol':'CADJPY_Open','flag_buy':'CADJPY_buy','flag_sell':'CADJPY_sell','preco_euro':'EURCAD_Open',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'CHFJPY':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'chf','second_currency':'jpy',
            'symbol':'CHFJPY_Open','flag_buy':'CHFJPY_buy','flag_sell':'CHFJPY_sell','preco_euro':'EURCHF_Open',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'NZDJPY':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'nzd','second_currency':'jpy',
            'symbol':'NZDJPY_Open','flag_buy':'NZDJPY_buy','flag_sell':'NZDJPY_sell','preco_euro':'EURNZD_Open',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},

  'AUDCHF':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'aud','second_currency':'chf',
            'symbol':'AUDCHF_Open','flag_buy':'AUDCHF_buy','flag_sell':'AUDCHF_sell','preco_euro':'EURAUD_Open',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'CADCHF':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'cad','second_currency':'chf',
            'symbol':'CADCHF_Open','flag_buy':'CADCHF_buy','flag_sell':'CADCHF_sell','preco_euro':'EURCAD_Open',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'NZDCHF':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'nzd','second_currency':'chf',
            'symbol':'NZDCHF_Open','flag_buy':'NZDCHF_buy','flag_sell':'NZDCHF_sell','preco_euro':'EURNZD_Open',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},

  'AUDNZD':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'aud','second_currency':'nzd',
            'symbol':'AUDNZD_Open','flag_buy':'AUDNZD_buy','flag_sell':'AUDNZD_sell','preco_euro':'EURAUD_Open',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'NZDCAD':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'nzd','second_currency':'cad',
            'symbol':'NZDCAD_Open','flag_buy':'NZDCAD_buy','flag_sell':'NZDCAD_sell','preco_euro':'EURNZD_Open',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},

  'AUDCAD':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'aud','second_currency':'cad',
            'symbol':'AUDCAD_Open','flag_buy':'AUDCAD_buy','flag_sell':'AUDCAD_sell','preco_euro':'EURAUD_Open',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]}
}

def walk_forward_test(data,tot,balance=1000):

    best_balance_result = 1000
    balance_bests_results = pd.DataFrame()
    best_tksl = []

    for j in range(1,tot):

        clear_output(wait=True)
        print(f'{j}/{tot-1}')

        #best_result = 0

        buy_orders = []
        sell_orders = []

        balance_backtest = balance
        list_backtest = [balance_backtest]

        flag_jpy_buy = False
        flag_jpy_sell = False
        flag_normal_buy = False
        flag_normal_sell = False

        tk_normal = j / 10_000
        sl_normal = j / 20_000
        tk_jpy = j / 100
        sl_jpy = j / 200

        my_events = EVENTS

        for i in range(len(data)):

            buy_result = 0
            sell_result = 0

            for h in my_events.values():

                if data[h['flag_buy']].iloc[i] and h['buy']:
                    h['buy_price'] = data[h['symbol']].iloc[i]
                    h['buy'] = False
                    if h['second_currency'] == 'jpy':
                        h['tk_buy'] = data[h['symbol']].iloc[i] + tk_jpy
                        h['sl_buy'] = data[h['symbol']].iloc[i] - sl_jpy
                    else:
                        h['tk_buy'] = data[h['symbol']].iloc[i] + tk_normal
                        h['sl_buy'] = data[h['symbol']].iloc[i] - sl_normal

                if h['buy'] == False and data[h['symbol']].iloc[i] >= h['tk_buy']:
                    balance_backtest, buy_result = finance_calculation(balance_backtest,saldo_inicial=h['tk_buy'],saldo_final=h['buy_price'],eur=h['first_currency'],preco_eur=data[h['preco_euro']].iloc[i],jpy=h['second_currency'])
                    list_backtest.append(balance_backtest)
                    sell_orders.append(buy_result)
                    h['trade_history'].append(buy_result)
                    h['buy'] = True
                elif h['buy'] == False and data[h['symbol']].iloc[i] <= h['sl_buy']:
                    balance_backtest, buy_result = finance_calculation(balance_backtest,saldo_inicial=h['sl_buy'],saldo_final=h['buy_price'],eur=h['first_currency'],preco_eur=data[h['preco_euro']].iloc[i],jpy=h['second_currency'])
                    list_backtest.append(balance_backtest)
                    sell_orders.append(buy_result)
                    h['trade_history'].append(buy_result)
                    h['buy'] = True

                if data[h['flag_sell']].iloc[i] and h['sell']:
                    h['sell_price'] = data[h['symbol']].iloc[i]
                    h['sell'] = False
                    if h['second_currency'] == 'jpy':
                        h['tk_sell'] = data[h['symbol']].iloc[i] - tk_jpy
                        h['sl_sell'] = data[h['symbol']].iloc[i] + sl_jpy
                    else:
                        h['tk_sell'] = data[h['symbol']].iloc[i] - tk_normal
                        h['sl_sell'] = data[h['symbol']].iloc[i] + sl_normal

                if h['sell'] == False and data[h['symbol']].iloc[i] <= h['tk_sell']:
                    balance_backtest, sell_result = finance_calculation(balance_backtest,saldo_inicial=h['sell_price'],saldo_final=h['tk_sell'],eur=h['first_currency'],preco_eur=data[h['preco_euro']].iloc[i],jpy=h['second_currency'])
                    list_backtest.append(balance_backtest)
                    buy_orders.append(sell_result)
                    h['trade_history'].append(sell_result)
                    h['sell'] = True
                elif h['sell'] == False and data[h['symbol']].iloc[i] >= h['sl_sell']:
                    balance_backtest, sell_result = finance_calculation(balance_backtest,saldo_inicial=h['sell_price'],saldo_final=h['sl_sell'],eur=h['first_currency'],preco_eur=data[h['preco_euro']].iloc[i],jpy=h['second_currency'])
                    list_backtest.append(balance_backtest)
                    buy_orders.append(sell_result)
                    h['trade_history'].append(sell_result)
                    h['sell'] = True

        if balance_backtest > best_balance_result:
            balance_bests_results[f'TKSL:{j}'] = pd.Series(list_backtest)
            best_tksl.append(j)
            best_balance_result = balance_backtest


    return balance_bests_results, best_tksl


def finance_calculation(balance, saldo_inicial, saldo_final, iteration=1, risk=0.01, eur='', preco_eur=0, compra=False, jpy=''):
    balance_calc = balance
    if balance < 1000:
        balance_calc = 1000
    #risco = risk * 100
    #alavancagem = 100
    #lot = round(balance_calc // 1000 * 1000 * risco)
    #lot = round(1.12 / iteration * 100_000)
    lot = 0

    if jpy == 'jpy':
        calc = (balance_calc * risk) / (0.01 / saldo_final * 1000)
        if calc > 99.99:
            calc = 99.99
            lot = (calc / iteration * 100_000)
    else:
        calc = (balance_calc * risk) / (0.0001 / saldo_final * 1000)
        if calc > 99.99:
            calc = 99.99
            lot = (calc / iteration * 100_000)

    comission = (lot//1000) * 0.1

    if eur == 'eur':
        if jpy == 'jpy':
            tot = (saldo_inicial - saldo_final) * 1_000
            tot2 = lot * 0.001 / saldo_final
            tot3 = round(tot * tot2 - comission,2)
            return (tot3 + balance), tot3
        else:
            tot = (saldo_inicial - saldo_final) * 100_000
            tot2 = lot * 0.00001 / saldo_final
            tot3 = round(tot * tot2 - comission,2)
            return (tot3 + balance), tot3
    else:
        if jpy == 'jpy':
            tot = (saldo_inicial - saldo_final) * 100_000
            tot2 = lot * 0.001 / saldo_final
            tot3 = round(tot * tot2 / saldo_final / preco_eur - comission,2)
            return (tot3 + balance), tot3
        else:
            tot = (saldo_inicial - saldo_final) * 100_000
            tot2 = lot * 0.00001 / saldo_final
            tot3 = round(tot * tot2 / saldo_final / preco_eur - comission,2)
            return (tot3 + balance), tot3
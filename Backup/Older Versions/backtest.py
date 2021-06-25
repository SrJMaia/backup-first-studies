import pandas as pd
from IPython.display import clear_output

EVENTS = {
  'EURUSD':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'eur','second_currency':'usd',
            'symbol':'EURUSD','flag_buy':'EURUSD_buy','flag_sell':'EURUSD_sell','preco_euro':'EURUSD',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'EURCHF':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'eur','second_currency':'chf',
            'symbol':'EURCHF','flag_buy':'EURCHF_buy','flag_sell':'EURCHF_sell','preco_euro':'EURCHF',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'EURGBP':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'eur','second_currency':'gbp',
            'symbol':'EURGBP','flag_buy':'EURGBP_buy','flag_sell':'EURGBP_sell','preco_euro':'EURGBP',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'EURJPY':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'eur','second_currency':'jpy',
            'symbol':'EURJPY','flag_buy':'EURJPY_buy','flag_sell':'EURJPY_sell','preco_euro':'EURJPY',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'EURNZD':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'eur','second_currency':'nzd',
            'symbol':'EURNZD','flag_buy':'EURNZD_buy','flag_sell':'EURNZD_sell','preco_euro':'EURNZD',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'EURAUD':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'eur','second_currency':'aud',
            'symbol':'EURAUD','flag_buy':'EURAUD_buy','flag_sell':'EURAUD_sell','preco_euro':'EURAUD',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'EURCAD':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'eur','second_currency':'cad',
            'symbol':'EURCAD','flag_buy':'EURCAD_buy','flag_sell':'EURCAD_sell','preco_euro':'EURCAD',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},

  'GBPAUD':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'gbp','second_currency':'aud',
            'symbol':'GBPAUD','flag_buy':'GBPAUD_buy','flag_sell':'GBPAUD_sell','preco_euro':'EURGBP',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'GBPCHF':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'gbp','second_currency':'chf',
            'symbol':'GBPCHF','flag_buy':'GBPCHF_buy','flag_sell':'GBPCHF_sell','preco_euro':'EURGBP',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'GBPJPY':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'gbp','second_currency':'jpy',
            'symbol':'GBPJPY','flag_buy':'GBPJPY_buy','flag_sell':'GBPJPY_sell','preco_euro':'EURGBP',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'GBPCAD':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'gbp','second_currency':'cad',
            'symbol':'GBPCAD','flag_buy':'GBPCAD_buy','flag_sell':'GBPCAD_sell','preco_euro':'EURGBP',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'GBPUSD':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'gbp','second_currency':'usd',
            'symbol':'GBPUSD','flag_buy':'GBPUSD_buy','flag_sell':'GBPUSD_sell','preco_euro':'EURGBP',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'GBPNZD':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'gbp','second_currency':'nzd',
            'symbol':'GBPNZD','flag_buy':'GBPNZD_buy','flag_sell':'GBPNZD_sell','preco_euro':'EURGBP',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},

  'USDCHF':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'usd','second_currency':'chf',
            'symbol':'USDCHF','flag_buy':'USDCHF_buy','flag_sell':'USDCHF_sell','preco_euro':'EURUSD',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'USDJPY':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'usd','second_currency':'jpy',
            'symbol':'USDJPY','flag_buy':'USDJPY_buy','flag_sell':'USDJPY_sell','preco_euro':'EURUSD',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'AUDUSD':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'aud','second_currency':'usd',
            'symbol':'AUDUSD','flag_buy':'AUDUSD_buy','flag_sell':'AUDUSD_sell','preco_euro':'EURAUD',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'NZDUSD':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'nzd','second_currency':'usd',
            'symbol':'NZDUSD','flag_buy':'NZDUSD_buy','flag_sell':'NZDUSD_sell','preco_euro':'EURNZD',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'USDCAD':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'usd','second_currency':'cad',
            'symbol':'USDCAD','flag_buy':'USDCAD_buy','flag_sell':'USDCAD_sell','preco_euro':'EURUSD',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},

  'AUDJPY':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'aud','second_currency':'jpy',
            'symbol':'AUDJPY','flag_buy':'AUDJPY_buy','flag_sell':'AUDJPY_sell','preco_euro':'EURAUD',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'CADJPY':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'cad','second_currency':'jpy',
            'symbol':'CADJPY','flag_buy':'CADJPY_buy','flag_sell':'CADJPY_sell','preco_euro':'EURCAD',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'CHFJPY':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'chf','second_currency':'jpy',
            'symbol':'CHFJPY','flag_buy':'CHFJPY_buy','flag_sell':'CHFJPY_sell','preco_euro':'EURCHF',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'NZDJPY':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'nzd','second_currency':'jpy',
            'symbol':'NZDJPY','flag_buy':'NZDJPY_buy','flag_sell':'NZDJPY_sell','preco_euro':'EURNZD',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},

  'AUDCHF':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'aud','second_currency':'chf',
            'symbol':'AUDCHF','flag_buy':'AUDCHF_buy','flag_sell':'AUDCHF_sell','preco_euro':'EURAUD',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'CADCHF':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'cad','second_currency':'chf',
            'symbol':'CADCHF','flag_buy':'CADCHF_buy','flag_sell':'CADCHF_sell','preco_euro':'EURCAD',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'NZDCHF':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'nzd','second_currency':'chf',
            'symbol':'NZDCHF','flag_buy':'NZDCHF_buy','flag_sell':'NZDCHF_sell','preco_euro':'EURNZD',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},

  'AUDNZD':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'aud','second_currency':'nzd',
            'symbol':'AUDNZD','flag_buy':'AUDNZD_buy','flag_sell':'AUDNZD_sell','preco_euro':'EURAUD',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},
  'NZDCAD':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'nzd','second_currency':'cad',
            'symbol':'NZDCAD','flag_buy':'NZDCAD_buy','flag_sell':'NZDCAD_sell','preco_euro':'EURNZD',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]},

  'AUDCAD':{'buy':True,'sell':True,'buy_price':0,'sell_price':0,'first_currency':'aud','second_currency':'cad',
            'symbol':'AUDCAD','flag_buy':'AUDCAD_buy','flag_sell':'AUDCAD_sell','preco_euro':'EURAUD',
            'tk_sell':0,'sl_sell':0,'tk_buy':0,'sl_buy':0,'trade_history':[]}
}

def finance_calculation(balance, saldo_inicial, saldo_final, iteration=1, risk=0.01, eur='', preco_eur=0, compra=False, jpy=''):
    balance_calc = balance
    if balance < 1000:
        balance_calc = 1000
    risco = risk * 100
    #alavancagem = 100
    # Usar o risco como alavancagem. Assim eu multiplico o capital * Risco
    #lot = round(balance_calc // 1000 * 1000 * risco)
    lot = 10_000

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


def pip_calculation(pip_balance,preco_inicial, preco_final):
    pip = preco_inicial - preco_final
    return pip + pip_balance


def pct_backtest(data, risco=0.01 , tksl=1, balance=1000, single=True, tot=1):
    """
    Se single False e for um multi test
    Mudar o valor de tot, pois alem do tamanho das iterações
    tot será usado como TP e SL
    """

    best_balance_result = balance
    balance_bests_results = pd.DataFrame()
    best_tksl = []

    risk = risco

    x = 0
    if single:
        x = list(range(1,2))
    else:
        x = list(range(1,tot))

    for j in x:

        if not single:
            clear_output(wait=True)
            print(f'{j}/{tot-1}')

        buy_orders = []
        sell_orders = []

        balance_backtest = balance
        list_backtest = [balance_backtest]

        flag_jpy_buy, flag_jpy_sell = False, False
        flag_normal_buy, flag_normal_sell = False, False

        tk_normal, sl_normal, tk_jpy, sl_jpy = 0, 0, 0, 0
        if single:
            tk_normal = tksl / 10000
            sl_normal = tksl / 20000
            tk_jpy = tksl / 100
            sl_jpy = tksl / 200
        else:
            tk_normal = j / 10000
            sl_normal = j / 20000
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
                    balance_backtest, buy_result = finance_calculation(balance=balance_backtest, iteration = tksl if single else j, risk = risk, saldo_inicial=h['tk_buy'],
                                                                       saldo_final=h['buy_price'], eur=h['first_currency'],
                                                                       preco_eur=data[h['preco_euro']].iloc[i], jpy=h['second_currency'])
                    list_backtest.append(balance_backtest)
                    buy_orders.append(buy_result)
                    h['trade_history'].append(buy_result)
                    h['buy'] = True
                elif h['buy'] == False and data[h['symbol']].iloc[i] <= h['sl_buy']:
                    balance_backtest, buy_result = finance_calculation(balance=balance_backtest, iteration = tksl if single else j, risk=risk, saldo_inicial=h['sl_buy'],
                                                                       saldo_final=h['buy_price'], eur=h['first_currency'],
                                                                       preco_eur=data[h['preco_euro']].iloc[i], jpy=h['second_currency'])
                    list_backtest.append(balance_backtest)
                    buy_orders.append(buy_result)
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
                    balance_backtest, sell_result = finance_calculation(balance=balance_backtest, iteration = tksl if single else j, risk=risk, saldo_inicial=h['sell_price'],
                                                                        saldo_final=h['tk_sell'], eur=h['first_currency'],
                                                                        preco_eur=data[h['preco_euro']].iloc[i], jpy=h['second_currency'])
                    list_backtest.append(balance_backtest)
                    sell_orders.append(sell_result)
                    h['trade_history'].append(sell_result)
                    h['sell'] = True
                elif h['sell'] == False and data[h['symbol']].iloc[i] >= h['sl_sell']:
                    balance_backtest, sell_result = finance_calculation(balance=balance_backtest, iteration = tksl if single else j, risk=risk,saldo_inicial=h['sell_price'],
                                                                        saldo_final=h['sl_sell'], eur=h['first_currency'],
                                                                        preco_eur=data[h['preco_euro']].iloc[i], jpy=h['second_currency'])
                    list_backtest.append(balance_backtest)
                    sell_orders.append(sell_result)
                    h['trade_history'].append(sell_result)
                    h['sell'] = True

        if single:
            balance_bests_results['result'] = pd.Series(list_backtest)
            balance_bests_results['buy'] = pd.Series(buy_orders)
            balance_bests_results['sell'] = pd.Series(sell_orders)
            for h in my_events:
                balance_bests_results[my_events[h]['symbol']] = pd.Series(my_events[h]['trade_history'])
            return balance_bests_results
        else:
            if balance_backtest > balance:
                balance_bests_results[f'TKSL:{j}'] = pd.Series(list_backtest)
                best_tksl.append(j)
                best_balance_result = balance_backtest

    balance_bests_results['best_tksl'] = pd.Series(best_tksl)
    return balance_bests_results


def pct_backtest_without_tpsl(data, risco=0.01, balance=1000):

    best_balance_result = balance
    balance_bests_results = pd.DataFrame()
    best_tksl = []

    buy_orders = []
    sell_orders = []

    balance_backtest = balance
    list_backtest = [balance_backtest]

    flag_jpy_buy, flag_jpy_sell = False, False
    flag_normal_buy, flag_normal_sell = False, False

    my_events = EVENTS

    for i in range(len(data)):

        clear_output(wait=True)
        print(f'{i}/{len(data)-1}')

        buy_result = 0
        sell_result = 0

        for h in my_events.values():

            if data[h['flag_buy']].iloc[i] and h['buy']:
                if not h['sell']:
                    h['buy_price'] = data[h['symbol']].iloc[i]
                    h['buy'] = False
                    h['sell'] = True
                    balance_backtest, sell_result = finance_calculation(balance=balance_backtest,  risk=risco, saldo_inicial=h['sell_price'],
                                                                        saldo_final=data[h['symbol']].iloc[i], eur=h['first_currency'],
                                                                        preco_eur=data[h['preco_euro']].iloc[i], jpy=h['second_currency'])
                    list_backtest.append(balance_backtest)
                    sell_orders.append(sell_result)
                    h['trade_history'].append(sell_result)
                else:
                    h['buy_price'] = data[h['symbol']].iloc[i]
                    h['buy'] = False

            if data[h['flag_sell']].iloc[i] and h['sell']:
                if not h['buy']:
                    h['sell_price'] = data[h['symbol']].iloc[i]
                    h['sell'] = False
                    h['buy'] = True
                    balance_backtest, buy_result = finance_calculation(balance=balance_backtest,  risk=risco, saldo_inicial=data[h['symbol']].iloc[i],
                                                                       saldo_final=h['buy_price'], eur=h['first_currency'],
                                                                       preco_eur=data[h['preco_euro']].iloc[i], jpy=h['second_currency'])
                    list_backtest.append(balance_backtest)
                    buy_orders.append(buy_result)
                    h['trade_history'].append(buy_result)
                else:
                    h['sell_price'] = data[h['symbol']].iloc[i]
                    h['sell'] = False


    balance_bests_results['result'] = pd.Series(list_backtest)
    balance_bests_results['buy'] = pd.Series(buy_orders)
    balance_bests_results['sell'] = pd.Series(sell_orders)
    for h in my_events:
        balance_bests_results[my_events[h]['symbol']] = pd.Series(my_events[h]['trade_history'])
    return balance_bests_results

import numpy as np
from numba import njit

@njit(fastmath=True)
def finance_calculation(balance, saldo_inicial, saldo_final, preco_eur, eur):

    initial_balance = 1000
    lot = 1000

    #if balance > (3*initial_balance):
    #    lot = (balance - initial_balance) // 1000 * 1000

    comission = (lot//1000) * 0.07
    #overnight = (lot//1000) * 0.1
    # random entre -2 a 2 pips para simular slippage

    if eur:
        tot = (lot * (saldo_inicial - saldo_final)) / saldo_final
        tot2 = tot - comission
        return (tot2 + balance), tot2
    else:
        tot = (lot * (saldo_inicial - saldo_final)) / saldo_final
        tot2 = tot / saldo_final / preco_eur - comission
        return (tot2 + balance), tot2


@njit
def tpsl_calc(price, multiply_tp, multiply_sl, tpsl_value=0, jpy=False, buy=True, fix_tpsl = False):
    tp, sl = 0, 0
    round_tpsl = 3 if jpy else 5
    if fix_tpsl:
        if buy:
            tp = round(price + multiply_tp, round_tpsl)
            sl = round(price - multiply_sl, round_tpsl)
        elif not buy:
            tp = round(price - multiply_tp, round_tpsl)
            sl = round(price + multiply_sl, round_tpsl)
    else:
        if buy:
            tp = price + round(multiply_tp * tpsl_value, round_tpsl)
            sl = price - round(multiply_sl * tpsl_value, round_tpsl)
        elif not buy:
            tp = price - round(multiply_tp * tpsl_value, round_tpsl)
            sl = price + round(multiply_sl * tpsl_value, round_tpsl)

    return tp, sl


@njit(parallel=True)
def single_backtest(array, multiply_tp, multiply_sl, fix_tpsl = False, jpy = False, balance = 1000):
    """
    Caso for operar moedas nao eur, mudar o sistema do array
    array = [0] Open
            [1] High
            [2] Low
            [3] Close
            [4] Preços do TimeFrame
            [5] TPSL
            [6] Sell Flag
            [7] Buy Flag
    tpsl = TakeProfit e StopLoss int > 0
    multiply_tpsl = float > 0
                    Será o valor que irá dividir SL
                    Se 1 significa risco 1:1, se 2, 2:1 and so on
    fix_tpsl = Se True, multiply_tp e sl deverão ser um valor fixo para calculo
    ---
    buy_sell: 0 = Compra
              1 = Venda
    operacao_info: 0 = Preço de Compra
                   1 = Preço de Venda
                   2 = TP Venda
                   3 = SL Venda
                   4 = TP Compra
                   5 = SL Compra
    """

    balance_backtest = balance

    operacao_info = np.zeros((6),dtype=np.float32)
    buy_sell = np.ones((2),dtype=np.bool_)

    buy_sell_tot_trades_indi = np.zeros(3, dtype=np.int32)

    buy_orders = np.zeros((array[7].size), dtype=np.float32)
    sell_orders = np.zeros((array[6].size), dtype=np.float32)
    buy_orders[0] = balance_backtest
    sell_orders[0] = balance_backtest
    buy_sell_tot_trades_indi[0] += 1
    buy_sell_tot_trades_indi[1] += 1

    tot_trades = np.zeros(((array[7].size+array[6].size)), dtype=np.float32)
    tot_trades[0] = balance_backtest
    buy_sell_tot_trades_indi[2] += 1

    #tk_normal = round(tpsl / 10000,5)
    #sl_normal = round(tpsl / 10000 / multiply_tpsl, 5)
    #tk_jpy = round(tpsl / 100)
    #sl_jpy = round(tpsl / 100 / multiply_tpsl,5)

    for i in np.arange(array[0].size): # Array tamanho

        if not np.isnan(array[4, i]):

            if array[7, i] == 1. and buy_sell[0] == 1.: #Compra
                operacao_info[0] = array[4, i]
                buy_sell[0] = False
                operacao_info[4], operacao_info[5] = tpsl_calc(price=array[4, i],
                                                                multiply_tp=multiply_tp,
                                                                multiply_sl=multiply_sl,
                                                                tpsl_value=array[5, i],
                                                                jpy=jpy, buy=True,
                                                                fix_tpsl=fix_tpsl)
            elif array[6, i] == 1. and buy_sell[1] == 1.:
                operacao_info[1] = array[4, i]
                buy_sell[1] = False
                operacao_info[2], operacao_info[3] = tpsl_calc(price=array[4, i],
                                                                multiply_tp=multiply_tp,
                                                                multiply_sl=multiply_sl,
                                                                tpsl_value=array[5, i],
                                                                jpy=jpy, buy=False,
                                                                fix_tpsl=fix_tpsl)

        if np.isnan(array[4, i]):
            if buy_sell[0] == False and (array[[0, 1, 2, 3], i] <= operacao_info[5]).sum() > 0:
                balance_backtest, buy_result = finance_calculation(balance=balance_backtest,
                                                                    saldo_inicial=operacao_info[5],
                                                                    saldo_final=operacao_info[0],
                                                                    eur = eur,
                                                                    preco_eur=1)
                tot_trades[buy_sell_tot_trades_indi[2]] = balance_backtest
                buy_orders[buy_sell_tot_trades_indi[0]] = buy_orders[buy_sell_tot_trades_indi[0]-1] + buy_result
                buy_sell_tot_trades_indi[0] += 1
                buy_sell_tot_trades_indi[2] += 1
                buy_sell[0] = True
            elif buy_sell[0] == False and (array[[0, 1, 2, 3], i] >= operacao_info[4]).sum() > 0:
                balance_backtest, buy_result = finance_calculation(balance=balance_backtest,
                                                                    saldo_inicial=operacao_info[4],
                                                                    saldo_final=operacao_info[0],
                                                                    eur = eur,
                                                                    preco_eur=1)
                tot_trades[buy_sell_tot_trades_indi[2]] = balance_backtest
                buy_orders[buy_sell_tot_trades_indi[0]] = buy_orders[buy_sell_tot_trades_indi[0]-1] + buy_result
                buy_sell_tot_trades_indi[0] += 1
                buy_sell_tot_trades_indi[2] += 1
                buy_sell[0] = True

            if buy_sell[1] == False and (array[[0, 1, 2, 3], i] >= operacao_info[3]).sum() > 0:
                balance_backtest, sell_result = finance_calculation(balance=balance_backtest,saldo_inicial=operacao_info[1],
                                                                    saldo_final=operacao_info[3], eur = eur,
                                                                    preco_eur=1)
                tot_trades[buy_sell_tot_trades_indi[2]] = balance_backtest
                sell_orders[buy_sell_tot_trades_indi[1]] = sell_orders[buy_sell_tot_trades_indi[1]-1] + sell_result
                buy_sell_tot_trades_indi[1] += 1
                buy_sell_tot_trades_indi[2] += 1
                buy_sell[1] = True
            elif buy_sell[1] == False and (array[[0, 1, 2, 3], i] <= operacao_info[2]).sum() > 0:
                balance_backtest, sell_result = finance_calculation(balance=balance_backtest, saldo_inicial=operacao_info[1],
                                                                    saldo_final=operacao_info[2], eur = eur,
                                                                    preco_eur=1)
                tot_trades[buy_sell_tot_trades_indi[2]] = balance_backtest
                sell_orders[buy_sell_tot_trades_indi[1]] = sell_orders[buy_sell_tot_trades_indi[1]-1] + sell_result
                buy_sell_tot_trades_indi[1] += 1
                buy_sell_tot_trades_indi[2] += 1
                buy_sell[1] = True

    return tot_trades, sell_orders, buy_orders

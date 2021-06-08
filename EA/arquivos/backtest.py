import numpy as np
from numba import njit

@njit
def finance_calculation(balance, saldo_inicial, saldo_final, preco_eur):

    initial_balance = 1000
    lot = 1000

    #if balance > (3*initial_balance):
    #    lot = (balance - initial_balance) // 1000 * 1000

    comission = (lot//1000) * 0.07
    #overnight = (lot//1000) * 0.1
    # random entre -2 a 2 pips para simular slippage

    result = (lot * (saldo_inicial - saldo_final)) / preco_eur - comission
    return (result + balance), result


@njit
def check_tpsl_exit(price1, price2, price3, tpsl, higher=True):
    result = False
    if higher:
        result = (price1 >= tpsl) or (price2 >= tpsl) or (price3 >= tpsl)
    elif not higher:
        result = (price1 <= tpsl) or (price2 <= tpsl) or (price3 <= tpsl)
    return result


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
            tp = round(price + (multiply_tp * tpsl_value), round_tpsl)
            sl = round(price - (multiply_sl * tpsl_value), round_tpsl)
        elif not buy:
            tp = round(price - (multiply_tp * tpsl_value), round_tpsl)
            sl = round(price + (multiply_sl * tpsl_value), round_tpsl)

    return tp, sl


@njit
def single_backtest(array, multiply_tp, multiply_sl, size_buy=0, size_sell=0, jpy=False, universal_flag=True, fix_tpsl = False, balance = 1000):
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
    size_array = lista, 0 = tamanho sell_flag
                        1 = tamanho buy_flag
    universal_flag = apenas uma flag para compra e venda
    fix_tpsl = Se True, multiply_tp e sl deverão ser um valor fixo para calculo
    ---
    buy_sell: 0 = Compra
              1 = Venda
              2 = uni_flag
    operacao_info: 0 = Preço de Compra
                   1 = Preço de Venda
                   2 = TP Venda
                   3 = SL Venda
                   4 = TP Compra
                   5 = SL Compra

    OBS: SE FUTURAMENTE FOR USAR UM PAR QUE NÃO CONTENHA EUR, MODIFICAR
    O ARRAY DE ACESSO array[4, i] NO finance_calculation
    """

    balance_backtest = balance

    operacao_info = np.zeros((6),dtype=np.float32)
    buy_sell = np.ones((3),dtype=np.bool_)

    buy_sell_tot_trades_indi = np.zeros(3, dtype=np.int32)
    buy_indi, sell_indi, tot_trades_indi = 0, 0, 0

    tot_trades = np.zeros(((size_buy+size_sell)), dtype=np.float32)
    buy_orders = np.zeros((size_buy), dtype=np.float32)
    sell_orders = np.zeros((size_sell), dtype=np.float32)
    tot_trades[0] = balance_backtest
    buy_orders[0] = balance_backtest
    sell_orders[0] = balance_backtest
    buy_indi += 1
    sell_indi += 1
    tot_trades_indi += 1

    for i in np.arange(array[0].size): # Array tamanho

        buy_result, sell_result = 0, 0

        if universal_flag:
            """
            Há um bug que nao funciona, não sei o motivo
            """
            if not np.isnan(array[4, i]):
                if array[7, i] and buy_sell[0]: #Compra
                    operacao_info[0] = array[4, i]
                    operacao_info[4], operacao_info[5] = tpsl_calc(price=array[4, i],
                                                                    multiply_tp=multiply_tp,
                                                                    multiply_sl=multiply_sl,
                                                                    tpsl_value=array[5, i],
                                                                    jpy=jpy,
                                                                    buy=True,
                                                                    fix_tpsl=fix_tpsl)
                    buy_sell[2] = False
                elif array[6, i] and buy_sell[1]:
                    operacao_info[1] = array[4, i]
                    operacao_info[2], operacao_info[3] = tpsl_calc(price=array[4, i],
                                                                    multiply_tp=multiply_tp,
                                                                    multiply_sl=multiply_sl,
                                                                    tpsl_value=array[5, i],
                                                                    jpy=jpy,
                                                                    buy=False,
                                                                    fix_tpsl=fix_tpsl)
                    buy_sell[2] = False
            elif np.isnan(array[4, i]):
                if buy_sell[2] == False and check_tpsl_exit(array[0][i], array[1][i], array[2][i], operacao_info[5], higher=False):
                    balance_backtest, buy_result = finance_calculation(balance=balance_backtest,
                                                                        saldo_inicial=operacao_info[5],
                                                                        saldo_final=operacao_info[0],
                                                                        preco_eur=operacao_info[5])
                    tot_trades[tot_trades_indi] = balance_backtest
                    buy_orders[buy_indi] = buy_orders[buy_indi-1] + buy_result
                    buy_indi += 1
                    tot_trades_indi += 1
                    buy_sell[2] = True
                elif buy_sell[2] == False and check_tpsl_exit(array[0][i], array[1][i], array[2][i], operacao_info[4], higher=True):
                    balance_backtest, buy_result = finance_calculation(balance=balance_backtest,
                                                                        saldo_inicial=operacao_info[4],
                                                                        saldo_final=operacao_info[0],
                                                                        preco_eur=operacao_info[4])
                    tot_trades[tot_trades_indi] = balance_backtest
                    buy_orders[buy_indi] = buy_orders[buy_indi-1] + buy_result
                    buy_indi += 1
                    tot_trades_indi += 1
                    buy_sell[2] = True
                elif buy_sell[2] == False and check_tpsl_exit(array[0][i], array[1][i], array[2][i], operacao_info[3], higher=True):
                    balance_backtest, sell_result = finance_calculation(balance=balance_backtest,
                                                                        saldo_inicial=operacao_info[1],
                                                                        saldo_final=operacao_info[3],
                                                                        preco_eur=operacao_info[1])
                    tot_trades[tot_trades_indi] = balance_backtest
                    sell_orders[sell_indi] = sell_orders[sell_indi-1] + sell_result
                    sell_indi += 1
                    tot_trades_indi += 1
                    buy_sell[2] = True
                elif buy_sell[2] == False and check_tpsl_exit(array[0][i], array[1][i], array[2][i], operacao_info[2], higher=False):
                    balance_backtest, sell_result = finance_calculation(balance=balance_backtest,
                                                                        saldo_inicial=operacao_info[1],
                                                                        saldo_final=operacao_info[2],
                                                                        preco_eur=operacao_info[1])
                    tot_trades[tot_trades_indi] = balance_backtest
                    sell_orders[sell_indi] = sell_orders[sell_indi-1] + sell_result
                    sell_indi += 1
                    tot_trades_indi += 1
                    buy_sell[2] = True
        elif not universal_flag: # UNIVERSAL FLAG
            if not np.isnan(array[4, i]):
                if array[7, i] and buy_sell[0]: #Compra
                    operacao_info[0] = array[4, i]
                    operacao_info[4], operacao_info[5] = tpsl_calc(price=array[4, i],
                                                                    multiply_tp=multiply_tp,
                                                                    multiply_sl=multiply_sl,
                                                                    tpsl_value=array[5, i],
                                                                    jpy=jpy,
                                                                    buy=True,
                                                                    fix_tpsl=fix_tpsl)
                    buy_sell[0] = False
                elif array[6, i] and buy_sell[1]:
                    operacao_info[1] = array[4, i]
                    operacao_info[2], operacao_info[3] = tpsl_calc(price=array[4, i],
                                                                    multiply_tp=multiply_tp,
                                                                    multiply_sl=multiply_sl,
                                                                    tpsl_value=array[5, i],
                                                                    jpy=jpy,
                                                                    buy=False,
                                                                    fix_tpsl=fix_tpsl)
                    buy_sell[1] = False
            elif np.isnan(array[4, i]):
                if buy_sell[0] == False and check_tpsl_exit(array[0][i], array[1][i], array[2][i], operacao_info[5], higher=False):
                    balance_backtest, buy_result = finance_calculation(balance=balance_backtest,
                                                                        saldo_inicial=operacao_info[5],
                                                                        saldo_final=operacao_info[0],
                                                                        preco_eur=operacao_info[5])
                    tot_trades[tot_trades_indi] = balance_backtest
                    buy_orders[buy_indi] = buy_orders[buy_indi-1] + buy_result
                    buy_indi += 1
                    tot_trades_indi += 1
                    buy_sell[0] = True
                elif buy_sell[0] == False and check_tpsl_exit(array[0][i], array[1][i], array[2][i], operacao_info[4], higher=True):
                    balance_backtest, buy_result = finance_calculation(balance=balance_backtest,
                                                                        saldo_inicial=operacao_info[4],
                                                                        saldo_final=operacao_info[0],
                                                                        preco_eur=operacao_info[4])
                    tot_trades[tot_trades_indi] = balance_backtest
                    buy_orders[buy_indi] = buy_orders[buy_indi-1] + buy_result
                    buy_indi += 1
                    tot_trades_indi += 1
                    buy_sell[0] = True
                elif buy_sell[1] == False and check_tpsl_exit(array[0][i], array[1][i], array[2][i], operacao_info[3], higher=True):
                    balance_backtest, sell_result = finance_calculation(balance=balance_backtest,
                                                                        saldo_inicial=operacao_info[1],
                                                                        saldo_final=operacao_info[3],
                                                                        preco_eur=operacao_info[1])
                    tot_trades[tot_trades_indi] = balance_backtest
                    sell_orders[sell_indi] = sell_orders[sell_indi-1] + sell_result
                    sell_indi += 1
                    tot_trades_indi += 1
                    buy_sell[1] = True
                elif buy_sell[1] == False and check_tpsl_exit(array[0][i], array[1][i], array[2][i], operacao_info[2], higher=False):
                    balance_backtest, sell_result = finance_calculation(balance=balance_backtest,
                                                                        saldo_inicial=operacao_info[1],
                                                                        saldo_final=operacao_info[2],
                                                                        preco_eur=operacao_info[1])
                    tot_trades[tot_trades_indi] = balance_backtest
                    sell_orders[sell_indi] = sell_orders[sell_indi-1] + sell_result
                    sell_indi += 1
                    tot_trades_indi += 1
                    buy_sell[1] = True

    return tot_trades, sell_orders, buy_orders

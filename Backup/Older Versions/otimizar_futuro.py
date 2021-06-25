from collections import deque
from IPython.display import clear_output


def finance_calculation(balance, saldo_inicial, saldo_final):

    initial_balance = 1000

    lot = initial_balance

    calc = balance - initial_balance

    #if balance > initial_balance:
        #lot = (balance + (calc * 0.025)) // 1000 * 1000

    comission = (lot//1000) * 0.1

    tot = (lot * (saldo_inicial - saldo_final)) / saldo_final
    tot2 = round(tot - comission,2)
    return (tot2 + balance), tot2

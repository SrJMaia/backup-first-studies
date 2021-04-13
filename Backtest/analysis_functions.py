import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def compare(test_columns):

    # Futurametne arrumar isso
    a1 = set(test_columns[0])
    b2 = set(test_columns[1])
    c3 = set(test_columns[2])
    d4 = set(test_columns[3])
    e5 = set(test_columns[4])
    f6 = set(test_columns[5])
    g7 = set(test_columns[6])
    h8 = set(test_columns[7])
    j9 = set(test_columns[8])
    k10 = set(test_columns[9])
    l11 = set(test_columns[10])
    m12 = set(test_columns[11])

    x = set.intersection(a1, b2, c3, d4, e5, f6, g7, h8, j9, k10, l11, m12)

    return list(x)


def outliers_calc(series, bins=100,no_return=False):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3-q1
    lower = q1 - (1.5 * iqr)
    upper = q3 + (1.5 * iqr)
    a = series[series < lower].count()
    b = series[series > upper].count()
    print(f"""
    Lower: {lower} | Upper: {upper}
    Lower Total: {a} | Upper Total: {b}
    Total Outliers: {a+b}
    Total Outliers %: {round((a+b)/series.count()*100,4)}%
    """)
    plt.hist(series,bins=bins)
    plt.grid()
    plt.axvline(x=lower,color='r')
    plt.axvline(x=upper,color='r')
    plt.show()
    if no_return:
        return lower, upper


# Backtest Analysis
def backtest_analysis(series, trades_buy, trades_sell, tot_trades, test_number=0):
    series.dropna(inplace=True)
    gross_profit, gross_loss = 0.0, 0.0
    total_profit_trades, total_loss_trades, total_trades = 0, 0, 0
    total_loss_trades_list, total_profit_trades_list = [], []
    for i in series.diff():
        if i < 0:
            gross_loss += i
            total_loss_trades += 1
            total_loss_trades_list.append(i)
        elif i > 0:
            gross_profit += i
            total_profit_trades += 1
            total_profit_trades_list.append(i)
    total_loss_trades_list = pd.Series(total_loss_trades_list)
    total_profit_trades_list = pd.Series(total_profit_trades_list)
    initial_balance = series.iloc[0]
    total_trades = total_profit_trades + total_loss_trades
    per_win = round(total_profit_trades/total_trades*100,2)
    per_loss = round(total_loss_trades/total_trades*100,2)
    net_profit = round(series.iloc[-1]-1000,2)
    gross_profit = round(gross_profit,2)
    gross_loss = round(gross_loss,2)
    equity_drawdown_maximal = round(series.min()-series.iloc[0],2)
    equity_drawdown_relative = round((1-(series.min()/series.iloc[0]))*100,2)
    profit_factor = abs(round(gross_profit/gross_loss,2))
    recovery_factor = 0
    if equity_drawdown_maximal == 0:
        recovery_factor = round(net_profit/1,2)
    else:
        recovery_factor = round(net_profit/abs(equity_drawdown_maximal),2)
    buy_percentage_won = round(len(trades_buy[trades_buy > 0]) / len(trades_buy) * 100,2)
    buy_percentage_loss = round((1 -(buy_percentage_won / 100)) * 100,2)
    buy_won_trades = len(trades_buy[trades_buy > 0])
    buy_profit = round(trades_buy[trades_buy > 0].sum(),2)
    buy_profit_mean = round(trades_buy[trades_buy > 0].mean(),2)
    buy_profit_median = round(trades_buy[trades_buy > 0].median(),2)
    buy_profit_std = round(trades_buy[trades_buy > 0].std(),2)
    buy_loss_trades = len(trades_buy[trades_buy < 0])
    buy_loss = round(trades_buy[trades_buy < 0 ].sum(),2)
    buy_loss_mean = round(trades_buy[trades_buy < 0 ].mean(),2)
    buy_loss_median = round(trades_buy[trades_buy < 0 ].median(),2)
    buy_loss_std = round(trades_buy[trades_buy < 0 ].std(),2)
    sell_percentage_won = round(len(trades_sell[trades_sell > 0]) / len(trades_sell) * 100,2)
    sell_percentage_loss = (1 -(sell_percentage_won / 100)) * 100
    sell_won_trades = len(trades_sell[trades_sell > 0])
    sell_profit = round(trades_sell[trades_sell > 0].sum(),2)
    sell_profit_mean = round(trades_sell[trades_sell > 0].mean(),2)
    sell_profit_median = round(trades_sell[trades_sell > 0].median(),2)
    sell_profit_std = round(trades_sell[trades_sell > 0].std(),2)
    sell_loss_trades = len(trades_sell[trades_sell < 0])
    sell_loss = round(trades_sell[trades_sell < 0 ].sum(),2)
    sell_loss_mean = round(trades_sell[trades_sell < 0 ].mean(),2)
    sell_loss_median = round(trades_sell[trades_sell < 0 ].median(),2)
    sell_loss_std = round(trades_sell[trades_sell < 0 ].std(),2)

    average_win_size = pd.Series(total_profit_trades_list).mean()
    average_loss_size = pd.Series(total_loss_trades_list).mean()
    reward_risk_ratio = round(abs(average_win_size / average_loss_size))

        # Expectancy
    # Learning Markets
    expectancy_learning_markets = round(((reward_risk_ratio * (per_win/100)) - (per_loss/100))*100,2)
    # Vantage Point Trading
    expectancy_vantage_point_trading = round(((per_win/100)*average_win_size)-((per_loss/100)*average_loss_size))
    # Livro
    expectancy_livro = round((average_win_size*per_win+average_loss_size*per_loss)/(-average_loss_size),2)

    print(f'''

                Geral

    Teste: {test_number}
    Capital Inicial: {initial_balance}€
    Total de Trades: {total_trades}
    Lucro Liquido: {net_profit}€
    Lucro Bruto: {gross_profit}€
    Perda Bruta: {gross_loss}€
    Média Lucro: {round(series.mean(),2)}€
    Mediana Lucro: {round(series.median(),2)}€
    Desvio Padrão Lucro: {round(series.std(),2)}€
    Razão Risco Lucro: {reward_risk_ratio}
    Maximo Rebaixamento do Capital: {equity_drawdown_maximal}€
    Rebaixamento Relativo ao Capital: {equity_drawdown_relative}%

                Expectancy

    Learning Markets: {expectancy_learning_markets}%
    OBS: Superficialmente, isso significa que em média essa estratégia trará um retorno de {(expectancy_learning_markets)/100} vezes o tamanho da sua perca.
    Vantage Point Trading: {expectancy_vantage_point_trading}€
    OBS: É esperado receber x€ em cada trade.
    Livro: {expectancy_livro}
    OBS: Para cada 1€ arriscado é esperado receber x% dele. Preferência >0.1

    --//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--

                Vitória e Derrotas

    Total de Trades Vitoriosos: {total_profit_trades}
    Média de Lucro: {round(total_profit_trades_list.mean(),2)}€
    Mediana de Lucro: {round(total_profit_trades_list.median(),2)}€
    Desvio Padrão do Lucro: {round(total_profit_trades_list.std(),2)}€
    Porcentagem de Vitória: {per_win}%
    Total de Trades Perdidos: {total_loss_trades}
    Média de Prejuízo: {round(total_loss_trades_list.mean(),2)}€
    Mediana do Prejuízo: {round(total_loss_trades_list.median(),2)}€
    Desvio Padrão do Prejuízo: {round(total_loss_trades_list.std(),2)}€
    Porcentagem de Derrota: {per_loss}%
    Fator Lucro: {profit_factor}
    OBS: Fator Lucro > 1.5
    Fator de Recuperação: {recovery_factor}

    --//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--

                Geral

    Porcentagem de Vitória: {buy_percentage_won}%
    Porcentagem de Derrota: {buy_percentage_loss}%

                Buy

    Trades Vitoriosos: {buy_won_trades}
    Lucro Total: {buy_profit}€
    Média Lucro: {buy_profit_mean}€
    Mediana Lucro: {buy_profit_median}€
    Desvio Padrão: {buy_profit_std}€

    Trades Perdidos: {buy_loss_trades}
    Lucro Total: {buy_loss}€
    Média Prejuízo: {buy_loss_mean}€
    Mediana Prejuízo: {buy_loss_median}€
    Desvio Padrão: {buy_loss_std}€

    --//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--

                Geral

    Porcentagem de Vitória: {sell_percentage_won}%
    Porcentagem de Derrota: {sell_percentage_loss}%

                Sell

    Trades Vitoriosos: {sell_won_trades}
    Lucro Total: {sell_profit}€
    Média Lucro: {sell_profit_mean}€
    Mediana Lucro: {sell_profit_median}€
    Desvio Padrão: {sell_profit_std}€

    Trades Perdidos: {sell_loss_trades}
    Lucro Total: {sell_loss}€
    Média Prejuízo: {sell_loss_mean}€
    Mediana Prejuízo: {sell_loss_median}€
    Desvio Padrão: {sell_loss_std}€

    --//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--

                Cada Par
    ''')
    plot_per_won, plot_per_loss = [], []
    plot_tot_won, plot_tot_loss = [], []
    plot_profit_brut, plot_loss_brut = [], []
    plot_profit_mean, plot_loss_mean = [], []
    plot_profit_median, plot_loss_median = [], []
    plot_profit_std, plot_loss_std = [], []
    colors = []

    tot_dict = tot_trades.to_dict()

    for i in tot_dict:
        plot_per_won.append(round((len(tot_trades[i][tot_trades[i] > 0]) / len(tot_trades[i].dropna())) * 100,2))
        plot_per_loss.append(round(((len(tot_trades[i][tot_trades[i] < 0]) / len(tot_trades[i].dropna()))) * 100,2))
        plot_tot_won.append(len(tot_trades[i][tot_trades[i] > 0]))
        plot_tot_loss.append(len(tot_trades[i][tot_trades[i] < 0]))
        plot_profit_brut.append(round(tot_trades[i][tot_trades[i] > 0].sum(),2))
        plot_loss_brut.append(round(tot_trades[i][tot_trades[i] < 0].sum(),2))
        plot_profit_mean.append(round(tot_trades[i][tot_trades[i] > 0].mean(),2))
        plot_loss_mean.append(round(tot_trades[i][tot_trades[i] < 0].mean(),2))
        plot_profit_median.append(round(tot_trades[i][tot_trades[i] > 0].median(),2))
        plot_loss_median.append(round(tot_trades[i][tot_trades[i] < 0].median(),2))
        plot_profit_std.append(round(tot_trades[i][tot_trades[i] > 0].std(),2))
        plot_loss_std.append(round(tot_trades[i][tot_trades[i] < 0].std(),2))
        sum = tot_trades[i].sum()
        if sum < 0:
            colors.append('firebrick')
        else:
            colors.append('darkgreen')

    x = np.arange(28)

        # Porcentagem Vitória/Derrota
    plt.bar(x-0.2,plot_per_loss,color='firebrick')
    plt.bar(x+0.2,plot_per_won,color='darkgreen')
    plt.grid()
    plt.xticks(x, tot_trades.columns)
    plt.xlabel("Pares",fontsize=20)
    plt.ylabel("Porcentagem",fontsize=20)
    plt.title("Porcentagem de Vitória/Derrotas",fontsize=30)
    plt.show()

        # Total Vitória e Derrota
    plt.bar(x-0.2,plot_tot_loss,color='firebrick')
    plt.bar(x+0.2,plot_tot_won,color='darkgreen')
    plt.grid()
    plt.xticks(x, tot_trades.columns)
    plt.xlabel("Pares",fontsize=20)
    plt.ylabel("Total",fontsize=20)
    plt.title("Total de Vitórias/Derrotas",fontsize=30)
    plt.show()

        # Lucro/Prejuízo Bruto
    plt.bar(tot_trades.columns,plot_profit_brut,color='darkgreen')
    plt.bar(tot_trades.columns,plot_loss_brut,color='firebrick')
    plt.grid()
    plt.xlabel("Pares",fontsize=20)
    plt.ylabel("Lucro/Prejuízo",fontsize=20)
    plt.title("Lucro/Prejuízo Bruto",fontsize=30)
    plt.show()

        # Média Lucro/Prejuízo
    plt.bar(tot_trades.columns,plot_profit_mean,color='darkgreen')
    plt.bar(tot_trades.columns,plot_loss_mean,color='firebrick')
    plt.grid()
    plt.xlabel("Pares",fontsize=20)
    plt.ylabel("Lucro/Prejuízo",fontsize=20)
    plt.title("Média Lucro/Prejuízo",fontsize=30)
    plt.show()

        # Mediana Lucro/Prejuízo
    plt.bar(tot_trades.columns,plot_profit_median,color='darkgreen')
    plt.bar(tot_trades.columns,plot_loss_median,color='firebrick')
    plt.grid()
    plt.xlabel("Pares",fontsize=20)
    plt.ylabel("Lucro/Prejuízo",fontsize=20)
    plt.title("Mediana Lucro/Prejuízo",fontsize=30)
    plt.show()

        # Desvio Padrão Lucro/Prejuízo
    plt.bar(x-0.2,plot_profit_std,color='darkgreen')
    plt.bar(x+0.2,plot_loss_std,color='firebrick')
    plt.grid()
    plt.xticks(x, tot_trades.columns)
    plt.xlabel("Pares",fontsize=20)
    plt.ylabel("Lucro/Prejuízo",fontsize=20)
    plt.title("Desvio Padrão Lucro/Prejuízo",fontsize=30)
    plt.show()

        # Lucro Liquido
    plt.bar(tot_trades.columns,tot_trades.sum(),color=colors)
    plt.grid()
    plt.xlabel("Pares",fontsize=20)
    plt.ylabel("Lucro Liquido",fontsize=20)
    plt.title("Lucros Liquido\ de Cada Par",fontsize=30)
    plt.show()

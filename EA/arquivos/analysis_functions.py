import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class Analysis:

    def analysis_backtest(self, df):
        period = len(self.get_normal_data())
        if period < 4000:
            print('Period data set D1')
            period /= 365
        elif period > 4000 and period < 24000:
            print('Period data set H4')
            period = period / 6 / 365
        elif l > 24000 and period < 96000:
            print('Period data set H1')
            period = period / 24 / 365

        self.period_data = period

        analy = pd.DataFrame()
        analy['Analises'] = np.nan
        analy[df.columns] = np.nan
        analy.set_index('Analises', inplace=True)
        analy = analy.T

        trades_total = self.count_trades(df)
        analy['Total_Trades'] = trades_total

        trades_year = self.count_trades_per_year(df)
        analy['Average_Trades_Per_Year'] = trades_year

        ar = self.annualized_return(df)
        analy['Annualized_Return_%'] = ar

        max_dd, max_equity = self.max_drawdown(df)
        analy['Max_DD_%'] = max_dd
        analy['Max_DD_€'] = max_equity

        win_percent = self.win_percent_rate(df)
        analy['Average_Win_Rate_%'] = win_percent

        max_pos, min_pos, max_neg, min_neg = self.max_min(df)
        analy['Largest_Win_€'] = max_pos
        analy['Smallest_Win_€'] = min_pos

        loss_percent = self.loss_percent_rate(df)
        analy['Average_Loss_Rate_%'] = loss_percent

        analy['Largest_Loss_€'] = max_neg
        analy['Smallest_Loss_€'] = min_neg

        return analy


    @staticmethod
    def max_drawdown(df):
        count = []
        equity = []
        for i in df.columns:
            array = 0
            if i == 'Total_Trades':
                array = df[i].dropna().to_numpy()
            elif i == 'Short_Trades' or i == 'Long_Trades':
                count.append(np.nan)
                equity.append(np.nan)
                continue
            else:
                array = np.append(1000, df[i].dropna().to_numpy()).cumsum()
            calc = ((np.maximum.accumulate(array) - array) / np.maximum.accumulate(array)).max() * 100 * -1
            equity_max = np.where(((np.maximum.accumulate(array) - array) / np.maximum.accumulate(array)) == ((np.maximum.accumulate(array) - array) / np.maximum.accumulate(array)).max())[0][0]
            equity.append(pd.Series(array).diff(equity_max)[equity_max])
            count.append(calc)

        return count, equity


    @staticmethod
    def loss_percent_rate(df):
        count = []
        for i in df.columns:
            if i == 'Total_Trades':
                count.append(df[i].diff()[df[i].diff() < 0].count() / df[i].count() * 100)
            else:
                count.append(df[i][df[i] < 0].count() / df[i].count() * 100)
        return count


    @staticmethod
    def win_percent_rate(df):
        count = []
        for i in df.columns:
            if i == 'Total_Trades':
                count.append(df[i].diff()[df[i].diff() > 0].count() / df[i].count() * 100)
            else:
                count.append(df[i][df[i] > 0].count() / df[i].count() * 100)
        return count


    @staticmethod
    def count_trades_per_year(df):
        count = []
        for i in df.columns:
            count.append(df[i].dropna().count() / 365)
        return count


    @staticmethod
    def count_trades(df):
        count = []
        for i in df.columns:
            count.append(df[i].dropna().count())
        return count


    def annualized_return(self, df):

        period = 1 / self.period_data

        ar = []

        for i in df.columns:
            if i == 'Total_Trades':
                ret = df['Total_Trades'].iloc[-1] / df['Total_Trades'].iloc[0]
                if ret < 0:
                    ret = abs(ret)
                    tot = (((ret ** period) - 1) * 100) * -1
                    ar.append(tot)
                else:
                    ar.append((((ret ** period) - 1) * 100))
            else:
                ret = df[i].sum() / df['Total_Trades'].iloc[0]
                if ret < 0:
                    ret = abs(ret)
                    tot = ((ret ** period) * 100) * -1
                    ar.append(tot)
                else:
                    ar.append(((ret ** period) * 100))

        return ar


    @staticmethod
    def max_min(df):
        max_positive, min_positive = [], []
        max_negative, min_negative = [], []
        for i in df.columns:
            if i == 'Total_Trades':
                max_positive.append(df[i].diff()[df[i].diff() > 0].max())
                min_positive.append(df[i].diff()[df[i].diff() > 0].min())
                max_negative.append(df[i].diff()[df[i].diff() < 0].max())
                min_negative.append(df[i].diff()[df[i].diff() < 0].min())
            else:
                max_positive.append(df[i][df[i] > 0].max())
                min_positive.append(df[i][df[i] > 0].min())
                max_negative.append(df[i][df[i] < 0].max())
                min_negative.append(df[i][df[i] < 0].min())
        return max_positive, min_positive, max_negative, min_negative


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

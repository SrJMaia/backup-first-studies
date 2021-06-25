    eurcad, euraud, eurnzd, eurgbp, eurjpy, eurchf, eurusd = [], [], [], [], [], [], []
    gbpnzd, gbpusd, gbpcad, gbpjpy, gbpchf, gbpaud = [], [], [], [], [], []
    usdcad, nzdusd, audusd, usdjpy, usdchf = [], [], [], [], []
    nzdjpy, chfjpy, cadjpy, audjpy = [], [], [], []
    nzdchf, cadchf, audchf = [], [], []
    nzdcad, audnzd = [], []
    audcad = []
"""
Analises Futuras - Livro

gain, loss = [], []
for i in test['EURUSD']:
    if i > 0:
        gain.append(i)
    else:
        loss.append(i)
gain = pd.Series(gain)
loss = pd.Series(loss)

X = 2 * len(gain) * len(loss)
N = len(test['EURUSD'])
R = 1
for i in range(1,len(test['EURUSD'])):
    if test['EURUSD'].iloc[i] > 0 and test['EURUSD'].iloc[i-1] < 0:
        R += 1
    elif test['EURUSD'].iloc[i] < 0 and test['EURUSD'].iloc[i-1] > 0:
        R += 1

(N * (R - 0.5) - X) / (math.sqrt((X*(X-N))/(N-1)))

# Quanto maior o nivel de confiança do Z Score, significa que ha muitas sequencias
# de trades ganhadores/perdedores seguidos
# Se positivo implica que vitorias geram derrotas, e vice versa. QUanto mais ganha, maior a probabildiade de perder
# SE for negativo, signfica que virtorias geram vitorias, e derrotas geram derrotas
# Cut para ter um nivel de confiança descente tem que ser no minimo 2 ou 95.45%

from scipy.stats import pearsonr
pearsonr(test['EURUSD'].iloc[1:],test['EURUSD'].shift().dropna())
# Caso haja uma grande dependencia fazer um walk forward test, para saber se toda a amostra
# de fato tem correlação ou apenas um periodo foi forte
# Uma correlação maior que 0.25 significa que grandes vitorias são seguidas por grandes derrotas
# Uma correlação menro que -0.25 significa que grandes derrotas sao seguidas por grandes vitórias

# Usar o expectancy para filtrar os trades e mvez do saldo maxximo?
(prob_win * amount_won) + (prob_loss * (amount_loss # A negative value))
# Se mairo que 0, o sistema e lucrativo, retorna um valor em centaavos 
"""

def ajusting_data(data):
    """
    Função usada para pegar o pct_change qunado importa um csv apenas dos preços
    """


    open_symbols = {
        'eur':['EURCHF_Open','EURGBP_Open','EURJPY_Open','EURNZD_Open','EURUSD_Open','EURAUD_Open','EURCAD_Open'],
        'gbp':['EURGBP_Open','GBPAUD_Open','GBPCHF_Open','GBPJPY_Open','GBPCAD_Open','GBPUSD_Open','GBPNZD_Open'],
        'usd':['GBPUSD_Open','USDCHF_Open','USDJPY_Open','AUDUSD_Open','NZDUSD_Open','USDCAD_Open','EURUSD_Open'],
        'jpy':['AUDJPY_Open','CADJPY_Open','CHFJPY_Open','EURJPY_Open','USDJPY_Open','GBPJPY_Open','NZDJPY_Open'],
        'chf':['AUDCHF_Open','CADCHF_Open','CHFJPY_Open','USDCHF_Open','EURCHF_Open','GBPCHF_Open','NZDCHF_Open'],
        'nzd':['AUDNZD_Open','EURNZD_Open','GBPNZD_Open','NZDUSD_Open','NZDCAD_Open','NZDCHF_Open','NZDJPY_Open'],
        'aud':['AUDCAD_Open','AUDCHF_Open','AUDJPY_Open','AUDUSD_Open','AUDNZD_Open','EURAUD_Open','GBPAUD_Open'],
        'cad':['AUDCAD_Open','CADCHF_Open','CADJPY_Open','USDCAD_Open','EURCAD_Open','GBPCAD_Open','NZDCAD_Open']
    }

    close_symbols = {
        'eur':['EURCHF_Close','EURGBP_Close','EURJPY_Close','EURNZD_Close','EURUSD_Close','EURAUD_Close','EURCAD_Close'],
        'gbp':['EURGBP_Close','GBPAUD_Close','GBPCHF_Close','GBPJPY_Close','GBPCAD_Close','GBPUSD_Close','GBPNZD_Close'],
        'usd':['GBPUSD_Close','USDCHF_Close','USDJPY_Close','AUDUSD_Close','NZDUSD_Close','USDCAD_Close','EURUSD_Close'],
        'jpy':['AUDJPY_Close','CADJPY_Close','CHFJPY_Close','EURJPY_Close','USDJPY_Close','GBPJPY_Close','NZDJPY_Close'],
        'chf':['AUDCHF_Close','CADCHF_Close','CHFJPY_Close','USDCHF_Close','EURCHF_Close','GBPCHF_Close','NZDCHF_Close'],
        'nzd':['AUDNZD_Close','EURNZD_Close','GBPNZD_Close','NZDUSD_Close','NZDCAD_Close','NZDCHF_Close','NZDJPY_Close'],
        'aud':['AUDCAD_Close','AUDCHF_Close','AUDJPY_Close','AUDUSD_Close','AUDNZD_Close','EURAUD_Close','GBPAUD_Close'],
        'cad':['AUDCAD_Close','CADCHF_Close','CADJPY_Close','USDCAD_Close','EURCAD_Close','GBPCAD_Close','NZDCAD_Close']
    }

    high_symbols = {
        'eur':['EURCHF_High','EURGBP_High','EURJPY_High','EURNZD_High','EURUSD_High','EURAUD_High','EURCAD_High'],
        'gbp':['EURGBP_High','GBPAUD_High','GBPCHF_High','GBPJPY_High','GBPCAD_High','GBPUSD_High','GBPNZD_High'],
        'usd':['GBPUSD_High','USDCHF_High','USDJPY_High','AUDUSD_High','NZDUSD_High','USDCAD_High','EURUSD_High'],
        'jpy':['AUDJPY_High','CADJPY_High','CHFJPY_High','EURJPY_High','USDJPY_High','GBPJPY_High','NZDJPY_High'],
        'chf':['AUDCHF_High','CADCHF_High','CHFJPY_High','USDCHF_High','EURCHF_High','GBPCHF_High','NZDCHF_High'],
        'nzd':['AUDNZD_High','EURNZD_High','GBPNZD_High','NZDUSD_High','NZDCAD_High','NZDCHF_High','NZDJPY_High'],
        'aud':['AUDCAD_High','AUDCHF_High','AUDJPY_High','AUDUSD_High','AUDNZD_High','EURAUD_High','GBPAUD_High'],
        'cad':['AUDCAD_High','CADCHF_High','CADJPY_High','USDCAD_High','EURCAD_High','GBPCAD_High','NZDCAD_High']
    }

    low_symbols = {
        'eur':['EURCHF_Low','EURGBP_Low','EURJPY_Low','EURNZD_Low','EURUSD_Low','EURAUD_Low','EURCAD_Low'],
        'gbp':['EURGBP_Low','GBPAUD_Low','GBPCHF_Low','GBPJPY_Low','GBPCAD_Low','GBPUSD_Low','GBPNZD_Low'],
        'usd':['GBPUSD_Low','USDCHF_Low','USDJPY_Low','AUDUSD_Low','NZDUSD_Low','USDCAD_Low','EURUSD_Low'],
        'jpy':['AUDJPY_Low','CADJPY_Low','CHFJPY_Low','EURJPY_Low','USDJPY_Low','GBPJPY_Low','NZDJPY_Low'],
        'chf':['AUDCHF_Low','CADCHF_Low','CHFJPY_Low','USDCHF_Low','EURCHF_Low','GBPCHF_Low','NZDCHF_Low'],
        'nzd':['AUDNZD_Low','EURNZD_Low','GBPNZD_Low','NZDUSD_Low','NZDCAD_Low','NZDCHF_Low','NZDJPY_Low'],
        'aud':['AUDCAD_Low','AUDCHF_Low','AUDJPY_Low','AUDUSD_Low','AUDNZD_Low','EURAUD_Low','GBPAUD_Low'],
        'cad':['AUDCAD_Low','CADCHF_Low','CADJPY_Low','USDCAD_Low','EURCAD_Low','GBPCAD_Low','NZDCAD_Low']
    }


    symbols = {
        'eur':['EURCHF_High','EURGBP_High','EURJPY_High','EURNZD_High','EURUSD_High','EURAUD_High','EURCAD_High','EURCHF_Open','EURGBP_Open','EURJPY_Open','EURNZD_Open','EURUSD_Open','EURAUD_Open','EURCAD_Open','EURCHF_Low','EURGBP_Low','EURJPY_Low','EURNZD_Low','EURUSD_Low','EURAUD_Low','EURCAD_Low','EURCHF_Close','EURGBP_Close','EURJPY_Close','EURNZD_Close','EURUSD_Close','EURAUD_Close','EURCAD_Close'],
        'gbp':['EURGBP_High','GBPAUD_High','GBPCHF_High','GBPJPY_High','GBPCAD_High','GBPUSD_High','GBPNZD_High','EURGBP_Open','GBPAUD_Open','GBPCHF_Open','GBPJPY_Open','GBPCAD_Open','GBPUSD_Open','GBPNZD_Open','EURGBP_Low','GBPAUD_Low','GBPCHF_Low','GBPJPY_Low','GBPCAD_Low','GBPUSD_Low','GBPNZD_Low','EURGBP_Close','GBPAUD_Close','GBPCHF_Close','GBPJPY_Close','GBPCAD_Close','GBPUSD_Close','GBPNZD_Close'],
        'usd':['GBPUSD_High','USDCHF_High','USDJPY_High','AUDUSD_High','NZDUSD_High','USDCAD_High','EURUSD_High','GBPUSD_Open','USDCHF_Open','USDJPY_Open','AUDUSD_Open','NZDUSD_Open','USDCAD_Open','EURUSD_Open','GBPUSD_Low','USDCHF_Low','USDJPY_Low','AUDUSD_Low','NZDUSD_Low','USDCAD_Low','EURUSD_Low','GBPUSD_Close','USDCHF_Close','USDJPY_Close','AUDUSD_Close','NZDUSD_Close','USDCAD_Close','EURUSD_Close'],
        'jpy':['AUDJPY_High','CADJPY_High','CHFJPY_High','EURJPY_High','USDJPY_High','GBPJPY_High','NZDJPY_High','AUDJPY_Open','CADJPY_Open','CHFJPY_Open','EURJPY_Open','USDJPY_Open','GBPJPY_Open','NZDJPY_Open','AUDJPY_Low','CADJPY_Low','CHFJPY_Low','EURJPY_Low','USDJPY_Low','GBPJPY_Low','NZDJPY_Low','AUDJPY_Close','CADJPY_Close','CHFJPY_Close','EURJPY_Close','USDJPY_Close','GBPJPY_Close','NZDJPY_Close'],
        'chf':['AUDCHF_High','CADCHF_High','CHFJPY_High','USDCHF_High','EURCHF_High','GBPCHF_High','NZDCHF_High','AUDCHF_Open','CADCHF_Open','CHFJPY_Open','USDCHF_Open','EURCHF_Open','GBPCHF_Open','NZDCHF_Open','AUDCHF_Low','CADCHF_Low','CHFJPY_Low','USDCHF_Low','EURCHF_Low','GBPCHF_Low','NZDCHF_Low','AUDCHF_Close','CADCHF_Close','CHFJPY_Close','USDCHF_Close','EURCHF_Close','GBPCHF_Close','NZDCHF_Close'],
        'nzd':['AUDNZD_High','EURNZD_High','GBPNZD_High','NZDUSD_High','NZDCAD_High','NZDCHF_High','NZDJPY_High','AUDNZD_Open','EURNZD_Open','GBPNZD_Open','NZDUSD_Open','NZDCAD_Open','NZDCHF_Open','NZDJPY_Open','AUDNZD_Low','EURNZD_Low','GBPNZD_Low','NZDUSD_Low','NZDCAD_Low','NZDCHF_Low','NZDJPY_Low','AUDNZD_Close','EURNZD_Close','GBPNZD_Close','NZDUSD_Close','NZDCAD_Close','NZDCHF_Close','NZDJPY_Close'],
        'aud':['AUDCAD_High','AUDCHF_High','AUDJPY_High','AUDUSD_High','AUDNZD_High','EURAUD_High','GBPAUD_High','AUDCAD_Open','AUDCHF_Open','AUDJPY_Open','AUDUSD_Open','AUDNZD_Open','EURAUD_Open','GBPAUD_Open','AUDCAD_Low','AUDCHF_Low','AUDJPY_Low','AUDUSD_Low','AUDNZD_Low','EURAUD_Low','GBPAUD_Low','AUDCAD_Close','AUDCHF_Close','AUDJPY_Close','AUDUSD_Close','AUDNZD_Close','EURAUD_Close','GBPAUD_Close'],
        'cad':['AUDCAD_High','CADCHF_High','CADJPY_High','USDCAD_High','EURCAD_High','GBPCAD_High','NZDCAD_High','AUDCAD_Open','CADCHF_Open','CADJPY_Open','USDCAD_Open','EURCAD_Open','GBPCAD_Open','NZDCAD_Open','AUDCAD_Low','CADCHF_Low','CADJPY_Low','USDCAD_Low','EURCAD_Low','GBPCAD_Low','NZDCAD_Low','AUDCAD_Close','CADCHF_Close','CADJPY_Close','USDCAD_Close','EURCAD_Close','GBPCAD_Close','NZDCAD_Close']
    }


    for i,j in enumerate(open_symbols):
        data[f'{str(j)}_open'] = data[open_symbols[j]].pct_change().sum(axis=1)*100
    for i,j in enumerate(close_symbols):
        data[f'{str(j)}_close'] = data[close_symbols[j]].pct_change().sum(axis=1)*100
    for i,j in enumerate(high_symbols):
        data[f'{str(j)}_high'] = data[high_symbols[j]].pct_change().sum(axis=1)*100
    for i,j in enumerate(low_symbols):
        data[f'{str(j)}_low'] = data[low_symbols[j]].pct_change().sum(axis=1)*100
    for i,j in enumerate(symbols):
        data[f'{str(j)}'] = data[symbols[j]].pct_change().sum(axis=1)*100

    return data


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


"""
Regressão linear com o cut pre definido em 0.95
"""
bests_results_lr = []
best_equity_lr = 1000
flag_new_high = True
for i in single_final_test.columns:
    lr_test = pd.DataFrame()
    lr_test['x'] = pd.Series(range(len(single_final_test[i].dropna())))
    lr_test['y'] = single_final_test[i].dropna()
    x_v = lr_test[['x']]
    y_v = lr_test[['y']]
    model = LinearRegression()
    model.fit(x_v, y_v)
    result = model.score(x_v, y_v)
    equity = single_final_test[i].dropna().iloc[-1]
    if result > 0.95:
        if flag_new_high:
            bests_results_lr.append(i)
            best_equity_lr = equity
            flag_new_high = False
        elif flag_new_high == False and equity > best_equity_lr:
            bests_results_lr.append(i)
            best_equity_lr = equity
single_final_test[bests_results_lr].plot()
plt.grid()

def future(balance, saldo_inicial, saldo_final, iteration=1, risk=0.01, eur='', preco_eur=0, compra=False, jpy=''):

    balance_calc = balance

    leverage = 10

    if balance < 1000:
        balance_calc = 1000

    if eur == 'eur':
        if jpy == 'jpy':
            calc = (balance_calc * risk) / (0.01 / saldo_final * 100_000)
            if calc > 99.99:
                calc = 99.99
            elif calc > (x := balance * leverage / 100_000):
                calc = x
            lot = (calc / iteration * 1_000)
            comission = (lot//1000) * 0.1
            c1 = (saldo_inicial - saldo_final) * lot
            c2 = round(c1 - comission,2)
            return (c2 + balance), c2
        else:
            calc = (balance_calc * risk) / (0.0001 / saldo_final * 100_000)
            if calc > 99.99:
                calc = 99.99
            elif calc > (x := balance * leverage / 100_000):
                calc = x
            lot = (calc / iteration * 100_000)
            comission = (lot//1000) * 0.1
            c1 = (saldo_inicial - saldo_final) * lot
            c2 = round(c1 - comission,2)
            return (c2 + balance), c1
    else:
        if jpy == 'jpy':
            calc = (balance_calc * risk) / (0.01 / saldo_final * 100_000)
            if calc > 99.99:
                calc = 99.99
            elif calc > (x := balance * leverage / 100_000):
                calc = x
            lot = (calc / iteration * 100_000)
            comission = (lot//1000) * 0.1
            c1 = (saldo_inicial - saldo_final) * lot
            c2 = round(c1 / preco_eur - comission,2)
            return (c2 + balance), c2
        else:
            calc = (balance_calc * risk) / (0.0001 / saldo_final * 100_000)
            if calc > 99.99:
                calc = 99.99
            elif calc > (x := balance * leverage / 100_000):
                calc = x
            lot = (calc / iteration * 100_000)
            comission = (lot//1000) * 0.1
            c1 = (saldo_inicial - saldo_final) * lot
            c2 = round(c1 / preco_eur - comission,2)
            return (c2 + balance), c2

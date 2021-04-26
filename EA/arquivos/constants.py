class Pairs:

    ALL_PAIRS_OPEN = ('EURCHF_Open','EURGBP_Open','EURJPY_Open','EURNZD_Open','EURUSD_Open','EURAUD_Open','EURCAD_Open',
                      'GBPAUD_Open','GBPCHF_Open','GBPJPY_Open','GBPCAD_Open','GBPUSD_Open','GBPNZD_Open','USDCHF_Open',
                      'USDJPY_Open','AUDUSD_Open','NZDUSD_Open','USDCAD_Open','AUDJPY_Open','CADJPY_Open','CHFJPY_Open',
                      'NZDJPY_Open','AUDCHF_Open','CADCHF_Open','NZDCHF_Open','AUDNZD_Open','NZDCAD_Open','AUDCAD_Open')

    ALL_PAIRS_CLOSE = ('EURCHF_Close','EURGBP_Close','EURJPY_Close','EURNZD_Close','EURUSD_Close','EURAUD_Close','EURCAD_Close',
                      'GBPAUD_Close','GBPCHF_Close','GBPJPY_Close','GBPCAD_Close','GBPUSD_Close','GBPNZD_Close','USDCHF_Close',
                      'USDJPY_Close','AUDUSD_Close','NZDUSD_Close','USDCAD_Close','AUDJPY_Close','CADJPY_Close','CHFJPY_Close',
                      'NZDJPY_Close','AUDCHF_Close','CADCHF_Close','NZDCHF_Close','AUDNZD_Close','NZDCAD_Close','AUDCAD_Close')

    ALL_PAIRS_HIGH = ('EURCHF_High','EURGBP_High','EURJPY_High','EURNZD_High','EURUSD_High','EURAUD_High','EURCAD_High',
                      'GBPAUD_High','GBPCHF_High','GBPJPY_High','GBPCAD_High','GBPUSD_High','GBPNZD_High','USDCHF_High',
                      'USDJPY_High','AUDUSD_High','NZDUSD_High','USDCAD_High','AUDJPY_High','CADJPY_High','CHFJPY_High',
                      'NZDJPY_High','AUDCHF_High','CADCHF_High','NZDCHF_High','AUDNZD_High','NZDCAD_High','AUDCAD_High')

    ALL_PAIRS_LOW = ('EURCHF_Low','EURGBP_Low','EURJPY_Low','EURNZD_Low','EURUSD_Low','EURAUD_Low','EURCAD_Low',
                      'GBPAUD_Low','GBPCHF_Low','GBPJPY_Low','GBPCAD_Low','GBPUSD_Low','GBPNZD_Low','USDCHF_Low',
                      'USDJPY_Low','AUDUSD_Low','NZDUSD_Low','USDCAD_Low','AUDJPY_Low','CADJPY_Low','CHFJPY_Low',
                      'NZDJPY_Low','AUDCHF_Low','CADCHF_Low','NZDCHF_Low','AUDNZD_Low','NZDCAD_Low','AUDCAD_Low')


    ALL_PAIRS = ('EURCHF','EURGBP','EURJPY','EURNZD','EURUSD','EURAUD','EURCAD',
                 'GBPAUD','GBPCHF','GBPJPY','GBPCAD','GBPUSD','GBPNZD','USDCHF',
                 'USDJPY','AUDUSD','NZDUSD','USDCAD','AUDJPY','CADJPY','CHFJPY',
                 'NZDJPY','AUDCHF','CADCHF','NZDCHF','AUDNZD','NZDCAD','AUDCAD')

    ALL_PAIRS_TPSL = ('EURCHF_TPSL','EURGBP_TPSL','EURJPY_TPSL','EURNZD_TPSL','EURUSD_TPSL','EURAUD_TPSL','EURCAD_TPSL',
                     'GBPAUD_TPSL','GBPCHF_TPSL','GBPJPY_TPSL','GBPCAD_TPSL','GBPUSD_TPSL','GBPNZD_TPSL','USDCHF_TPSL',
                     'USDJPY_TPSL','AUDUSD_TPSL','NZDUSD_TPSL','USDCAD_TPSL','AUDJPY_TPSL','CADJPY_TPSL','CHFJPY_TPSL',
                     'NZDJPY_TPSL','AUDCHF_TPSL','CADCHF_TPSL','NZDCHF_TPSL','AUDNZD_TPSL','NZDCAD_TPSL','AUDCAD_TPSL')

    ALL_PAIRS_FOR_DF = ['EURCHF','EURGBP','EURJPY','EURNZD','EURUSD','EURAUD','EURCAD',
                        'GBPAUD','GBPCHF','GBPJPY','GBPCAD','GBPUSD','GBPNZD','USDCHF',
                        'USDJPY','AUDUSD','NZDUSD','USDCAD','AUDJPY','CADJPY','CHFJPY',
                        'NZDJPY','AUDCHF','CADCHF','NZDCHF','AUDNZD','NZDCAD','AUDCAD']

    ALL_PAIRS_BUY = (
        'EURCHF_buy','EURGBP_buy','EURJPY_buy','EURNZD_buy','EURUSD_buy','EURAUD_buy','EURCAD_buy',
        'GBPAUD_buy','GBPCHF_buy','GBPJPY_buy','GBPCAD_buy','GBPUSD_buy','GBPNZD_buy','USDCHF_buy',
        'USDJPY_buy','AUDUSD_buy','NZDUSD_buy','USDCAD_buy','AUDJPY_buy','CADJPY_buy','CHFJPY_buy',
        'NZDJPY_buy','AUDCHF_buy','CADCHF_buy','NZDCHF_buy','AUDNZD_buy','NZDCAD_buy','AUDCAD_buy'
    )

    ALL_PAIRS_SELL = (
        'EURCHF_sell','EURGBP_sell','EURJPY_sell','EURNZD_sell','EURUSD_sell','EURAUD_sell','EURCAD_sell',
        'GBPAUD_sell','GBPCHF_sell','GBPJPY_sell','GBPCAD_sell','GBPUSD_sell','GBPNZD_sell','USDCHF_sell',
        'USDJPY_sell','AUDUSD_sell','NZDUSD_sell','USDCAD_sell','AUDJPY_sell','CADJPY_sell','CHFJPY_sell',
        'NZDJPY_sell','AUDCHF_sell','CADCHF_sell','NZDCHF_sell','AUDNZD_sell','NZDCAD_sell','AUDCAD_sell'
    )

    DIFF_SYMBOLS = (
        ('eur',('EURCHF','EURGBP','EURJPY','EURNZD','EURUSD','EURAUD','EURCAD')),
        ('gbp',('EURGBP','GBPAUD','GBPCHF','GBPJPY','GBPCAD','GBPUSD','GBPNZD')),
        ('usd',('GBPUSD','USDCHF','USDJPY','AUDUSD','NZDUSD','USDCAD','EURUSD')),
        ('jpy',('AUDJPY','CADJPY','CHFJPY','EURJPY','USDJPY','GBPJPY','NZDJPY')),
        ('chf',('AUDCHF','CADCHF','CHFJPY','USDCHF','EURCHF','GBPCHF','NZDCHF')),
        ('nzd',('AUDNZD','EURNZD','GBPNZD','NZDUSD','NZDCAD','NZDCHF','NZDJPY')),
        ('aud',('AUDCAD','AUDCHF','AUDJPY','AUDUSD','AUDNZD','EURAUD','GBPAUD')),
        ('cad',('AUDCAD','CADCHF','CADJPY','USDCAD','EURCAD','GBPCAD','NZDCAD'))
    )

    SPLIT_PAIRS = (
        ('eur','chf'),('eur','gbp'),('eur','jpy'),('eur','nzd'),('eur','usd'),
        ('eur','aud'),('eur','cad'),('gbp','aud'),('gbp','chf'),('gbp','jpy'),
        ('gbp','cad'),('gbp','usd'),('gbp','nzd'),('usd','chf'),('usd','jpy'),
        ('aud','usd'),('nzd','usd'),('usd','cad'),('aud','jpy'),('cad','jpy'),
        ('chf','jpy'),('nzd','jpy'),('aud','chf'),('cad','chf'),('nzd','chf'),
        ('aud','nzd'),('nzd','cad'),('aud','cad')
    )

    SIGNAL_LIST = (
        ('eur_signal','chf_signal'),('eur_signal','gbp_signal'),('eur_signal','jpy_signal'),('eur_signal','nzd_signal'),('eur_signal','usd_signal'),
        ('eur_signal','aud_signal'),('eur_signal','cad_signal'),('gbp_signal','aud_signal'),('gbp_signal','chf_signal'),('gbp_signal','jpy_signal'),
        ('gbp_signal','cad_signal'),('gbp_signal','usd_signal'),('gbp_signal','nzd_signal'),('usd_signal','chf_signal'),('usd_signal','jpy_signal'),
        ('aud_signal','usd_signal'),('nzd_signal','usd_signal'),('usd_signal','cad_signal'),('aud_signal','jpy_signal'),('cad_signal','jpy_signal'),
        ('chf_signal','jpy_signal'),('nzd_signal','jpy_signal'),('aud_signal','chf_signal'),('cad_signal','chf_signal'),('nzd_signal','chf_signal'),
        ('aud_signal','nzd_signal'),('nzd_signal','cad_signal'),('aud_signal','cad_signal')
    )

    MY_EVENTS = {
    'EURUSD':{'buy':False,'sell':False,'sell_request':0,'buy_request':0,'symbol':'EURUSD','buy_strategy':'EURUSD_buy','sell_strategy':'EURUSD_sell'},
    'EURCHF':{'buy':False,'sell':False,'sell_request':0,'buy_request':0,'symbol':'EURCHF','buy_strategy':'EURCHF_buy','sell_strategy':'EURCHF_sell'},
    'EURGBP':{'buy':False,'sell':False,'sell_request':0,'buy_request':0,'symbol':'EURGBP','buy_strategy':'EURGBP_buy','sell_strategy':'EURGBP_sell'},
    'EURJPY':{'buy':False,'sell':False,'sell_request':0,'buy_request':0,'symbol':'EURJPY','buy_strategy':'EURJPY_buy','sell_strategy':'EURJPY_sell'},
    'EURNZD':{'buy':False,'sell':False,'sell_request':0,'buy_request':0,'symbol':'EURNZD','buy_strategy':'EURNZD_buy','sell_strategy':'EURNZD_sell'},
    'EURAUD':{'buy':False,'sell':False,'sell_request':0,'buy_request':0,'symbol':'EURAUD','buy_strategy':'EURAUD_buy','sell_strategy':'EURAUD_sell'},
    'EURCAD':{'buy':False,'sell':False,'sell_request':0,'buy_request':0,'symbol':'EURCAD','buy_strategy':'EURCAD_buy','sell_strategy':'EURCAD_sell'},

    'GBPAUD':{'buy':False,'sell':False,'sell_request':0,'buy_request':0,'symbol':'GBPAUD','buy_strategy':'GBPAUD_buy','sell_strategy':'GBPAUD_sell'},
    'GBPCHF':{'buy':False,'sell':False,'sell_request':0,'buy_request':0,'symbol':'GBPCHF','buy_strategy':'GBPCHF_buy','sell_strategy':'GBPCHF_sell'},
    'GBPJPY':{'buy':False,'sell':False,'sell_request':0,'buy_request':0,'symbol':'GBPJPY','buy_strategy':'GBPJPY_buy','sell_strategy':'GBPJPY_sell'},
    'GBPCAD':{'buy':False,'sell':False,'sell_request':0,'buy_request':0,'symbol':'GBPCAD','buy_strategy':'GBPCAD_buy','sell_strategy':'GBPCAD_sell'},
    'GBPUSD':{'buy':False,'sell':False,'sell_request':0,'buy_request':0,'symbol':'GBPUSD','buy_strategy':'GBPUSD_buy','sell_strategy':'GBPUSD_sell'},
    'GBPNZD':{'buy':False,'sell':False,'sell_request':0,'buy_request':0,'symbol':'GBPNZD','buy_strategy':'GBPNZD_buy','sell_strategy':'GBPNZD_sell'},

    'USDCHF':{'buy':False,'sell':False,'sell_request':0,'buy_request':0,'symbol':'USDCHF','buy_strategy':'USDCHF_buy','sell_strategy':'USDCHF_sell'},
    'USDJPY':{'buy':False,'sell':False,'sell_request':0,'buy_request':0,'symbol':'USDJPY','buy_strategy':'USDJPY_buy','sell_strategy':'USDJPY_sell'},
    'AUDUSD':{'buy':False,'sell':False,'sell_request':0,'buy_request':0,'symbol':'AUDUSD','buy_strategy':'AUDUSD_buy','sell_strategy':'AUDUSD_sell'},
    'NZDUSD':{'buy':False,'sell':False,'sell_request':0,'buy_request':0,'symbol':'NZDUSD','buy_strategy':'NZDUSD_buy','sell_strategy':'NZDUSD_sell'},
    'USDCAD':{'buy':False,'sell':False,'sell_request':0,'buy_request':0,'symbol':'USDCAD','buy_strategy':'USDCAD_buy','sell_strategy':'USDCAD_sell'},

    'AUDJPY':{'buy':False,'sell':False,'sell_request':0,'buy_request':0,'symbol':'AUDJPY','buy_strategy':'AUDJPY_buy','sell_strategy':'AUDJPY_sell'},
    'CADJPY':{'buy':False,'sell':False,'sell_request':0,'buy_request':0,'symbol':'CADJPY','buy_strategy':'CADJPY_buy','sell_strategy':'CADJPY_sell'},
    'CHFJPY':{'buy':False,'sell':False,'sell_request':0,'buy_request':0,'symbol':'CHFJPY','buy_strategy':'CHFJPY_buy','sell_strategy':'CHFJPY_sell'},
    'NZDJPY':{'buy':False,'sell':False,'sell_request':0,'buy_request':0,'symbol':'NZDJPY','buy_strategy':'NZDJPY_buy','sell_strategy':'NZDJPY_sell'},

    'AUDCHF':{'buy':False,'sell':False,'sell_request':0,'buy_request':0,'symbol':'AUDCHF','buy_strategy':'AUDCHF_buy','sell_strategy':'AUDCHF_sell'},
    'CADCHF':{'buy':False,'sell':False,'sell_request':0,'buy_request':0,'symbol':'CADCHF','buy_strategy':'CADCHF_buy','sell_strategy':'CADCHF_sell'},
    'NZDCHF':{'buy':False,'sell':False,'sell_request':0,'buy_request':0,'symbol':'NZDCHF','buy_strategy':'NZDCHF_buy','sell_strategy':'NZDCHF_sell'},

    'AUDNZD':{'buy':False,'sell':False,'sell_request':0,'buy_request':0,'symbol':'AUDNZD','buy_strategy':'AUDNZD_buy','sell_strategy':'AUDNZD_sell'},
    'NZDCAD':{'buy':False,'sell':False,'sell_request':0,'buy_request':0,'symbol':'NZDCAD','buy_strategy':'NZDCAD_buy','sell_strategy':'NZDCAD_sell'},

    'AUDCAD':{'buy':False,'sell':False,'sell_request':0,'buy_request':0,'symbol':'AUDCAD','buy_strategy':'AUDCAD_buy','sell_strategy':'AUDCAD_sell'}
    }

    JPY = ('EURJPY','USDJPY','GBPJPY','AUDJPY','CHFJPY','NZDJPY','CADJPY')

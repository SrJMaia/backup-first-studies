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

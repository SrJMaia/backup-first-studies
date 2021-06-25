from arquivos.expert import eaonline

ea = eaonline(risk=0.01, multiply=3, magic_number=1005, timeframe='D1', tpsl_avg = 10, tp_multi=4.0, sl_multi=0.5, pct_period=7)

ea.start()

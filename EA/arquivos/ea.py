from arquivos.expert import eaonline

ea = eaonline(risk=0.01, multiply=3, magic_number=1005, timeframe='D1', tpsl = 100, pct_period=7)

ea.start()

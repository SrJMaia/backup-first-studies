from PySimpleGUI import PySimpleGUI as sg

def my_layout():
    layout = [
        [sg.Text("",font=['Arial',15],size=(25,1),auto_size_text=True,key='-MARGIN_FREE0-',justification='c',background_color='grey80'),
         sg.Text("",font=['Arial',15],size=(25,1),auto_size_text=True,key='-BALANCE0-',justification='c',background_color='grey80'),
         sg.Text("",font=['Arial',15],size=(25,1),auto_size_text=True,key='-PROFIT0-',justification='c',background_color='grey80')],
        [sg.Text("")],
        [sg.Text("",size=(25,1),key='-EUR0-',justification='l')],
        [sg.Text("",size=(25,1),key='-USD0-',justification='l')],
        [sg.Text("",size=(25,1),key='-GBP0-',justification='l')],
        [sg.Text("",size=(25,1),key='-JPY0-',justification='l')],
        [sg.Text("",size=(25,1),key='-CHF0-',justification='l')],
        [sg.Text("",size=(25,1),key='-NZD0-',justification='l')],
        [sg.Text("",size=(25,1),key='-AUD0-',justification='l')],
        [sg.Text("",size=(25,1),key='-CAD0-',justification='l')],
        [sg.Text("")],
        [sg.Text("",size=(12,1),key='-CONEXITION0-',justification='r'),
         sg.Text("",size=(13,1),key='-PING0-',justification='r')],
    ]

    return layout


def update_screen(window,data,balance,profit,margin_free,conexao,ping):
    window['-MARGIN_FREE0-'].update(f"Margin Free: {margin_free}€")
    window['-BALANCE0-'].update(f"Balance: {balance}€")
    window['-PROFIT0-'].update(f"Profit: {profit}€",text_color=['red' if profit<0 else 'green'])
    window['-EUR0-'].update(f"EUR - C0: {data['eur'].iloc[-1]} | C-1: {data['eur'].iloc[-2]}")
    window['-USD0-'].update(f"USD - C0: {data['usd'].iloc[-1]} | C-1: {data['usd'].iloc[-2]}")
    window['-GBP0-'].update(f"GBP - C0: {data['gbp'].iloc[-1]} | C-1: {data['gbp'].iloc[-2]}")
    window['-JPY0-'].update(f"JPY - C0: {data['jpy'].iloc[-1]} | C-1: {data['jpy'].iloc[-2]}")
    window['-CHF0-'].update(f"CHF - C0: {data['chf'].iloc[-1]} | C-1: {data['chf'].iloc[-2]}")
    window['-NZD0-'].update(f"NZD - C0: {data['nzd'].iloc[-1]} | C-1: {data['nzd'].iloc[-2]}")
    window['-AUD0-'].update(f"AUD - C0: {data['aud'].iloc[-1]} | C-1: {data['aud'].iloc[-2]}")
    window['-CAD0-'].update(f"CAD - C0: {data['cad'].iloc[-1]} | C-1: {data['cad'].iloc[-2]}")
    window['-CONEXITION0-'].update(f"Conexão: {'ON' if conexao else 'OFF'}",text_color=['green' if conexao else 'red'])
    window['-PING0-'].update(f"Ping: {round(ping/1000,2)}ms",text_color='green' if ping<round(ping/1000,2) else 'goldenrod')

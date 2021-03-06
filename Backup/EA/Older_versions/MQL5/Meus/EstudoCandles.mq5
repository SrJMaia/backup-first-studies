//+------------------------------------------------------------------+
//|                                                EstudoCandles.mq5 |
//|                        Copyright 2020, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2020, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
//---

// Não é preciso especificar a quantidade nesse array - Caso haja duvida aperte F1 em cima de MqlRates
MqlRates velas[];

// Ira mostrar os dados do ultimo candle, o que esta no moento
MqlTick tick;





//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- create timer
   EventSetTimer(5);
   
// Vai copiar os dados da vela
// 1.Paridade 2.Periodo Grafico 3. Candle da coleta de dados 4.Total de Dados 5. Array de velas
// A vela 0 é a vela que esta sendo formada, ou seja, a ultima
   CopyRates(_Symbol,_Period,0,3,velas);
// Caso nao seja declarado a frase abaixo, o ultimo candle nao sera o numero 0 e sim o contrario
   ArraySetAsSeries(velas,true);
   
   
//---
   
   SymbolInfoTick(_Symbol,tick);
   
   
   
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//--- destroy timer
   EventKillTimer();
   
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//---
   

   
  }
//+------------------------------------------------------------------+
//| Timer function                                                   |
//+------------------------------------------------------------------+
void OnTimer()
  {
//---
   
//   Vai imprimir os valores especificado da ultiam vela, dependendo da vela que queira devera mudar o numero

   int ind = 0;
   
//   Print("Preço Abertura = ", velas[ind].open);
//   Print("Preço Fechamento = ", velas[ind].close);
//   Print("Preço Max = ", velas[ind].high);
//   Print("Preço Min = ", velas[ind].low);
//   
//   Print("----------------------------------------");
//   
//   Print("Last = ", tick.last);
//   Print("Tempo = ", tick.time);
//   Print("Volume = ", tick.volume);
//   
//   Print("----------------------------------------");
   
// "\n"+ faz pular uma linha
// DoubleToString faz o que o nome diz, transforma um numero em letra
// Provavelmente ICMarket nao fala o volume ou o ultimo preço
// Comment mostra comentario na tela

   string leg_tela = "Preço Abertura = "+ DoubleToString(velas[ind].open)+"\n"+
                     "Preço Fechamento = "+ DoubleToString(velas[ind].close)+"\n"+
                     "Preço Max = "+ DoubleToString(velas[ind].high)+"\n"+
                     "Preço Min = "+ DoubleToString(velas[ind].low)+"\n\n"+
                     "Tempo = "+tick.time+"\n"+
                     "Volume = "+DoubleToString(tick.volume_real);
   
   Comment(leg_tela);
   
// A diferença de comment para alert e que alerta mostra uma caixa de alerta e tambemm mostra na barra de ferramenta em expert
   
   Alert(leg_tela);
   
   Print("----------------------------------------");
   
   
  }
//+------------------------------------------------------------------+

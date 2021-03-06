//+------------------------------------------------------------------+
//|                                                                  |
//|                                                    MonstroV5.mq5 |
//|                                                                  |
//+------------------------------------------------------------------+
#property copyright "Your Holding"
#property version   "5.0"
//---
#include <Trade\Trade.mqh>
//#include <Modulos_EA.mqh>
#include <expert/expertbase.mqh>
#include <indicators/indicators.mqh>
#include <Trade\PositionInfo.mqh>
#include <Trade\SymbolInfo.mqh>
//---
enum LIGA
  {
   SIM,        // Sim
   NAO         // Não
  };

input LIGA liga_breakeven                  = NAO;                  // Liga BreakEven
input LIGA liga_sl_movel                   = SIM;                  // Liga SL Movel
//---
input group "-----Gerenciamento-----"
//input double num_lots                    = 0.01;               // Número de Lotes
input double TKCompra                      = 3000;                 // Take Profit
input double SLCompra                      = 1300;                 // Stop Loss
input double TKVenda                       = 1200;                 // Take Profit
input double SLVenda                       = 1100;                 // Stop Loss
input double risco                         = 3;                    // Capital a Ser Arriscado por Operação
input double alavancagem                   = 500;                  // Alavancagem da Conta
//---
input group "-----Horários-----"
input string hora_limite_fecha_op         = "22:00";               // Horário Limite para Fechar Operação
//---
//+------------------------------------------------------------------+
//|  Variáveis para os indicadores                                   |
//+------------------------------------------------------------------+

int eur_Handle;
double obs_eur_Buffer[];

//+------------------------------------------------------------------+
//| Variáveis para as funçoes                                        |
//+------------------------------------------------------------------+

MqlRates velas[];            // Variável para armazenar velas
MqlTick tick;                // Variável para armazenar ticks
MqlRates rates[];            // Variavel para armazenar preços

CTrade trade;
CPositionInfo pos;

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//--

   eur_Handle = iCustom(_Symbol,PERIOD_CURRENT,"Indicatorstesteoverbs.ex5",20);
   if(eur_Handle == INVALID_HANDLE)
      return INIT_FAILED;

   CopyRates(_Symbol,_Period,0,4,velas);
   ArraySetAsSeries(velas,true);

   ArraySetAsSeries(rates,true);

// Para adicionar no gráfico o indicador:

//---


   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//---
   IndicatorRelease(eur_Handle);

  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+

bool be_ativado = false;
bool PositionClosePartial = true;

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void OnTick()
  {
//---

   if(CopyRates(_Symbol, _Period, 0, 3, rates)<0)
     {
      Alert("Erro ao obter as informações de MqlRates: ", GetLastError());
      return;
     }
   ArraySetAsSeries(velas,true);

   CopyBuffer(eur_Handle,0,0,4,obs_eur_Buffer);

   CopyRates(_Symbol,_Period,0,4,velas);

   ArraySetAsSeries(obs_eur_Buffer,true);
   Comment(obs_eur_Buffer[3]);
//---
   

// Alimentar com dados variável de tick
   SymbolInfoTick(_Symbol,tick);

// LOGICA PARA ATIVAR COMPRA

   bool Comprar = false; // Pode comprar?
   bool Vender  = false; // Pode vender?

   Comprar = false;
   Vender = false;

//---

   double lotePadrao;
   double porcentagem = risco/100;
   double calcTeste = (((AccountInfoDouble(ACCOUNT_BALANCE)*porcentagem)*alavancagem)/100000)/SymbolInfoDouble(_Symbol,SYMBOL_BID);;
   if(calcTeste < 0.01)
     {
      lotePadrao = 0.01;
     }
   else
      if(calcTeste > 99.99)
        {
         lotePadrao = 99.99;
        }
      else
        {
         lotePadrao = (DoubleToString(calcTeste,2));
        }


//---


// retorna true se tivermos uma nova vela
   bool temosNovaVela = TemosNovaVela();

// Toda vez que existir uma nova vela entrar nesse 'if'
   if(temosNovaVela)
     {
      
      // Condição de Compra:
      if(Comprar && PositionSelect(_Symbol)==false)
        {
         desenhaLinhaVertical("Compra",velas[1].time,clrBlue);
         CompraAMercado2(lotePadrao,tick.ask);
         be_ativado = false;
        }
      if(Comprar && PositionSelect(_Symbol) == true && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_SELL)
        {
         desenhaLinhaVertical("Compra",velas[1].time,clrBlue);
         FecharPosicao();
         CompraAMercado2(lotePadrao,tick.ask);
         be_ativado = false;
        }
      // Condição de Venda:
      if(Vender && PositionSelect(_Symbol)==false)
        {
         desenhaLinhaVertical("Venda",velas[1].time,clrRed);
         VendaAMercado2(lotePadrao,tick.bid);
         be_ativado = false;
        }
      if(Vender && PositionSelect(_Symbol)==true && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY)
        {
         FecharPosicao();
         desenhaLinhaVertical("Venda",velas[1].time,clrRed);
         VendaAMercado2(lotePadrao,tick.bid);
         be_ativado = false;
        }


      //---

      //Print("Lucro Acumulado = ", LucroAcumulado());

      //---

      //--- TESTE

      //if(PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY && Vender)
      //  {
      //   FechaPosicao();
      //  }else if(PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_SELL && Comprar)
      //          {
      //           FechaPosicao();
      //          }

      //---Breakeven
      if(liga_breakeven == SIM && PositionSelect(_Symbol) && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY)
        {
         double preco_entrada = PositionGetDouble(POSITION_PRICE_OPEN);
         double preco_sl      = PositionGetDouble(POSITION_SL);
         double preco_tp      = PositionGetDouble(POSITION_TP);
         double preco_medio   = (preco_entrada + preco_tp)/2;

         desenhaLinhaHorizontal("Compra",preco_medio,clrMagenta);

         if(tick.last >= preco_medio && !be_ativado)
           {
            trade.PositionModify(PositionGetTicket(0),preco_entrada,preco_tp);
            be_ativado = true;
           }

        }

      if(liga_breakeven == SIM && PositionSelect(_Symbol) && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_SELL)
        {
         double preco_entrada = PositionGetDouble(POSITION_PRICE_OPEN);
         double preco_sl      = PositionGetDouble(POSITION_SL);
         double preco_tp      = PositionGetDouble(POSITION_TP);
         double preco_medio   = (preco_entrada + preco_tp)/2;

         desenhaLinhaHorizontal("Compra",preco_medio,clrMagenta);

         if(tick.last <= preco_medio && !be_ativado)
           {
            trade.PositionModify(PositionGetTicket(0),preco_entrada,preco_tp);
            be_ativado = true;
           }
        }

      //--- STOP LOSS MOVEL

      if(liga_sl_movel == SIM && PositionSelect(_Symbol) && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY)
        {
         double preco_entrada = PositionGetDouble(POSITION_PRICE_OPEN);
         double preco_sl      = PositionGetDouble(POSITION_SL);
         double preco_tp      = PositionGetDouble(POSITION_TP);
         double novo_sl       = NormalizeDouble(tick.last-SLCompra*_Point,_Digits);

         double dist_sl       = SLCompra*_Point;

         if((tick.last - preco_sl) > dist_sl && preco_sl != novo_sl)
           {
            Print("Compra - SL atual = ", preco_sl, ", Novo = ", novo_sl, " , Preço de Entrada = ", preco_entrada);
            trade.PositionModify(PositionGetTicket(0),novo_sl,preco_tp);
           }
        }

      if(liga_sl_movel == SIM && PositionSelect(_Symbol) && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_SELL)
        {
         double preco_entrada = PositionGetDouble(POSITION_PRICE_OPEN);
         double preco_sl      = PositionGetDouble(POSITION_SL);
         double preco_tp      = PositionGetDouble(POSITION_TP);
         double novo_sl       = NormalizeDouble(tick.last+SLVenda*_Point,_Digits);

         double dist_sl       = SLVenda*_Point;

         if((preco_sl - tick.last) > dist_sl && preco_sl != novo_sl)
           {
            Print("Venda - SL atual = ", preco_sl, ", Novo = ", novo_sl, " , Preço de Entrada = ", preco_entrada);
            trade.PositionModify(PositionGetTicket(0),novo_sl,preco_tp);
           }
        }
     }

//---
   if(TimeToString(TimeCurrent(),TIME_MINUTES) == hora_limite_fecha_op && PositionSelect(_Symbol)==true && saberDiaDaSemana(TimeCurrent()) == 5)
     {
      Print("-----> Fim do Tempo Operacional: encerrar posições abertas!");

      FecharPosicao();
     }
  }

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool inicioOperacao(string inicio_op, string fim_op)
  {
   bool resp = false;

   datetime tc = TimeCurrent();

   if(TimeToString(tc,TIME_MINUTES)  >= inicio_op &&  TimeToString(tc,TIME_MINUTES)  <= fim_op)
     {
      resp = true;

     }
   else
     {
      resp = false;
     }

   return resp;
  }

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
int saberDiaDaSemana(datetime d)
  {
//0-dom, 1-seg, 2-ter, 3-qua, 5-qui, 6-sex, 7-sab
   MqlDateTime str;
   TimeToStruct(d,str);

   return str.day_of_week;
  }

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
int saberMesAno(datetime d)
  {
//0-dom, 1-seg, 2-ter, 3-qua, 5-qui, 6-sex, 7-sab
   MqlDateTime str;
   TimeToStruct(d,str);

   return str.mon;
  }
//+------------------------------------------------------------------+


//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void CompraAMercado(double num_lotes, double ask, double TK_, double SL_)
  {



   trade.Buy(num_lotes,_Symbol,NormalizeDouble(ask,_Digits),NormalizeDouble(ask - SL_*_Point,_Digits),
             NormalizeDouble(ask + TK_*_Point,_Digits));

   if(trade.ResultRetcode() == 10008 || trade.ResultRetcode() == 10009)
     {
      Print("Ordem de compra Executada com Sucesso!!");
     }
   else
     {
      Print("Erro de execução... ", GetLastError());
      ResetLastError();
     }

  }
//---

//---
void VendaAMercado(double num_lotes, double bid, double TK_, double SL_)
  {


   trade.Sell(num_lotes,_Symbol,NormalizeDouble(bid,_Digits),NormalizeDouble(bid + SL_*_Point,_Digits),
              NormalizeDouble(bid - TK_*_Point,_Digits));

   if(trade.ResultRetcode() == 10008 || trade.ResultRetcode() == 10009)
     {
      Print("Ordem de venda Executada com Sucesso!!");
     }
   else
     {
      Print("Erro de execução... ", GetLastError());
      ResetLastError();
     }

  }
//---
void CompraAMercado2(double num_lotes, double ask)
  {



   trade.Buy(num_lotes,_Symbol,NormalizeDouble(ask,_Digits));

   if(trade.ResultRetcode() == 10008 || trade.ResultRetcode() == 10009)
     {
      Print("Ordem de compra Executada com Sucesso!!");
     }
   else
     {
      Print("Erro de execução... ", GetLastError());
      ResetLastError();
     }

  }
//---

//---
void VendaAMercado2(double num_lotes, double bid)
  {


   trade.Sell(num_lotes,_Symbol,NormalizeDouble(bid,_Digits));

   if(trade.ResultRetcode() == 10008 || trade.ResultRetcode() == 10009)
     {
      Print("Ordem de venda Executada com Sucesso!!");
     }
   else
     {
      Print("Erro de execução... ", GetLastError());
      ResetLastError();
     }

  }
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void FecharPosicao()
  {

   ulong ticket = PositionGetTicket(0);

   trade.PositionClose(ticket);

   if(trade.ResultRetcode() == 10009)
     {
      Print("Fechamento Executado com Sucesso!!");
     }
   else
     {
      Print("Erro de execução... ", GetLastError());
      ResetLastError();
     }

  }


//+------------------------------------------------------------------+
//| FUNÇÕES PARA AUXILIAR NA VISUALIZAÇÃO DA ESTRATÉGIA              |
//+------------------------------------------------------------------+

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void desenhaLinhaVertical(string nome, datetime dt, color cor = clrAliceBlue)
  {
   ObjectDelete(0,nome);
   ObjectCreate(0,nome,OBJ_VLINE,0,dt,0);
   ObjectSetInteger(0,nome,OBJPROP_COLOR,cor);
  }
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void desenhaLinhaHorizontal(string nome, double price, color cor = clrAliceBlue)
  {
   ObjectDelete(0,nome);
   ObjectCreate(0,nome,OBJ_HLINE,0,0,price);
   ObjectSetInteger(0,nome,OBJPROP_COLOR,cor);
  }
//---

//+------------------------------------------------------------------+
//| FUNÇÕES ÚTEIS                                                    |
//+------------------------------------------------------------------+
double LucroAcumulado()
  {

   double lucro_acum = 0;
   double lucro = 0;

   HistorySelect(0,TimeCurrent());

   ulong tn = HistoryDealsTotal();

//Print("Total de negócios = ", tn);

//Print("Negócio 2 Lucro = ", );

   for(int i=1; i<=tn; i++)
     {
      ulong tick_n = HistoryDealGetTicket(i);

      lucro = HistoryDealGetDouble(tick_n,DEAL_PROFIT);
      //Print("Negócio (",i, ") , Lucro = ",lucro );

      lucro_acum = lucro_acum + lucro; // lucro_acum += lucro

     }

   return lucro_acum;
  }




//--- Para Mudança de Candle
bool TemosNovaVela()
  {
//--- memoriza o tempo de abertura da ultima barra (vela) numa variável
   static datetime last_time=0;
//--- tempo atual
   datetime lastbar_time= (datetime) SeriesInfoInteger(Symbol(),Period(),SERIES_LASTBAR_DATE);

//--- se for a primeira chamada da função:
   if(last_time==0)
     {
      //--- atribuir valor temporal e sair
      last_time=lastbar_time;
      return(false);
     }

//--- se o tempo estiver diferente:
   if(last_time!=lastbar_time)
     {
      //--- memorizar esse tempo e retornar true
      last_time=lastbar_time;
      return(true);
     }
//--- se passarmos desta linha, então a barra não é nova; retornar false
   return(false);
  }
//---
//int saberDiaDaSemana(datetime d)
//   {
//      //0-dom, 1-seg, 2-ter, 3-qua, 5-qui, 6-sex, 7-sab
//      MqlDateTime str;
//      TimeToStruct(d,str);
//
//      return str.day_of_week;
//   }

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
int saberAno(datetime d)
  {
//0-dom, 1-seg, 2-ter, 3-qua, 5-qui, 6-sex, 7-sab
   MqlDateTime str;
   TimeToStruct(d,str);

   return str.year;
  }

//      int saberMesAno(datetime d)
//   {
//      //0-dom, 1-seg, 2-ter, 3-qua, 5-qui, 6-sex, 7-sab
//      MqlDateTime str;
//      TimeToStruct(d,str);
//
//      return str.mon;
//   }

//     bool inicioOperacao(string inicio_op, string fim_op)
//   {
//      bool resp = false;
//
//      datetime tc = TimeCurrent();
//
//      if( TimeToString(tc,TIME_MINUTES)  >= inicio_op &&  TimeToString(tc,TIME_MINUTES)  <= fim_op )
//        {
//         resp = true;
//
//        }else
//           {
//            resp = false;
//           }
//
//      return resp;
//   }
//---

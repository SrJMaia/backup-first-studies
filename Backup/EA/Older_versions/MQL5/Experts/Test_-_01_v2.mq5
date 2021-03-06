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
//# EUR 'EURCHF','EURGBP','EURJPY','EURNZD','EURUSD','EURAUD','EURCAD'
//# GBP 'GBPAUD','GBPCHF','GBPJPY','GBPCAD','GBPUSD','GBPNZD'
//# USD 'USDCHF','USDJPY','AUDUSD','NZDUSD','USDCAD'
//# JPY 'AUDJPY','CADJPY','CHFJPY','NZDJPY'
//# CHF 'AUDCHF','CADCHF','NZDCHF'
//# NZD 'AUDNZD','NZDCAD'
//# AUD 'AUDCAD'
int eurusd_Handle;
double eurusd_Buffer[];
int eurchf_Handle;
double eurchf_Buffer[];
int eurgbp_Handle;
double eurgbp_Buffer[];
int eurjpy_Handle;
double eurjpy_Buffer[];
int eurnzd_Handle;
double eurnzd_Buffer[];
int euraud_Handle;
double euraud_Buffer[];
int eurcad_Handle;
double eurcad_Buffer[];

int gbpaud_Handle;
double gbpaud_Buffer[];
int gbpchf_Handle;
double gbpchf_Buffer[];
int gbpjpy_Handle;
double gbpjpy_Buffer[];
int gbpcad_Handle;
double gbpcad_Buffer[];
int gbpusd_Handle;
double gbpusd_Buffer[];
int gbpnzd_Handle;
double gbpnzd_Buffer[];

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

   eurusd_Handle = iCustom("EURUSD",PERIOD_CURRENT,"overbs_v2.ex5");
   if(eurusd_Handle == INVALID_HANDLE)
      return INIT_FAILED;
   eurchf_Handle = iCustom("EURCHF",PERIOD_CURRENT,"overbs_v2.ex5");
   if(eurchf_Handle == INVALID_HANDLE)
      return INIT_FAILED;
   eurgbp_Handle = iCustom("EURGBP",PERIOD_CURRENT,"overbs_v2.ex5");
   if(eurgbp_Handle == INVALID_HANDLE)
      return INIT_FAILED;
   eurjpy_Handle = iCustom("EURJPY",PERIOD_CURRENT,"overbs_v2.ex5");
   if(eurjpy_Handle == INVALID_HANDLE)
      return INIT_FAILED;
   eurnzd_Handle = iCustom("EURNZD",PERIOD_CURRENT,"overbs_v2.ex5");
   if(eurnzd_Handle == INVALID_HANDLE)
      return INIT_FAILED;
   euraud_Handle = iCustom("EURAUD",PERIOD_CURRENT,"overbs_v2.ex5");
   if(euraud_Handle == INVALID_HANDLE)
      return INIT_FAILED;
   eurcad_Handle = iCustom("EURCAD",PERIOD_CURRENT,"overbs_v2.ex5");
   if(eurcad_Handle == INVALID_HANDLE)
      return INIT_FAILED;

   gbpaud_Handle = iCustom("GBPAUD",PERIOD_CURRENT,"overbs_v2.ex5");
   if(gbpaud_Handle == INVALID_HANDLE)
      return INIT_FAILED;
   gbpchf_Handle = iCustom("GBPCHF",PERIOD_CURRENT,"overbs_v2.ex5");
   if(gbpchf_Handle == INVALID_HANDLE)
      return INIT_FAILED;
   gbpjpy_Handle = iCustom("GBPJPY",PERIOD_CURRENT,"overbs_v2.ex5");
   if(gbpjpy_Handle == INVALID_HANDLE)
      return INIT_FAILED;
   gbpcad_Handle = iCustom("GBPCAD",PERIOD_CURRENT,"overbs_v2.ex5");
   if(gbpcad_Handle == INVALID_HANDLE)
      return INIT_FAILED;
   gbpusd_Handle = iCustom("GBPUSD",PERIOD_CURRENT,"overbs_v2.ex5");
   if(gbpusd_Handle == INVALID_HANDLE)
      return INIT_FAILED;
   gbpnzd_Handle = iCustom("GBPNZD",PERIOD_CURRENT,"overbs_v2.ex5");
   if(gbpnzd_Handle == INVALID_HANDLE)
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

   IndicatorRelease(eurusd_Handle);
   IndicatorRelease(eurchf_Handle);
   IndicatorRelease(eurgbp_Handle);
   IndicatorRelease(eurjpy_Handle);
   IndicatorRelease(eurnzd_Handle);
   IndicatorRelease(eurcad_Handle);
   IndicatorRelease(euraud_Handle);
   
   IndicatorRelease(gbpaud_Handle);
   IndicatorRelease(gbpchf_Handle);
   IndicatorRelease(gbpjpy_Handle);
   IndicatorRelease(gbpcad_Handle);
   IndicatorRelease(gbpusd_Handle);
   IndicatorRelease(gbpnzd_Handle);
   

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
//---

//# EUR 'EURCHF','EURGBP','EURJPY','EURNZD','EURUSD','EURAUD','EURCAD'
   CopyBuffer(eurusd_Handle,0,0,4,eurusd_Buffer);
   CopyBuffer(eurchf_Handle,0,0,4,eurchf_Buffer);
   CopyBuffer(eurgbp_Handle,0,0,4,eurgbp_Buffer);   
   CopyBuffer(eurjpy_Handle,0,0,4,eurjpy_Buffer);
   CopyBuffer(eurnzd_Handle,0,0,4,eurnzd_Buffer);
   CopyBuffer(euraud_Handle,0,0,4,euraud_Buffer);   
   CopyBuffer(eurcad_Handle,0,0,4,eurcad_Buffer);
//# GBP 'GBPAUD','GBPCHF','GBPJPY','GBPCAD','GBPUSD','GBPNZD'
   CopyBuffer(gbpaud_Handle,0,0,4,gbpaud_Buffer);
   CopyBuffer(gbpchf_Handle,0,0,4,gbpchf_Buffer);   
   CopyBuffer(gbpjpy_Handle,0,0,4,gbpjpy_Buffer);
   CopyBuffer(gbpcad_Handle,0,0,4,gbpcad_Buffer);
   CopyBuffer(gbpusd_Handle,0,0,4,gbpusd_Buffer);   
   CopyBuffer(gbpnzd_Handle,0,0,4,gbpnzd_Buffer);

   CopyRates(_Symbol,_Period,0,4,velas);

// Ordenar o vetor de dados:
   ArraySetAsSeries(eurusd_Buffer,true);
   ArraySetAsSeries(eurchf_Buffer,true);
   ArraySetAsSeries(eurgbp_Buffer,true);
   ArraySetAsSeries(eurjpy_Buffer,true);
   ArraySetAsSeries(eurnzd_Buffer,true);
   ArraySetAsSeries(euraud_Buffer,true);
   ArraySetAsSeries(eurcad_Buffer,true);

   ArraySetAsSeries(gbpaud_Buffer,true);
   ArraySetAsSeries(gbpchf_Buffer,true);
   ArraySetAsSeries(gbpjpy_Buffer,true);
   ArraySetAsSeries(gbpcad_Buffer,true);
   ArraySetAsSeries(gbpusd_Buffer,true);
   ArraySetAsSeries(gbpnzd_Buffer,true);
//---
   

// Alimentar com dados variável de tick
   SymbolInfoTick(_Symbol,tick); 


// LOGICA PARA ATIVAR COMPRA

   bool Comprar = false; // Pode comprar?
   bool Vender  = false; // Pode vender?

   Comprar = false;
   Vender = false;
   
   double sum_eur = eurusd_Buffer[0] + eurchf_Buffer[0] + eurgbp_Buffer[0] + eurjpy_Buffer[0] +
                    eurnzd_Buffer[0] + euraud_Buffer[0] + eurcad_Buffer[0];
//# GBP 'GBPAUD','GBPCHF','GBPJPY','GBPCAD','GBPUSD','GBPNZD'
   double sum_gbp = gbpaud_Buffer[0] + gbpchf_Buffer[0] + gbpjpy_Buffer[0] + gbpcad_Buffer[0] +
                    gbpusd_Buffer[0] + gbpnzd_Buffer[0] + eurgbp_Buffer[0];
                    
   // 0.389089
   
   // 0.373071 GBP
   
//---
   
   bool buy = 0 > sum_eur > -(0.389089*2) && 0 < sum_gbp < (0.373071*2);
   bool sell = 0 < sum_eur < (0.389089*2) && 0 > sum_gbp > -(0.373071*2);
   
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
      if(buy && PositionSelect(_Symbol)==false)
        {
         CompraAMercado2(lotePadrao,tick.ask);
         be_ativado = false;
        }
      if(buy && PositionSelect(_Symbol) == true && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_SELL)
        {
         FecharPosicao();
         CompraAMercado2(lotePadrao,tick.ask);
         be_ativado = false;
        }
      // Condição de Venda:
      if(sell && PositionSelect(_Symbol)==false)
        {
         VendaAMercado2(lotePadrao,tick.bid);
         be_ativado = false;
        }
      if(sell && PositionSelect(_Symbol)==true && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY)
        {
         FecharPosicao();
         VendaAMercado2(lotePadrao,tick.bid);
         be_ativado = false;
        }

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

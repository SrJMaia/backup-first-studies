//+------------------------------------------------------------------+
//|                                                                  |
//|                                                    MonstroV5.mq5 |
//|                                                                  |
//+------------------------------------------------------------------+
#property copyright "Your Holding"
#property version   "5.0"
//---
#include <C:\Program Files\MetaTrader 5\MQL5\Include\Trade\Trade.mqh>
//#include <Experts/New_Folder/Modulos_EA.mqh>
#include <expert/expertbase.mqh>
#include <indicators/indicators.mqh>
#include <C:\Program Files\MetaTrader 5\MQL5\Include\Trade\PositionInfo.mqh>
#include <Trade\SymbolInfo.mqh>
//---
enum LIGA
  {
   SIM,        // Sim
   NAO         // Não
  };
//---
enum ESTRATEGIA_ENTRADA
  {
   APENAS_MM,  // Apenas Médias Móveis
   MM_E_TEMA,    // Triple Exponencial & MM
   APENAS_UMA_MM // Fechamento acima da média
  };
//---
input group "-----Estratégia de Entrada-----"
input ESTRATEGIA_ENTRADA   estrategia      = APENAS_MM;            // Estratégia de Entrada Trader
input LIGA liga_breakeven                  = NAO;                  // Liga BreakEven
input LIGA liga_sl_movel                   = SIM;                  // Liga SL Movel
//---
input group "-----Parâmetros de Entrada MM Cruzamento-----"
input int mm_rapida_periodo                = 12;                   // Periodo Média Rápida
input int mm_lenta_periodo                 = 32;                   // Periodo Média Lenta
input ENUM_TIMEFRAMES mm_tempo_grafico     = PERIOD_CURRENT;       // Tempo Gráfico
input ENUM_MA_METHOD  mm_metodoRapida      = MODE_EMA;             // Método MM Rápida
input ENUM_MA_METHOD  mm_metodoLenta       = MODE_EMA;             // Método MM Lenta
input ENUM_APPLIED_PRICE  mm_preco         = PRICE_CLOSE;          // Preço Aplicado
//---
input group "-----Parâmetros de Entrada TEMA-----"
input int tema_periodo                     = 12;                   // Periodo
input ENUM_TIMEFRAMES tema_tempo_grafico   = PERIOD_CURRENT;       // Tempo Gráfico
input ENUM_APPLIED_PRICE  tema_preco       = PRICE_CLOSE;          // Preço Aplicado
input group "-----Parâmetros de Entrada MM Solitária-----"
input int mm_solo                          = 32;                   // Periodo Média Solo
input ENUM_TIMEFRAMES mm_solo_tgrafico     = PERIOD_CURRENT;       // Tempo Gráfico
input ENUM_MA_METHOD  mm_metodoSolo        = MODE_EMA;             // Método MM Solo
input ENUM_APPLIED_PRICE  mm_solo_preco    = PRICE_CLOSE;          // Preço Aplicado
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
//--- Médias Móveis
// RÁPIDA - menor período
int mm_rapida_Handle;      // Handle controlador da média móvel rápida
double mm_rapida_Buffer[]; // Buffer para armazenamento dos dados das médias

// LENTA - maior período
int mm_lenta_Handle;      // Handle controlador da média móvel lenta
double mm_lenta_Buffer[]; // Buffer para armazenamento dos dados das médias

// TEMA
int tema_Handle;
double tema_Buffer[];

// MM SOLO
int mm_solo_Handle;
double mm_solo_Buffer[];

int magic_number = 111;

int c_indi_Handle;
double c_indi_Buffer[];

int std_indi_Handle;
double std_indi_Buffer[];

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
      
   c_indi_Handle = iCustom(_Symbol,PERIOD_CURRENT,"pct_Change.ex5",1);

   mm_rapida_Handle = iMA(_Symbol,mm_tempo_grafico,mm_rapida_periodo,0,mm_metodoRapida,mm_preco);
   mm_lenta_Handle  = iMA(_Symbol,mm_tempo_grafico,mm_lenta_periodo,0,mm_metodoLenta,mm_preco);

   tema_Handle      = iTEMA(_Symbol,tema_tempo_grafico,tema_periodo,0,tema_preco);

   mm_solo_Handle   = iMA(_Symbol,mm_solo_tgrafico,mm_solo,0,mm_metodoSolo,mm_solo_preco);

   if(c_indi_Handle<0)
     {
      Alert("Erro ao tentar criar Handles para o indicador - erro: ",GetLastError(),"!");
      return(-1);
     }

   if(mm_rapida_Handle<0 || mm_lenta_Handle<0)
     {
      Alert("Erro ao tentar criar Handles para o indicador - erro: ",GetLastError(),"!");
      return(-1);
     }

   if(tema_Handle < 0)
     {
      Alert("Erro ao tentar criar Handles para o indicador - erro: ",GetLastError(),"!");
      return(-1);
     }

   if(mm_solo_Handle < 0)
     {
      Alert("Erro ao tentar criar Handles para o indicador - erro: ",GetLastError(),"!");
      return(-1);
     }

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
   IndicatorRelease(std_indi_Handle);
   IndicatorRelease(c_indi_Handle);
   IndicatorRelease(mm_rapida_Handle);
   IndicatorRelease(mm_lenta_Handle);

   IndicatorRelease(tema_Handle);

   IndicatorRelease(mm_solo_Handle);
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

//---
//desenhaLinhaVertical("L1",tick.time,clrRed);
// Copiar um vetor de dados tamanho três para o vetor mm_Buffer
   CopyBuffer(std_indi_Handle,0,0,4,std_indi_Buffer);
   CopyBuffer(c_indi_Handle,0,0,4,c_indi_Buffer);
   CopyBuffer(mm_rapida_Handle,0,0,4,mm_rapida_Buffer);
   CopyBuffer(mm_lenta_Handle,0,0,4,mm_lenta_Buffer);
//
   CopyBuffer(tema_Handle,0,0,4,tema_Buffer);
//
   CopyBuffer(mm_solo_Handle,0,0,4,mm_solo_Buffer);

//--- Alimentar Buffers das Velas com dados:
   CopyRates(_Symbol,_Period,0,4,velas);
   ArraySetAsSeries(velas,true);

// Ordenar o vetor de dados:
   ArraySetAsSeries(std_indi_Buffer,true);
   ArraySetAsSeries(c_indi_Buffer,true);
   ArraySetAsSeries(mm_rapida_Buffer,true);
   ArraySetAsSeries(mm_lenta_Buffer,true);
//
   ArraySetAsSeries(tema_Buffer,true);
//
   ArraySetAsSeries(mm_solo_Buffer,true);
//---

// Alimentar com dados variável de tick
   SymbolInfoTick(_Symbol,tick);

// LOGICA PARA ATIVAR COMPRA
   
   bool venda_custom = c_indi_Buffer[0] > 0.001 && c_indi_Buffer[2] < 0.001;

   bool compra_custom = c_indi_Buffer[0] < -0.001 && c_indi_Buffer[2] > -0.001;

   bool compra_mm_cros = mm_rapida_Buffer[0] > mm_lenta_Buffer[0] &&
                         mm_rapida_Buffer[2] < mm_lenta_Buffer[2] ;

// LÓGICA PARA ATIVAR VENDA
   bool venda_mm_cros = mm_lenta_Buffer[0] > mm_rapida_Buffer[0] &&
                        mm_lenta_Buffer[2] < mm_rapida_Buffer[2];

//---
   bool compra_tema_cross = tema_Buffer[0] > mm_solo_Buffer[0] &&
                            tema_Buffer[2] < mm_solo_Buffer[2] ;

   bool venda_tema_cross  = mm_solo_Buffer[0] > tema_Buffer[0] &&
                            mm_solo_Buffer[2] < tema_Buffer[2] ;

//---
   bool compra_mm_solo = rates[0].close > mm_solo_Buffer[0] &&
                         rates[2].close < mm_solo_Buffer[2];

   bool venda_mm_solo  = mm_solo_Buffer[0] > rates[0].close &&
                         mm_solo_Buffer[2] < rates[2].close;


   bool Comprar = false; // Pode comprar?
   bool Vender  = false; // Pode vender?

   if(estrategia == APENAS_MM)
     {
      Comprar = compra_mm_cros;
      Vender  = venda_mm_cros;
     }
   else
      if(estrategia == MM_E_TEMA)
        {
         Comprar = compra_tema_cross;
         Vender = venda_tema_cross;
        }
      else
         if(estrategia == APENAS_UMA_MM)
           {
            Comprar = compra_mm_solo;
            Vender = venda_mm_solo;
           }

   Comprar = compra_custom;
   Vender = venda_custom;

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
      Print(c_indi_Buffer[0]);
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

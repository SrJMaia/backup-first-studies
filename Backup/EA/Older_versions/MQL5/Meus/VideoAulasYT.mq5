//+------------------------------------------------------------------+
//|                                                 VideoAulasYT.mq5 |
//|                        Copyright 2020, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2020, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"

#include <Trade\Trade.mqh>
CTrade trade;

input group           "Nome do grupo" 
input int                     ma_periodo = 20;//Período da Média
input int                     ma_desloc = 0;//Deslocamento da Média
input ENUM_MA_METHOD          ma_metodo = MODE_SMA;//Método Média Móvel
input ENUM_APPLIED_PRICE      ma_preco = PRICE_CLOSE;//Preço para Média
input ulong                   magicNum = 123456;//Magic Number
input ulong                   desvPts = 50;//Desvio em Pontos
input ENUM_ORDER_TYPE_FILLING preenchimento = ORDER_FILLING_RETURN;//Preenchimento da Ordem

input double                  lote = 0.01;//Volume
input double                  stopLoss = 5;//Stop Loss
input double                  takeProfit = 5;//Take Profit

input int                     posicoesAbertas = 2;

double                        PRC;//Preço normalizado
double                        STL;//StopLoss normalizado
double                        TKP;//TakeProfit normalizado

// variaveis podem ser estacadas
// double ask, bid, last;
// Array armazena os dados dos indicadores
   double smaArray[];
//   Handle recebe o metodo da media movel do MT5
   int smaHandle;
   
   bool                       posAberta;
   
   MqlTick                    ultimoTick;
   MqlRates                   rates[];

int OnInit()
  {
//---

//   Handle recebeu os dados da SMA, eu ativo o meu array e entao passo os dados pra ele
// Handle recebe as seguintes informações, paridade, periodo, valor da SMA, desvio, tipo de media, tipo de preço aplicado
   smaHandle = iMA(_Symbol, _Period, ma_periodo, ma_desloc, ma_metodo, ma_preco);
   if(smaHandle==INVALID_HANDLE)
         {
            Print("Erro ao criar média móvel - erro", GetLastError());
            return(INIT_FAILED);
         }
   ArraySetAsSeries(smaArray, true);
   ArraySetAsSeries(rates, true);

//---

// ha tres tipos de ordens para serem enviadas
   trade.SetTypeFilling(ORDER_FILLING_RETURN);
//   quantos pontos e aceitavel pra sua ordem ser executada caso haja spread ou volatidadde alta
   trade.SetDeviationInPoints(0);
//   O numero magico e mais util quando se tem mais de um robo operando
   trade.SetExpertMagicNumber(123456);

//---



//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//---

  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//---

// A função retorna false ou true, a ! na frente da função faz com que caso retorne false na função, o que esta dentro do if sera verdadeiro
  if(!SymbolInfoTick(_Symbol, ultimoTick))
         {
            Alert("Erro ao obter informações de preços: ", GetLastError());
            return;
         }
         
//   ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
//   bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
//   Last é last price, ultimo preço negociado
//   last = SymbolInfoDouble(_Symbol, SYMBOL_LAST);
   
    if(CopyBuffer(smaHandle, 0, 0, 3, smaArray)<0)
         {
         Alert("Erro ao copiar dados da média móvel: ", GetLastError());
         return;
         }
         
       if(CopyRates(_Symbol, _Period, 0, 3, rates)<0)
         {
            Alert("Erro ao obter as informações de MqlRates: ", GetLastError());
            return;
         }
         
      // Com essa função ira checar se há posições abertas apenas deste robo, sem interfiri em outros
      posAberta = false;
      for(int i = PositionsTotal()-1; i>=0; i--)
         {
            string symbol = PositionGetSymbol(i);
            ulong magic = PositionGetInteger(POSITION_MAGIC);
            if(symbol == _Symbol && magic==magicNum)
               {  
                  posAberta = true;
                  break;
               }
         }

// Ordem de compra não esta funcionando
    if(ultimoTick.last>smaArray[0] && rates[1].close>rates[1].open && !posAberta && PositionsTotal() < posicoesAbertas)
         {
            //if(trade.Buy(lote, _Symbol, ask, ask-stopLoss, ask+takeProfit, ""))
            PRC = NormalizeDouble(ultimoTick.ask, _Digits);
            STL = NormalizeDouble(PRC - stopLoss, _Digits);
            TKP = NormalizeDouble(PRC + takeProfit, _Digits);
            if(trade.Buy(lote, _Symbol, PRC, STL, TKP, ""))               {
                  Print("Ordem de Compra - sem falha. ResultRetcode: ", trade.ResultRetcode(), ", RetcodeDescription: ", trade.ResultRetcodeDescription());
               }
            else
               {
                  Print("Ordem de Compra - com falha. ResultRetcode: ", trade.ResultRetcode(), ", RetcodeDescription: ", trade.ResultRetcodeDescription());
               }
         }
      else if(ultimoTick.last<smaArray[0] && rates[1].close<rates[1].open && !posAberta && PositionsTotal() < posicoesAbertas)
         {
            PRC = NormalizeDouble(ultimoTick.bid, _Digits);
            STL = NormalizeDouble(PRC + stopLoss, _Digits);
            TKP = NormalizeDouble(PRC - takeProfit, _Digits);
            if(trade.Sell(lote, _Symbol, PRC, STL, TKP, ""))               {
                  Print("Ordem de Venda - sem falha. ResultRetcode: ", trade.ResultRetcode(), ", RetcodeDescription: ", trade.ResultRetcodeDescription());
               }
            else
               {
                  Print("Ordem de Venda - com falha. ResultRetcode: ", trade.ResultRetcode(), ", RetcodeDescription: ", trade.ResultRetcodeDescription());
               }
         } 

   
   //Comment("Preço ASK = ", ask, "\nPreço BID = ", bid);
   
  }
//+------------------------------------------------------------------+

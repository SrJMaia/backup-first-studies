//+------------------------------------------------------------------+
//|                                                                  |
//|                                                    MonstroV5.mq5 |
//|                                                                  |
//+------------------------------------------------------------------+
#property copyright "Your Holding"
#property version   "5.0"
//---
#include <Trade/Trade.mqh>
#include <Modulos_EA.mqh>
#include <expert/expertbase.mqh>
#include <trade/trade.mqh>
#include <indicators/indicators.mqh>
// "-----Estratégia de Entrada-----"
bool estrategia                    = true;                   // Estratégia de Entrada Trader
bool liga_breakeven                = true;                   // Liga BreakEven
// "-----Gerenciamento e Estrategia-----"
double TKCompra                      = 3000;                 // Take Profit
double SLCompra                      = 1300;                 // Stop Loss
double TKVenda                       = 1200;                 // Take Profit
double SLVenda                       = 1100;                 // Stop Loss
double risco                         = 3;                    // Capital a Ser Arriscado por Operação
double alavancagem                   = 500;                  // Alavancagem da Conta
// MM SOLO
int mm_solo_Handle;
double mm_solo_Buffer[];

int magic_number = 1001;

//+------------------------------------------------------------------+
//| Variáveis para as funçoes                                        |
//+------------------------------------------------------------------+

MqlRates velas[];            // Variável para armazenar velas
MqlTick tick;                // Variável para armazenar ticks
MqlRates rates[];            // Variavel para armazenar preços

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//---
   
   mm_solo_Handle   = iMA("EURUSD",PERIOD_D1,200,0,MODE_SMA,PRICE_CLOSE);
      
        if(mm_solo_Handle < 0)
     {
      Alert("Erro ao tentar criar Handles para o indicador - erro: ",GetLastError(),"!");
      return(-1);
     }
   
   CopyRates("EURUSD",PERIOD_D1,0,4,velas);
   ArraySetAsSeries(velas,true);
   
   ArraySetAsSeries(rates,true);
   
   ChartIndicatorAdd(0,0,mm_solo_Handle);
   
   //---

   return(INIT_SUCCEEDED);
  }

void OnDeinit(const int reason)
  {
   IndicatorRelease(mm_solo_Handle);
  }
  
bool be_ativado = false;
bool PositionClosePartial = true;

void OnTick()
  {   
   if (CopyRates("EURUSD", PERIOD_D1, 0, 3, rates)<0)
      {
         Alert("Erro ao obter as informações de MqlRates: ", GetLastError());
         return;
      }
   
//---

    CopyBuffer(mm_solo_Handle,0,0,4,mm_solo_Buffer);
        
    //--- Alimentar Buffers das Velas com dados:
    CopyRates("EURUSD",PERIOD_D1,0,4,velas);
    ArraySetAsSeries(velas,true);
    
    //
    ArraySetAsSeries(mm_solo_Buffer,true);
    //---
    
    // Alimentar com dados variável de tick
    SymbolInfoTick("EURUSD",tick);
   
   //---
    bool compra_mm_solo = rates[0].close > mm_solo_Buffer[0] &&
                          rates[2].close < mm_solo_Buffer[2];
    
    bool venda_mm_solo  = mm_solo_Buffer[0] > rates[0].close &&
                          mm_solo_Buffer[2] < rates[2].close;               
                            
                               
    bool Comprar = false; // Pode comprar?
    bool Vender  = false; // Pode vender?
    
    if(estrategia == true)
       {
        Comprar = compra_mm_solo;
        Vender = venda_mm_solo;                       
       }
      
   //---
   
   double lotePadrao;
   double porcentagem = risco/100;
   double calcTeste = ((AccountInfoDouble(ACCOUNT_BALANCE)*porcentagem)*alavancagem)/100000;;
   if(calcTeste < 0.01)
     {
      lotePadrao = 0.01;
     }else if(calcTeste > 99.99)
             {
              lotePadrao = 99.99;
             }else
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
       if(Comprar && PositionSelect("EURUSD")==false && PositionsTotal() <= 5  && (saberMesAno(TimeCurrent()) != 6))
         {
                    desenhaLinhaVertical("Compra",velas[1].time,clrBlue);
                    CompraAMercado(lotePadrao,tick.ask,TKCompra,SLCompra);
                    be_ativado = false;
         }
              // Condição de Venda:
       if(Vender && PositionSelect("EURUSD")==false && PositionsTotal() <= 5  && (saberMesAno(TimeCurrent()) != 6))
         {
                   desenhaLinhaVertical("Venda",velas[1].time,clrRed);
                   VendaAMercado(lotePadrao,tick.bid,TKVenda,SLVenda);
                   be_ativado = false; 
         }

          
       //---
       
      Print("Lucro Acumulado = ", LucroAcumulado());
        
        //---Breakeven
        if(be_ativado == false && PositionSelect("EURUSD") && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY)
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
        
        if(be_ativado == false && PositionSelect("EURUSD") && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_SELL)
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
      }
    
    //---
  }

      int saberMesAno(datetime d)
   {
      //0-dom, 1-seg, 2-ter, 3-qua, 5-qui, 6-sex, 7-sab
      MqlDateTime str;
      TimeToStruct(d,str);
      
      return str.mon;
   }
//+------------------------------------------------------------------+
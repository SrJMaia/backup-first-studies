#property copyright "Your Holding"
#property version   "5.0"
//---
#include <Trade/Trade.mqh>
#include <Modulos_EA.mqh>
#include <expert/expertbase.mqh>
#include <trade/trade.mqh>
#include <indicators/indicators.mqh>
//---             EURUSD
//---
//---             D1
double TKCompraEURUSDD1             = 3000;        
double SLCompraEURUSDD1             = 1300;            
double TKVendaEURUSDD1              = 1200;          
double SLVendaEURUSDD1              = 1100;    
int mm_solo_EURUSD_D1_Handle;
double mm_solo_EURUSD_D1_Buffer[];       
//---             H1
double TKCompraEURUSDH1             = 1100;             
double SLCompraEURUSDH1             = 400;              
double TKVendaEURUSDH1              = 900;                
double SLVendaEURUSDH1              = 400;            
string inicioCompraEURUSDH1         = "04:00";            
string fimCompraEURUSDH1            = "16:00";         
string inicioVendaEURUSDH1          = "08:00";         
string fimVendaEURUSDH1             = "17:00";         
int mm_solo_EURUSD_H1_Handle;
double mm_solo_EURUSD_H1_Buffer[];
//---             M15
double TKCompraEURUSDM15            = 900;
double SLCompraEURUSDM15            = 900;
double TKVendaEURUSDM15             = 700;
double SLVendaEURUSDM15             = 800;
string inicioEURUSDM15              = "13:00";
string fimEURUSDM15                 = "16:00";
int mm_rapida_EURUSD_M15_Handle;
int mm_lenta_EURUSD_M15_Handle;
double mm_rapida_EURUSD_M15_Buffer[];
double mm_lenta_EURUSD_M15_Buffer[];
//---
int magic_number = 111;
string hora_limite_fecha_op         = "3:00";               // Horário Limite para Fechar Operação
//---
MqlRates velas[];      
MqlTick tickEURUSD;           
MqlRates rates[];        
//---
int OnInit()
  {
  
  //---           EURUSD
  //---
  //---           D1
   mm_solo_EURUSD_D1_Handle   = iMA("EURUSD",PERIOD_D1,200,0,MODE_SMA,PRICE_CLOSE);
   CopyRates("EURUSD",PERIOD_D1,0,4,velas);
   
           if(mm_solo_EURUSD_D1_Handle < 0)
     {
      Alert("Erro ao tentar criar Handles para o indicador - erro: ",GetLastError(),"!");
      return(-1);
     }
  //---           H1
   mm_solo_EURUSD_H1_Handle   = iMA("EURUSD",PERIOD_H1,100,0,MODE_SMA,PRICE_CLOSE);
   CopyRates("EURUSD",PERIOD_D1,0,4,velas);
       
        if(mm_solo_EURUSD_H1_Handle < 0)
     {
      Alert("Erro ao tentar criar Handles para o indicador - erro: ",GetLastError(),"!");
      return(-1);
     }
   //---          M15
   mm_rapida_EURUSD_M15_Handle = iMA("EURUSD",PERIOD_M15,8,0,MODE_EMA,PRICE_CLOSE);
   mm_lenta_EURUSD_M15_Handle  = iMA("EURUSD",PERIOD_M15,21,0,MODE_SMA,PRICE_CLOSE);
   CopyRates("EURUSD",PERIOD_M15,0,4,velas);
   if(mm_rapida_EURUSD_M15_Handle <0 || mm_lenta_EURUSD_M15_Handle < 0)
     {
      Alert("Erro ao tentar criar Handles para o indicador - erro: ",GetLastError(),"!");
      return(-1);
     }
   //---
      
   ArraySetAsSeries(velas,true);
   ArraySetAsSeries(rates,true);
   
   //---
   
   return(INIT_SUCCEEDED);
  
  }
  
void OnDeinit(const int reason)

  {   
   
   IndicatorRelease(mm_solo_EURUSD_D1_Handle);
   IndicatorRelease(mm_solo_EURUSD_H1_Handle);
   IndicatorRelease(mm_lenta_EURUSD_M15_Handle);
   IndicatorRelease(mm_rapida_EURUSD_M15_Handle);
      
  }

bool be_ativado = false;

void OnTick()
  {
   
   //---          EURUSD
    SymbolInfoTick("EURUSD",tickEURUSD);
   //---
   //---          D1
   if (CopyRates("EURUSD", PERIOD_D1, 0, 3, rates)<0)
      {
         Alert("Erro ao obter as informações de MqlRates: ", GetLastError());
         return;
      }
    CopyBuffer(mm_solo_EURUSD_D1_Handle,0,0,4,mm_solo_EURUSD_D1_Buffer);
    CopyRates("EURUSD",PERIOD_D1,0,4,velas);
    ArraySetAsSeries(mm_solo_EURUSD_D1_Buffer,true);
    bool compra_EURUSD_D1 = rates[0].close > mm_solo_EURUSD_D1_Buffer[0] &&
                          rates[2].close < mm_solo_EURUSD_D1_Buffer[2];
    bool venda_EURUSD_D1  = mm_solo_EURUSD_D1_Buffer[0] > rates[0].close &&
                          mm_solo_EURUSD_D1_Buffer[2] < rates[2].close; 
   //---          H1
   if (CopyRates("EURUSD", PERIOD_H1, 0, 3, rates)<0)
      {
         Alert("Erro ao obter as informações de MqlRates: ", GetLastError());
         return;
      }
    CopyBuffer(mm_solo_EURUSD_H1_Handle,0,0,4,mm_solo_EURUSD_H1_Buffer);
    CopyRates("EURUSD",PERIOD_H1,0,4,velas);
    ArraySetAsSeries(mm_solo_EURUSD_H1_Buffer,true);
    bool compra_EURUSD_H1 = rates[0].close > mm_solo_EURUSD_H1_Buffer[0] &&
                          rates[2].close < mm_solo_EURUSD_H1_Buffer[2];
    bool venda_EURUSD_H1  = mm_solo_EURUSD_H1_Buffer[0] > rates[0].close &&
                          mm_solo_EURUSD_H1_Buffer[2] < rates[2].close; 
   //---          M15
   if (CopyRates("EURUSD", PERIOD_M15, 0, 3, rates)<0)
      {
         Alert("Erro ao obter as informações de MqlRates: ", GetLastError());
         return;
      }
    CopyBuffer(mm_rapida_EURUSD_M15_Handle,0,0,4,mm_rapida_EURUSD_M15_Buffer);
    CopyBuffer(mm_lenta_EURUSD_M15_Handle,0,0,4,mm_lenta_EURUSD_M15_Buffer);
    CopyRates("EURUSD",PERIOD_M15,0,4,velas);
    ArraySetAsSeries(mm_rapida_EURUSD_M15_Buffer,true);
    ArraySetAsSeries(mm_lenta_EURUSD_M15_Buffer,true);
    bool compra_EURUSD_M15 = mm_rapida_EURUSD_M15_Buffer[0] > mm_lenta_EURUSD_M15_Buffer[0] &&
                          mm_rapida_EURUSD_M15_Buffer[2] < mm_lenta_EURUSD_M15_Buffer[2] ;
    bool venda_EURUSD_M15 = mm_lenta_EURUSD_M15_Buffer[0] > mm_rapida_EURUSD_M15_Buffer[0] &&
                         mm_lenta_EURUSD_M15_Buffer[2] < mm_rapida_EURUSD_M15_Buffer[2];
   //---

    ArraySetAsSeries(velas,true);
 
   //---
                         
    bool Comprar = false;
    bool Vender  = false;
      
   //---
   
   double loteD1;
   double porcentagemD1 = 1.5/100;
   double calcTesteD1 = (((AccountInfoDouble(ACCOUNT_BALANCE)*porcentagemD1)*500)/100000)/SymbolInfoDouble(_Symbol,SYMBOL_BID);;
   if(calcTesteD1 < 0.01)
     {
      loteD1 = 0.01;
     }else if(calcTesteD1 > 99.99)
             {
              loteD1 = 99.99;
             }else
               {
                loteD1 = ( DoubleToString(calcTesteD1,2));
               }
               
   double loteH1;
   double porcentagemH1 = 1.0/100;
   double calcTesteH1 = (((AccountInfoDouble(ACCOUNT_BALANCE)*porcentagemH1)*500)/100000)/SymbolInfoDouble(_Symbol,SYMBOL_BID);;
   if(calcTesteH1 < 0.01)
     {
      loteH1 = 0.01;
     }else if(calcTesteH1 > 99.99)
             {
              loteH1 = 99.99;
             }else
               {
                loteH1 = (DoubleToString(calcTesteH1,2));
               }
    
   double loteM15;
   double porcentagemM15 = 0.5/100;
   double calcTesteM15 = (((AccountInfoDouble(ACCOUNT_BALANCE)*porcentagemM15)*500)/100000)/SymbolInfoDouble(_Symbol,SYMBOL_BID);;
   if(calcTesteM15 < 0.01)
     {
      loteM15 = 0.01;
     }else if(calcTesteM15 > 99.99)
             {
              loteM15 = 99.99;
             }else
               {
                loteM15 = (DoubleToString(calcTesteM15,2));
               }
   
   //---

    bool temosNovaVela = TemosNovaVela(); 
    
   //---              EURUSD - D1
   
    if(temosNovaVela && PositionsTotal() <= 1000 && PERIOD_D1)
      { 
       Comprar = compra_EURUSD_D1;
       Vender = venda_EURUSD_D1;
       if(Comprar && PositionSelect("EURUSD") == false && (saberMesAno(TimeCurrent()) != 6))
         {
                    desenhaLinhaVertical("Compra",velas[1].time,clrBlue);
                    CompraAMercado(loteD1,tickEURUSD.ask,TKCompraEURUSDD1,SLCompraEURUSDD1);
                    be_ativado = false;
         }
       if(Vender && PositionSelect("EURUSD") == false && (saberMesAno(TimeCurrent()) != 6))
         {
                   desenhaLinhaVertical("Venda",velas[1].time,clrRed);
                   VendaAMercado(loteD1,tickEURUSD.bid,TKVendaEURUSDD1,SLVendaEURUSDD1);
                   be_ativado = false; 
         }
       }
       
         if(be_ativado == false && PositionSelect("EURUSD") && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY && PERIOD_D1)
          {
           double preco_entrada = PositionGetDouble(POSITION_PRICE_OPEN);
           double preco_sl      = PositionGetDouble(POSITION_SL);
           double preco_tp      = PositionGetDouble(POSITION_TP);
           double preco_medio   = (preco_entrada + preco_tp)/2;    
           
           desenhaLinhaHorizontal("Compra",preco_medio,clrMagenta); 
           
           if(tickEURUSD.last >= preco_medio && !be_ativado)
             {
              trade.PositionModify(PositionGetTicket(0),preco_entrada,preco_tp);
              be_ativado = true;
             }   
                             
          }
        
        if(be_ativado == false && PositionSelect("EURUSD") && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_SELL && PERIOD_D1)
          {
           double preco_entrada = PositionGetDouble(POSITION_PRICE_OPEN);
           double preco_sl      = PositionGetDouble(POSITION_SL);
           double preco_tp      = PositionGetDouble(POSITION_TP);
           double preco_medio   = (preco_entrada + preco_tp)/2;
           
           desenhaLinhaHorizontal("Compra",preco_medio,clrMagenta);
           
           if(tickEURUSD.last <= preco_medio && !be_ativado)
             {
              trade.PositionModify(PositionGetTicket(0),preco_entrada,preco_tp);
              be_ativado = true;
             }       
          }
   
   //---              EURUSD - H1
   
    if(temosNovaVela  && PositionsTotal() <= 1000 && PERIOD_H1)
      { 
         Comprar = compra_EURUSD_H1;
         Vender = venda_EURUSD_H1;
       if(Comprar && PositionSelect("EURUSD") == false && inicioOperacao(inicioCompraEURUSDH1,fimCompraEURUSDH1) &&
         (saberMesAno(TimeCurrent()) != 5 && saberMesAno(TimeCurrent()) != 8) &&
         (saberAno(TimeCurrent()) != 2015) && (saberAno(TimeCurrent()) != 2014))        
         {
                    desenhaLinhaVertical("Compra",velas[1].time,clrBlue);
                    CompraAMercado(loteH1,tickEURUSD.ask,TKCompraEURUSDH1,SLCompraEURUSDH1);
                    be_ativado = false;
         }
       if(Vender && PositionSelect("EURSUSD") == false && inicioOperacao(inicioVendaEURUSDH1,fimVendaEURUSDH1) &&
         (saberMesAno(TimeCurrent()) != 3 && saberMesAno(TimeCurrent()) != 4 && saberMesAno(TimeCurrent()) != 6 && saberMesAno(TimeCurrent()) != 7 && saberMesAno(TimeCurrent()) != 12) &&
         (saberAno(TimeCurrent()) != 2013))
         {
                   desenhaLinhaVertical("Venda",velas[1].time,clrRed);
                   VendaAMercado(loteH1,tickEURUSD.bid,TKVendaEURUSDH1,SLVendaEURUSDH1);
                   be_ativado = false; 
         }
        if(be_ativado == false && PositionSelect("EURUSD") && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY && PERIOD_H1)
          {
           double preco_entrada = PositionGetDouble(POSITION_PRICE_OPEN);
           double preco_sl      = PositionGetDouble(POSITION_SL);
           double preco_tp      = PositionGetDouble(POSITION_TP);
           double preco_medio   = (preco_entrada + preco_tp)/2;    
           
           desenhaLinhaHorizontal("Compra",preco_medio,clrMagenta); 
           
           if(tickEURUSD.last >= preco_medio && !be_ativado)
             {
              trade.PositionModify(PositionGetTicket(0),preco_entrada,preco_tp);
              be_ativado = true;
             }                  
          }
        }
        if(be_ativado == false && PositionSelect("EURUSD") && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_SELL && PERIOD_H1)
          {
           double preco_entrada = PositionGetDouble(POSITION_PRICE_OPEN);
           double preco_sl      = PositionGetDouble(POSITION_SL);
           double preco_tp      = PositionGetDouble(POSITION_TP);
           double preco_medio   = (preco_entrada + preco_tp)/2;
           
           desenhaLinhaHorizontal("Compra",preco_medio,clrMagenta);
           
           if(tickEURUSD.last <= preco_medio && !be_ativado)
             {
              trade.PositionModify(PositionGetTicket(0),preco_entrada,preco_tp);
              be_ativado = true;
             }       
          } 
          
   //---              EURUSD - M15
   
    if(temosNovaVela  && PositionsTotal() <= 1000 && PERIOD_M15)
      { 
         Comprar = compra_EURUSD_M15;
         Vender = venda_EURUSD_M15;
       if(Comprar && PositionSelect("EURUSD") == false && inicioOperacao(inicioEURUSDM15,fimEURUSDM15) &&
         (saberMesAno(TimeCurrent()) != 2 && saberMesAno(TimeCurrent()) != 5 && saberMesAno(TimeCurrent()) != 8 && 
          saberMesAno(TimeCurrent()) != 10 && saberMesAno(TimeCurrent()) != 11))      
         {
                    desenhaLinhaVertical("Compra",velas[1].time,clrBlue);
                    CompraAMercado(loteM15,tickEURUSD.ask,TKCompraEURUSDM15,SLCompraEURUSDM15);
                    be_ativado = false;
         }
       if(Vender && PositionSelect("EURSUSD") == false && inicioOperacao(inicioEURUSDM15,fimEURUSDM15) &&
         (saberMesAno(TimeCurrent()) != 1 && saberMesAno(TimeCurrent()) != 3 && saberMesAno(TimeCurrent()) != 4 && 
          saberMesAno(TimeCurrent()) != 6 && saberMesAno(TimeCurrent()) != 7 && saberMesAno(TimeCurrent()) != 9))
         {
                   desenhaLinhaVertical("Venda",velas[1].time,clrRed);
                   VendaAMercado(loteM15,tickEURUSD.bid,TKVendaEURUSDM15,SLVendaEURUSDM15);
                   be_ativado = false; 
         }
        if(be_ativado == false && PositionSelect("EURUSD") && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY && PERIOD_M15)
          {
           double preco_entrada = PositionGetDouble(POSITION_PRICE_OPEN);
           double preco_sl      = PositionGetDouble(POSITION_SL);
           double preco_tp      = PositionGetDouble(POSITION_TP);
           double preco_medio   = (preco_entrada + preco_tp)/2;    
           
           desenhaLinhaHorizontal("Compra",preco_medio,clrMagenta); 
           
           if(tickEURUSD.last >= preco_medio && !be_ativado)
             {
              trade.PositionModify(PositionGetTicket(0),preco_entrada,preco_tp);
              be_ativado = true;
             }   
                             
          }
        if(be_ativado == false && PositionSelect("EURUSD") && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_SELL && PERIOD_M15)
          {
           double preco_entrada = PositionGetDouble(POSITION_PRICE_OPEN);
           double preco_sl      = PositionGetDouble(POSITION_SL);
           double preco_tp      = PositionGetDouble(POSITION_TP);
           double preco_medio   = (preco_entrada + preco_tp)/2;
           
           desenhaLinhaHorizontal("Compra",preco_medio,clrMagenta);
           
           if(tickEURUSD.last <= preco_medio && !be_ativado)
             {
              trade.PositionModify(PositionGetTicket(0),preco_entrada,preco_tp);
              be_ativado = true;
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
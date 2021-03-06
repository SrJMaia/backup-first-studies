//---

#property copyright "Your Holding"
#property version   "1.0"

/*

      Listas de Melhorias
      
   1.1 - 
   
*/

//---

#include <Modulos_EA.mqh>

//---

double TK                           = 700;                 
double SL                           = 600;               
double TK2                          = 1000;            
double SL2                          = 400;         
string inicio_op                    = "08:00";         
string fim_op                       = "22:00";            
int mm_solo_Handle;
double mm_solo_Buffer[];

//---

int magic_number = 106;

//---

MqlRates velas[];       
MqlTick tickEURUSD;    
MqlRates rates[];      

//---

int OnInit()
  {

   //---

   mm_solo_Handle   = iMA("EURUSD",PERIOD_M30,100,0,MODE_SMA,PRICE_CLOSE);
     
        if(mm_solo_Handle < 0)
     {
      Alert("Erro ao tentar criar Handles para o indicador - erro: ",GetLastError(),"!");
      return(-1);
     }
   
   CopyRates("EURUSD",PERIOD_M30,0,4,velas);
   
   ArraySetAsSeries(velas,true);
   ArraySetAsSeries(rates,true);
   
   //---

   return(INIT_SUCCEEDED);
   
  }

void OnDeinit(const int reason)
  {

   IndicatorRelease(mm_solo_Handle);
   
  }

bool be_ativado = false;

void OnTick()
  {
    
    //---
   
   if (CopyRates(_Symbol, _Period, 0, 3, rates)<0)
      {
         Alert("Erro ao obter as informações de MqlRates: ", GetLastError());
         return;
      }
   
    //---
   
    CopyBuffer(mm_solo_Handle,0,0,4,mm_solo_Buffer);
        
    //--- 
    
    CopyRates("EURUSD",PERIOD_M30,0,4,velas);
    
    ArraySetAsSeries(velas,true);
    
    //---

    ArraySetAsSeries(mm_solo_Buffer,true);
    
    //---
    
    SymbolInfoTick("EURUSD",tickEURUSD);
   
   //---
   
    bool compra_mm_solo = rates[0].close > mm_solo_Buffer[0] &&
                          rates[2].close < mm_solo_Buffer[2];
    
    bool venda_mm_solo  = mm_solo_Buffer[0] > rates[0].close &&
                          mm_solo_Buffer[2] < rates[2].close;               
                            
    //---
                               
    bool Comprar = false; 
    bool Vender  = false; 
      
   //---
   
   double loteM30;
   double porcentagemM15 = 0.75/100;
   double calcTesteM15 = (((AccountInfoDouble(ACCOUNT_BALANCE)*porcentagemM15)*500)/100000)/SymbolInfoDouble(_Symbol,SYMBOL_BID)/2;
   if(calcTesteM15 < 0.01)
     {
      loteM30 = 0.01;
     }else if(calcTesteM15 > 99.99)
             {
              loteM30 = 99.99;
             }else
               {
                loteM30 = (DoubleToString(calcTesteM15,2));
               }
   
   //---
   
    bool temosNovaVela = TemosNovaVela(); 

   //---

    if(temosNovaVela && inicioOperacao(inicio_op,fim_op))
      { 
        Comprar = compra_mm_solo;
        Vender = venda_mm_solo;
       if(Comprar && PositionSelect(_Symbol)==false && PositionsTotal() < 1000 &&
          (saberMesAno(TimeCurrent()) != 2 && saberMesAno(TimeCurrent()) != 5 && saberMesAno(TimeCurrent()) != 9 && 
           saberMesAno(TimeCurrent()) != 11) && PERIOD_M30)
         {
                    desenhaLinhaVertical("Compra",velas[1].time,clrBlue);
                    CompraAMercado(loteM30,tickEURUSD.ask,TK,SL);
                    be_ativado = false;
         }

       if(Vender && PositionSelect(_Symbol)==false && PositionsTotal() < 100 && 
          (saberMesAno(TimeCurrent()) != 1 && saberMesAno(TimeCurrent()) != 4 && saberMesAno(TimeCurrent()) != 6 && saberMesAno(TimeCurrent()) != 7 && 
           saberMesAno(TimeCurrent()) != 9 && saberMesAno(TimeCurrent()) != 10))
         {
                   desenhaLinhaVertical("Venda",velas[1].time,clrRed);
                   VendaAMercado(loteM30,tickEURUSD.bid,TK2,SL2);
                   be_ativado = false; 
         }
          
        if(be_ativado == false && PositionSelect(_Symbol) && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY && PERIOD_M30)
          {
           double preco_entrada = PositionGetDouble(POSITION_PRICE_OPEN);
           double preco_sl      = PositionGetDouble(POSITION_SL);
           double preco_tp      = PositionGetDouble(POSITION_TP);
           double preco_medio   = (preco_entrada + preco_tp)/2;
           double lote2         = loteM30/2;    
           
           desenhaLinhaHorizontal("Compra",preco_medio,clrMagenta); 
           
           if(tickEURUSD.last >= preco_medio && !be_ativado)
             {
              trade.PositionModify(PositionGetTicket(0),preco_entrada,preco_tp);
              trade.PositionClosePartial(PositionGetTicket(0),lote2,0);
              be_ativado = true;
             }   
                             
          }
        
        if(be_ativado == false && PositionSelect(_Symbol) && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_SELL && PERIOD_M30)
          {
           double preco_entrada = PositionGetDouble(POSITION_PRICE_OPEN);
           double preco_sl      = PositionGetDouble(POSITION_SL);
           double preco_tp      = PositionGetDouble(POSITION_TP);
           double preco_medio   = (preco_entrada + preco_tp)/2;
           double lote2         = loteM30/2;
           
           desenhaLinhaHorizontal("Compra",preco_medio,clrMagenta);
           
           if(tickEURUSD.last <= preco_medio && !be_ativado)
             {
              trade.PositionModify(PositionGetTicket(0),preco_entrada,preco_tp);
              trade.PositionClosePartial(PositionGetTicket(0),lote2,0);
              be_ativado = true;
             }       
          }  
      }
  }
  
//+------------------------------------------------------------------+
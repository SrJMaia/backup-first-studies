//---

#property copyright "Monter - M Holding - EURUSD D1"
#property version   "1.3"

/*

      Listas de Melhorias
      
   1.1 - Ajustado o lote, proporcional ao risco: Mais seguro
   1.2 - Ao realizar o Breakeven irá encerrar metade dos contratos ativos na posição modificada
   1.3 - Removidos algusn #include
   
*/

//---

#include <Modulos_EA.mqh>

//---

double TKCompraEURUSDD1             = 3000;        
double SLCompraEURUSDD1             = 1300;            
double TKVendaEURUSDD1              = 1200;          
double SLVendaEURUSDD1              = 1100;    
int mm_solo_EURUSD_D1_Handle;
double mm_solo_EURUSD_D1_Buffer[];   
    
//---

int magic_number = 101;

//---

MqlRates velas[];      
MqlTick tickEURUSD;           
MqlRates rates[];        

//---

int OnInit()
  {
  
   mm_solo_EURUSD_D1_Handle   = iMA("EURUSD",PERIOD_D1,200,0,MODE_SMA,PRICE_CLOSE);
   CopyRates("EURUSD",PERIOD_D1,0,4,velas);
   
           if(mm_solo_EURUSD_D1_Handle < 0)
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
      
  }

bool be_ativado = false;

void OnTick()
  {
   
   //---          
   
    SymbolInfoTick("EURUSD",tickEURUSD);
    
   //---

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
                          
   //---      

    ArraySetAsSeries(velas,true);
 
   //---
                         
    bool Comprar = false;
    bool Vender  = false;
      
   //---
   
   double loteD1;
   double porcentagemD1 = 1.5/100;
   double calcTesteD1 = (((AccountInfoDouble(ACCOUNT_BALANCE)*porcentagemD1)*500)/100000)/SymbolInfoDouble(_Symbol,SYMBOL_BID)/4;
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
   
   //---

    bool temosNovaVela = TemosNovaVela(); 
    
   //---              
   
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
           double lote2         = loteD1/2;
           
           desenhaLinhaHorizontal("Compra",preco_medio,clrMagenta);
           
           if(tickEURUSD.last <= preco_medio && !be_ativado)
             {
              trade.PositionModify(PositionGetTicket(0),preco_entrada,preco_tp);
              trade.PositionClosePartial(PositionGetTicket(0),lote2,0);
              be_ativado = true;
             }   
                             
          }
        
        if(be_ativado == false && PositionSelect("EURUSD") && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_SELL && PERIOD_D1)
          {
           double preco_entrada = PositionGetDouble(POSITION_PRICE_OPEN);
           double preco_sl      = PositionGetDouble(POSITION_SL);
           double preco_tp      = PositionGetDouble(POSITION_TP);
           double preco_medio   = (preco_entrada + preco_tp)/2;
           double lote2         = loteD1/2;
           
           desenhaLinhaHorizontal("Compra",preco_medio,clrMagenta);
           
           if(tickEURUSD.last <= preco_medio && !be_ativado)
             {
              trade.PositionModify(PositionGetTicket(0),preco_entrada,preco_tp);
              trade.PositionClosePartial(PositionGetTicket(0),lote2,0);
              be_ativado = true;
             }       
          }      
  }
   
//+------------------------------------------------------------------+
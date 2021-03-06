//---

#property copyright "Monter - M Holding - EURUSD D1"
#property version   "1.3"

/*

      Listas de Melhorias
      
   1.1 - Ajustado o lote, proporcional ao risco: Mais seguro
   1.2 - Ao realizar o Breakeven irá encerrar metade dos contratos ativos na posição modificada
   1.3 - Removidos algusn #include

*/

#include <Modulos_EA.mqh>
     
//---             

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


//---

int magic_number = 102;

//---

MqlRates velas[];      
MqlTick tickEURUSD;           
MqlRates rates[];   
     
//---

int OnInit()
  {

  //---           
  
   mm_solo_EURUSD_H1_Handle   = iMA("EURUSD",PERIOD_H1,100,0,MODE_SMA,PRICE_CLOSE);
   CopyRates("EURUSD",PERIOD_D1,0,4,velas);
       
        if(mm_solo_EURUSD_H1_Handle < 0)
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
   
   IndicatorRelease(mm_solo_EURUSD_H1_Handle);
      
  }

bool be_ativado = false;

void OnTick()
  {
   
   //---          
   
    SymbolInfoTick("EURUSD",tickEURUSD);

   //---          ~
   
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
                          
   //---

    ArraySetAsSeries(velas,true);
 
   //---
                         
    bool Comprar = false;
    bool Vender  = false;
      
   //---
               
   double loteH1;
   double porcentagemH1 = 1.0/100;
   double calcTesteH1 = (((AccountInfoDouble(ACCOUNT_BALANCE)*porcentagemH1)*500)/100000)/SymbolInfoDouble(_Symbol,SYMBOL_BID)*0.75;
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
   
   //---

    bool temosNovaVela = TemosNovaVela(); 
   
   //---      
   
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
           double lote2         = loteH1/2;
           
           desenhaLinhaHorizontal("Compra",preco_medio,clrMagenta);
           
           if(tickEURUSD.last <= preco_medio && !be_ativado)
             {
              trade.PositionModify(PositionGetTicket(0),preco_entrada,preco_tp);
              trade.PositionClosePartial(PositionGetTicket(0),lote2,0);
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
           double lote2         = loteH1/2;
           
           desenhaLinhaHorizontal("Compra",preco_medio,clrMagenta);
           
           if(tickEURUSD.last <= preco_medio && !be_ativado)
             {
              trade.PositionModify(PositionGetTicket(0),preco_entrada,preco_tp);
              trade.PositionClosePartial(PositionGetTicket(0),lote2,0);
              be_ativado = true;
             }       
          } 
  }
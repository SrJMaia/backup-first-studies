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

int magic_number = 103;

//---

MqlRates velas[];      
MqlTick tickEURUSD;           
MqlRates rates[];        

//---

int OnInit()
  {
  
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

   IndicatorRelease(mm_lenta_EURUSD_M15_Handle);
   IndicatorRelease(mm_rapida_EURUSD_M15_Handle);
      
  }

bool be_ativado = false;

void OnTick()
  {
   
    SymbolInfoTick("EURUSD",tickEURUSD);
   
   //---          
   
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
    
   double loteM15;
   double porcentagemM15 = 0.5/100;
   double calcTesteM15 = (((AccountInfoDouble(ACCOUNT_BALANCE)*porcentagemM15)*500)/100000)/SymbolInfoDouble(_Symbol,SYMBOL_BID)/2;
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
    
   //---           
   
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
           double lote2         = loteM15/2;
           
           desenhaLinhaHorizontal("Compra",preco_medio,clrMagenta);
           
           if(tickEURUSD.last <= preco_medio && !be_ativado)
             {
              trade.PositionModify(PositionGetTicket(0),preco_entrada,preco_tp);
              trade.PositionClosePartial(PositionGetTicket(0),lote2,0);
              be_ativado = true;
             }   
                             
          }
          
        if(be_ativado == false && PositionSelect("EURUSD") && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_SELL && PERIOD_M15)
          {
           double preco_entrada = PositionGetDouble(POSITION_PRICE_OPEN);
           double preco_sl      = PositionGetDouble(POSITION_SL);
           double preco_tp      = PositionGetDouble(POSITION_TP);
           double preco_medio   = (preco_entrada + preco_tp)/2;
           double lote2         = loteM15/2;
           
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
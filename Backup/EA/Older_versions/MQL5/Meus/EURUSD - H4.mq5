//---

#property copyright "Your Holding"
#property version   "1.0"

//---

#include <Modulos_EA.mqh>

//---

double TK                            = 1000;         
double SL                            = 1800;           
double TK2                           = 1000;           
double SL2                           = 400;           
string inicio_op                    = "08:00";             
string fim_op                       = "21:00";            

//---

int mm_rapida_Handle;     
double mm_rapida_Buffer[]; 

int mm_lenta_Handle;  
double mm_lenta_Buffer[]; 

int magic_number = 105;

MqlRates velas[];        
MqlTick tick;           
MqlRates rates[];           

int OnInit()
  {

   mm_rapida_Handle = iMA("EURUSD",PERIOD_H4,8,0,MODE_EMA,PRICE_CLOSE);
   mm_lenta_Handle  = iMA("EURUSD",PERIOD_H4,21,0,MODE_SMA,PRICE_CLOSE);
      
   if(mm_rapida_Handle<0 || mm_lenta_Handle<0)
     {
      Alert("Erro ao tentar criar Handles para o indicador - erro: ",GetLastError(),"!");
      return(-1);
     }

   CopyRates("EURUSD",PERIOD_H4,0,4,velas);
   
   ArraySetAsSeries(velas,true);
   ArraySetAsSeries(rates,true);

   return(INIT_SUCCEEDED);
   
  }

void OnDeinit(const int reason)
  {

   IndicatorRelease(mm_rapida_Handle);
   IndicatorRelease(mm_lenta_Handle);

  }

bool be_ativado = false;

void OnTick()
  {
//---
   
   if (CopyRates("EURUSD", PERIOD_H4, 0, 3, rates)<0)
      {
         Alert("Erro ao obter as informações de MqlRates: ", GetLastError());
         return;
      }
   
//---

    CopyBuffer(mm_rapida_Handle,0,0,4,mm_rapida_Buffer);
    CopyBuffer(mm_lenta_Handle,0,0,4,mm_lenta_Buffer);
        
    CopyRates("EURUSD",PERIOD_H4,0,4,velas);
    
    ArraySetAsSeries(velas,true);
    
    ArraySetAsSeries(mm_rapida_Buffer,true);
    ArraySetAsSeries(mm_lenta_Buffer,true);
    
    SymbolInfoTick("EURUSD",tick);
   
    bool compra_mm_cros = mm_rapida_Buffer[0] > mm_lenta_Buffer[0] &&
                          mm_rapida_Buffer[2] < mm_lenta_Buffer[2] ;
                                                 
    bool venda_mm_cros = mm_lenta_Buffer[0] > mm_rapida_Buffer[0] &&
                         mm_lenta_Buffer[2] < mm_rapida_Buffer[2];
      
   //---                                
                               
    bool Comprar = false; 
    bool Vender  = false;
      
   //---
   
   double loteH4;
   double porcentagemH4 = 1.25/100;
   double calcTesteH4 = (((AccountInfoDouble(ACCOUNT_BALANCE)*porcentagemH4)*500)/100000)/SymbolInfoDouble(_Symbol,SYMBOL_BID)/2;
   if(calcTesteH4 < 0.01)
     {
      loteH4 = 0.01;
     }else if(calcTesteH4 > 99.99)
             {
              loteH4 = 99.99;
             }else
               {
                loteH4 = (DoubleToString(calcTesteH4,2));
               }
   
   //---
     
    bool temosNovaVela = TemosNovaVela(); 
    
    if(temosNovaVela)
      { 
      
          Comprar = compra_mm_cros;
          Vender  = venda_mm_cros;
       
       if(Comprar && PositionSelect(_Symbol)==false && PositionsTotal() < 100 &&
         (saberMesAno(TimeCurrent()) != 6 && saberMesAno(TimeCurrent()) != 5 && saberMesAno(TimeCurrent()) != 2 && saberMesAno(TimeCurrent()) != 10 &&
          saberMesAno(TimeCurrent()) != 7 && saberMesAno(TimeCurrent()) != 8 && saberMesAno(TimeCurrent()) != 9 && saberMesAno(TimeCurrent()) != 11))
         {
                    desenhaLinhaVertical("Compra",velas[1].time,clrBlue);
                    CompraAMercado(loteH4,tick.ask,TK,SL);
                    be_ativado = false;
         }
       
       if(Vender && PositionSelect(_Symbol)==false && PositionsTotal() < 100  &&
          (saberMesAno(TimeCurrent()) != 4 && saberMesAno(TimeCurrent()) != 8 && saberMesAno(TimeCurrent()) != 12 && saberMesAno(TimeCurrent()) != 11 &&
           saberMesAno(TimeCurrent()) != 3 && saberMesAno(TimeCurrent()) != 1 && saberMesAno(TimeCurrent()) != 9))
         {
                   desenhaLinhaVertical("Venda",velas[1].time,clrRed);
                   VendaAMercado(loteH4,tick.bid,TK2,SL2);
                   be_ativado = false; 
         }
          
        //---Breakeven
        if(be_ativado == false && PositionSelect(_Symbol) && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY)
          {
           double preco_entrada = PositionGetDouble(POSITION_PRICE_OPEN);
           double preco_sl      = PositionGetDouble(POSITION_SL);
           double preco_tp      = PositionGetDouble(POSITION_TP);
           double preco_medio   = (preco_entrada + preco_tp)/2;    
           double lote2         = loteH4/2;
           
           desenhaLinhaHorizontal("Compra",preco_medio,clrMagenta);
           
           if(tick.last <= preco_medio && !be_ativado)
             {
              trade.PositionModify(PositionGetTicket(0),preco_entrada,preco_tp);
              trade.PositionClosePartial(PositionGetTicket(0),lote2,0);
              be_ativado = true;
             }   
                             
          }
        
        if(be_ativado == false && PositionSelect(_Symbol) && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_SELL)
          {
           double preco_entrada = PositionGetDouble(POSITION_PRICE_OPEN);
           double preco_sl      = PositionGetDouble(POSITION_SL);
           double preco_tp      = PositionGetDouble(POSITION_TP);
           double preco_medio   = (preco_entrada + preco_tp)/2;
           double lote2         = loteH4/2;
           
           desenhaLinhaHorizontal("Compra",preco_medio,clrMagenta);
           
           if(tick.last <= preco_medio && !be_ativado)
             {
              trade.PositionModify(PositionGetTicket(0),preco_entrada,preco_tp);
              trade.PositionClosePartial(PositionGetTicket(0),lote2,0);
              be_ativado = true;
             }       
          }  
      } 
  }
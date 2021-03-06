//+------------------------------------------------------------------+
//|                                                   Modulos_EA.mqh |
//|                                      Copyright 2020, Rafaelfvcs. |
//|                             https://analistasquant.wordpress.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2020, Rafaelfvcs."
#property link      "https://analistasquant.wordpress.com"
//+------------------------------------------------------------------+
#include <Trade/Trade.mqh>

//-------------------------------------------------------------------+
// Atenção: EA para fins APENAS didáticos!
// Isso aqui não confere orientação e/ou sugestão de investimentos!
// O autor não se responsabiliza pelo uso indevido deste material 
//-------------------------------------------------------------------+

CTrade trade;

double var_teste;

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
        }else
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
        }else
           {
            Print("Erro de execução... ", GetLastError());
            ResetLastError();
           }              
   
   }
//---
void FecharPosicao()
   {
   
      ulong ticket = PositionGetTicket(0);
      
      trade.PositionClose(ticket);
      
      if(trade.ResultRetcode() == 10009)
        {
            Print("Fechamento Executado com Sucesso!!");
        }else
           {
            Print("Erro de execução... ", GetLastError());
            ResetLastError();
           }  
   
   }


//+------------------------------------------------------------------+
//| FUNÇÕES PARA AUXILIAR NA VISUALIZAÇÃO DA ESTRATÉGIA              |
//+------------------------------------------------------------------+

void desenhaLinhaVertical(string nome, datetime dt, color cor = clrAliceBlue)
   {
      ObjectDelete(0,nome);
      ObjectCreate(0,nome,OBJ_VLINE,0,dt,0);
      ObjectSetInteger(0,nome,OBJPROP_COLOR,cor);
   }
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
      
      for(int i=1;i<=tn;i++)
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
   int saberDiaDaSemana(datetime d)
   {
      //0-dom, 1-seg, 2-ter, 3-qua, 5-qui, 6-sex, 7-sab
      MqlDateTime str;
      TimeToStruct(d,str);
      
      return str.day_of_week;
   }
   
      int saberAno(datetime d)
   {
      //0-dom, 1-seg, 2-ter, 3-qua, 5-qui, 6-sex, 7-sab
      MqlDateTime str;
      TimeToStruct(d,str);
      
      return str.year;
   }
   
      int saberMesAno(datetime d)
   {
      //0-dom, 1-seg, 2-ter, 3-qua, 5-qui, 6-sex, 7-sab
      MqlDateTime str;
      TimeToStruct(d,str);
      
      return str.mon;
   }
   
     bool inicioOperacao(string inicio_op, string fim_op)
   {
      bool resp = false;
      
      datetime tc = TimeCurrent();
      
      if( TimeToString(tc,TIME_MINUTES)  >= inicio_op &&  TimeToString(tc,TIME_MINUTES)  <= fim_op )
        {
         resp = true;
         
        }else
           {
            resp = false;
           }
   
      return resp;
   }
//---

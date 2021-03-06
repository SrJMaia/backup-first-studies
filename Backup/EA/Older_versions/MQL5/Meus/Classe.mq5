//+------------------------------------------------------------------+
//|                                                       Classe.mq5 |
//|                        Copyright 2020, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2020, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+



class CIndicator
  {
      
      // o que esta aqui dentro o usuario não tem acesos
      // Todo indicador tem seu handle e o buffer que no caso é o main
      protected:
         int handle;
         double main[];
      
      // É a parte publica, pshift seria o desvio do indicador
      public:
         double Main(int pshift = 0);
         void Release();     
         // o de baixo e o contrutor
         CIndicator(){Print("Construtor");} // Construtor
         ~CIndicator(){Print("Destruidor");} // destruidor
            
  };






int OnInit()
  {
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
   
  }
//+------------------------------------------------------------------+

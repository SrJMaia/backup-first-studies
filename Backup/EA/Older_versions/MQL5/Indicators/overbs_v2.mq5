#property copyright "Copyright 2021, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property  tester_indicator "overbs.ex5"
#property indicator_separate_window
#property indicator_buffers 1
#property indicator_plots   1
#include <Math\Stat\Normal.mqh>
//--- plot buffer
#property indicator_label1  "buffer"
#property indicator_type1   DRAW_LINE
#property indicator_color1  clrRed
#property indicator_style1  STYLE_SOLID
#property indicator_width1  1
//--- input parameters
input int      period=20;
//--- indicator buffers

double dataBuffer[];
double stdBuffer[];
double calcBuffer[];

int limit;
double calc1, calc2;

int OnInit()
  {
   SetIndexBuffer(0,dataBuffer,INDICATOR_DATA);
   SetIndexBuffer(1,stdBuffer,INDICATOR_CALCULATIONS);
   SetIndexBuffer(2,calcBuffer,INDICATOR_CALCULATIONS);
   
   SymbolSelect("EURUSD",true);
   SymbolSelect("EURCAD",true);
   SymbolSelect("EURAUD",true);
   SymbolSelect("EURGBP",true);
   SymbolSelect("EURCHF",true);
   SymbolSelect("EURNZD",true);
   SymbolSelect("EURJPY",true);

   SymbolSelect("GBPAUD",true);
   SymbolSelect("GBPCHF",true);
   SymbolSelect("GBPJPY",true);
   SymbolSelect("GBPCAD",true);
   SymbolSelect("GBPUSD",true);
   SymbolSelect("GBPNZD",true);

   SymbolSelect("USDCHF",true);
   SymbolSelect("USDJPY",true);
   SymbolSelect("AUDUSD",true);
   SymbolSelect("NZDUSD",true);
   SymbolSelect("USDCAD",true);

   SymbolSelect("AUDJPY",true);
   SymbolSelect("CADJPY",true);
   SymbolSelect("CHFJPY",true);
   SymbolSelect("NZDJPY",true);

   SymbolSelect("AUDCHF",true);
   SymbolSelect("CADCHF",true);
   SymbolSelect("NZDCHF",true);

   SymbolSelect("AUDNZD",true);
   SymbolSelect("NZDCAD",true);

   SymbolSelect("AUDCAD",true);
   
   return(INIT_SUCCEEDED);
  }
int OnCalculate(const int rates_total,
                const int prev_calculated,
                const datetime &time[],
                const double &open[],
                const double &high[],
                const double &low[],
                const double &close[],
                const long &tick_volume[],
                const long &volume[],
                const int &spread[])
  {

   int backstep = period;
   int rates_start = MathMax(0, prev_calculated - 1);
   for(int i = rates_start; i < rates_total && !_StopFlag; i++)
   {
      dataBuffer[i] = 0.0;
      stdBuffer[i] = 0.0;
      calcBuffer[i] = 0.0;
      
      calc1 = 0.0;
      calc2 = 0.0;
      
      if(i < backstep) continue;
      
      calcBuffer[i] = ((close[i] / close[i-1]) -1)*100;
      
      dataBuffer[i] = calcBuffer[i];      
   }
//--- return value of prev_calculated for next call
   return(rates_total);
  }
//+------------------------------------------------------------------+

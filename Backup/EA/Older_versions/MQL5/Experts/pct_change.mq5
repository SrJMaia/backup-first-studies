//+------------------------------------------------------------------+
//|                                                   pct_change.mq5 |
//|                        Copyright 2020, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2020, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property indicator_separate_window
#property indicator_buffers 2
#property indicator_plots   2
//--- plot test
#property indicator_label1  "test1"
#property indicator_type1   DRAW_LINE
#property indicator_color1  clrRed
#property indicator_style1  STYLE_SOLID
#property indicator_width1  1

#property indicator_label1  "test2"
#property indicator_type1   DRAW_LINE
#property indicator_color1  clrAqua
#property indicator_style1  STYLE_SOLID
#property indicator_width1  1
//--- indicator buffers
double testBuffer[];
double indiBuffer[];
int indiHandle;
int periodTest = 1;
//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- indicator buffers mapping
   SetIndexBuffer(0,testBuffer,INDICATOR_DATA);

   indiHandle = iCustom(NULL,PERIOD_CURRENT,"testeur.ex5",20);
   if(indiHandle == INVALID_HANDLE)
      return INIT_FAILED;
      
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Custom indicator iteration function                              |
//+------------------------------------------------------------------+
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
//---

   if(CopyBuffer(indiHandle,0,0,rates_total,indiBuffer) <= 0)
      return 0;

   int limit = prev_calculated-1;

   if(prev_calculated == 0)
     {
      limit=0;
     }
     
   for(int i=limit; i<rates_total; i++)
     {
      if(i<periodTest)
        {
         continue;
        }
      
        
      testBuffer[i] = indiBuffer[i];
      
      Comment(testBuffer[i]);
     }

//--- return value of prev_calculated for next call
   return(rates_total);
  }
//+------------------------------------------------------------------+

//+------------------------------------------------------------------+
//|                                                         file.mq5 |
//|                        Copyright 2020, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2020, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property indicator_chart_window
#property indicator_buffers 1
#property indicator_plots   1
//--- plot test
#property indicator_label1  "test"
#property indicator_type1   DRAW_NONE
#property indicator_color1  clrRed
#property indicator_style1  STYLE_SOLID
#property indicator_width1  1
//--- indicator buffers
double         testBuffer[];
double eurusdBuffer[];
int InpPeriod = 20;
//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- indicator buffers mapping
   SetIndexBuffer(0,testBuffer,INDICATOR_DATA);

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
   int rates_start = MathMax(0, prev_calculated - 1);
   int eurusd = iCustom("EURUSD",PERIOD_M1,"IndicatorgetData.ex5");
   CopyBuffer(eurusd,0,0,rates_total,eurusdBuffer);
   // Se o arquivo existe, excluir e depois criar
   int filehandle=FileOpen("file.csv",FILE_WRITE|FILE_CSV,";");
   for(int i = rates_start; i < rates_total; i++)
     {
      if(filehandle!=INVALID_HANDLE)
        {
         FileWrite(filehandle,eurusdBuffer[i]);
        }
      else
         Print("Operaзгo FileOpen falhou, erro ",GetLastError());
     }
   FileClose(filehandle);
   Print("FileOpen OK");
   return(rates_total);
  }
//+------------------------------------------------------------------+

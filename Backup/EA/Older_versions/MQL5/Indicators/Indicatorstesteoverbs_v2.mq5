//+------------------------------------------------------------------+
//|                                                      ProjectName |
//|                                      Copyright 2020, CompanyName |
//|                                       http://www.companyname.net |
//+------------------------------------------------------------------+
#property copyright "Copyright 2021, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property tester_indicator "Indicatorstesteoverbs.ex5"
#property indicator_chart_window

#define PLOTS_TOTAL 8
#define PAIRS_TOTAL 28

#property indicator_plots   PLOTS_TOTAL
#property indicator_buffers PLOTS_TOTAL + PAIRS_TOTAL

#property indicator_label1  "plotEurBuffer"
#property indicator_type1   DRAW_NONE

input int      period=20;

enum E_PAIRS
{
   EURUSD,
   EURGBP,
   EURCAD,
   EURAUD,
   EURCHF,
   EURNZD,
   EURJPY,
   GBPAUD,
   GBPCHF,
   GBPJPY,
   GBPCAD,
   GBPUSD,
   GBPNZD,
   USDCHF,
   USDJPY,
   AUDUSD,
   NZDUSD,
   USDCAD,
   AUDJPY,
   CADJPY,
   CHFJPY,
   NZDJPY,
   AUDCHF,
   CADCHF,
   NZDCHF,
   AUDNZD,
   NZDCAD,
   AUDCAD,
};

struct S_PAIR
{
   string Name;
   int    Handle;
   double Buffer[];
};

S_PAIR Pairs[PAIRS_TOTAL];

// Plot
double plotEurBuffer[];
double plotGbpBuffer[];
double plotUsdBuffer[];
double plotJpyBuffer[];
double plotChfBuffer[];
double plotNzdBuffer[];
double plotAudBuffer[];
double plotCadBuffer[];

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
int OnInit()
  {
   SetIndexBuffer(0,plotEurBuffer,INDICATOR_DATA);
   SetIndexBuffer(1,plotAudBuffer,INDICATOR_DATA);
   SetIndexBuffer(2,plotCadBuffer,INDICATOR_DATA);
   SetIndexBuffer(3,plotChfBuffer,INDICATOR_DATA);
   SetIndexBuffer(4,plotGbpBuffer,INDICATOR_DATA);
   SetIndexBuffer(5,plotJpyBuffer,INDICATOR_DATA);
   SetIndexBuffer(6,plotNzdBuffer,INDICATOR_DATA);
   SetIndexBuffer(7,plotUsdBuffer,INDICATOR_DATA);

   //---
   for (int i = 0; i < PAIRS_TOTAL; i++)
   {
      SetIndexBuffer(PLOTS_TOTAL+i, Pairs[i].Buffer, INDICATOR_CALCULATIONS);
      //ArraySetAsSeries(Pairs[i].Buffer,true);
      Pairs[i].Name = EnumToString((E_PAIRS)i);
      while (!SymbolSelect(Pairs[i].Name, true) && !SymbolIsSynchronized(Pairs[i].Name))
         Sleep(1000);
      Pairs[i].Handle = iCustom(Pairs[i].Name, PERIOD_CURRENT, "overbs_v2.ex5", period);
      if(Pairs[i].Handle == INVALID_HANDLE)
         return INIT_FAILED;
   }

   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
   Comment("");
}
//gbp = ['EURGBP','GBPAUD','GBPCHF','GBPJPY','GBPCAD','GBPUSD','GBPNZD']
//usd = ['GBPUSD','USDCHF','USDJPY','AUDUSD','NZDUSD','USDCAD','EURUSD']
//jpy = ['AUDJPY','CADJPY','CHFJPY','EURJPY','USDJPY','GBPJPY','NZDJPY']
//chf = ['AUDCHF','CADCHF','CHFJPY','USDCHF','EURCHF','GBPCHF','NZDCHF']
//nzd = ['AUDNZD','EURNZD','GBPNZD','NZDUSD','NZDCAD','NZDCHF','NZDJPY']
//aud = ['AUDCAD','AUDCHF','AUDJPY','AUDUSD','AUDNZD','EURAUD','GBPAUD']
//cad = ['AUDCAD','CADCHF','CADJPY','USDCAD','EURCAD','GBPCAD','NZDCAD']
//eur = ['EURGBP','EURUSD','EURJPY','EURCHF','EURNZD','EURAUD',]
//gbp = ['GBPAUD','GBPCHF','GBPJPY','GBPCAD','GBPUSD','GBPNZD']
//usd = ['USDCHF','USDJPY','AUDUSD','NZDUSD','USDCAD']
//jpy = ['AUDJPY','CADJPY','CHFJPY','NZDJPY']
//chf = ['AUDCHF','CADCHF','NZDCHF']
//nzd = ['AUDNZD','NZDCAD']
//aud = ['AUDCAD']

//+------------------------------------------------------------------+
//|                                                                  |
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
   FastCopyBuffer(Pairs[EURUSD].Handle, 0, rates_total, prev_calculated, Pairs[EURUSD].Buffer);
   FastCopyBuffer(Pairs[EURGBP].Handle, 0, rates_total, prev_calculated, Pairs[EURGBP].Buffer);
   FastCopyBuffer(Pairs[EURAUD].Handle, 0, rates_total, prev_calculated, Pairs[EURAUD].Buffer);
   FastCopyBuffer(Pairs[EURCAD].Handle, 0, rates_total, prev_calculated, Pairs[EURCAD].Buffer);
   FastCopyBuffer(Pairs[EURCHF].Handle, 0, rates_total, prev_calculated, Pairs[EURCHF].Buffer);
   FastCopyBuffer(Pairs[EURNZD].Handle, 0, rates_total, prev_calculated, Pairs[EURNZD].Buffer);
   FastCopyBuffer(Pairs[EURJPY].Handle, 0, rates_total, prev_calculated, Pairs[EURJPY].Buffer);
   FastCopyBuffer(Pairs[GBPAUD].Handle, 0, rates_total, prev_calculated, Pairs[GBPAUD].Buffer);
   FastCopyBuffer(Pairs[GBPCHF].Handle, 0, rates_total, prev_calculated, Pairs[GBPCHF].Buffer);
   FastCopyBuffer(Pairs[GBPJPY].Handle, 0, rates_total, prev_calculated, Pairs[GBPJPY].Buffer);
   FastCopyBuffer(Pairs[GBPCAD].Handle, 0, rates_total, prev_calculated, Pairs[GBPCAD].Buffer);
   FastCopyBuffer(Pairs[GBPUSD].Handle, 0, rates_total, prev_calculated, Pairs[GBPUSD].Buffer);
   FastCopyBuffer(Pairs[GBPNZD].Handle, 0, rates_total, prev_calculated, Pairs[GBPNZD].Buffer);
   FastCopyBuffer(Pairs[USDCHF].Handle, 0, rates_total, prev_calculated, Pairs[USDCHF].Buffer);
   FastCopyBuffer(Pairs[USDJPY].Handle, 0, rates_total, prev_calculated, Pairs[USDJPY].Buffer);
   FastCopyBuffer(Pairs[AUDUSD].Handle, 0, rates_total, prev_calculated, Pairs[AUDUSD].Buffer);
   FastCopyBuffer(Pairs[NZDUSD].Handle, 0, rates_total, prev_calculated, Pairs[NZDUSD].Buffer);
   FastCopyBuffer(Pairs[USDCAD].Handle, 0, rates_total, prev_calculated, Pairs[USDCAD].Buffer);
   FastCopyBuffer(Pairs[AUDJPY].Handle, 0, rates_total, prev_calculated, Pairs[AUDJPY].Buffer);
   FastCopyBuffer(Pairs[CADJPY].Handle, 0, rates_total, prev_calculated, Pairs[CADJPY].Buffer);
   FastCopyBuffer(Pairs[CHFJPY].Handle, 0, rates_total, prev_calculated, Pairs[CHFJPY].Buffer);
   FastCopyBuffer(Pairs[NZDJPY].Handle, 0, rates_total, prev_calculated, Pairs[NZDJPY].Buffer);
   FastCopyBuffer(Pairs[AUDCHF].Handle, 0, rates_total, prev_calculated, Pairs[AUDCHF].Buffer);
   FastCopyBuffer(Pairs[CADCHF].Handle, 0, rates_total, prev_calculated, Pairs[CADCHF].Buffer);
   FastCopyBuffer(Pairs[NZDCHF].Handle, 0, rates_total, prev_calculated, Pairs[NZDCHF].Buffer);
   FastCopyBuffer(Pairs[AUDNZD].Handle, 0, rates_total, prev_calculated, Pairs[AUDNZD].Buffer);
   FastCopyBuffer(Pairs[NZDCAD].Handle, 0, rates_total, prev_calculated, Pairs[NZDCAD].Buffer);
   FastCopyBuffer(Pairs[AUDCAD].Handle, 0, rates_total, prev_calculated, Pairs[AUDCAD].Buffer);

   //int backstep = 1;
   int backstep = rates_total - MathMin(GetMinPeriod(), rates_total);
   backstep++;
   int rates_start = MathMax(0, prev_calculated - 1);
   for(int i = rates_start; i < rates_total; i++)
     {
      plotAudBuffer[i] = 0.0;
      plotCadBuffer[i] = 0.0;
      plotChfBuffer[i] = 0.0;
      plotEurBuffer[i] = 0.0;
      plotGbpBuffer[i] = 0.0;
      plotJpyBuffer[i] = 0.0;
      plotNzdBuffer[i] = 0.0;
      plotUsdBuffer[i] = 0.0;

      if(i < backstep) continue;

      plotEurBuffer[i] = NormalizeDouble((Pairs[EURUSD].Buffer[i] + Pairs[EURGBP].Buffer[i] + Pairs[EURAUD].Buffer[i] + Pairs[EURCAD].Buffer[i] +
                                         Pairs[EURCHF].Buffer[i] + Pairs[EURNZD].Buffer[i] + Pairs[EURJPY].Buffer[i]) * 100,0);;

      plotGbpBuffer[i] = NormalizeDouble((Pairs[EURGBP].Buffer[i] + Pairs[GBPAUD].Buffer[i] + Pairs[GBPCHF].Buffer[i] + Pairs[GBPJPY].Buffer[i] +
                                         Pairs[GBPCAD].Buffer[i] + Pairs[GBPUSD].Buffer[i] + Pairs[GBPNZD].Buffer[i]) * 100,0);   

      plotUsdBuffer[i] = NormalizeDouble((Pairs[GBPUSD].Buffer[i] + Pairs[USDCHF].Buffer[i] + Pairs[USDJPY].Buffer[i] + Pairs[AUDUSD].Buffer[i] +
                                         Pairs[NZDUSD].Buffer[i] + Pairs[USDCAD].Buffer[i] + Pairs[EURUSD].Buffer[i]) * 100,0);

      plotJpyBuffer[i] = NormalizeDouble((Pairs[AUDJPY].Buffer[i] + Pairs[CADJPY].Buffer[i] + Pairs[CHFJPY].Buffer[i] + Pairs[EURJPY].Buffer[i] +
                                         Pairs[USDJPY].Buffer[i] + Pairs[GBPJPY].Buffer[i] + Pairs[NZDJPY].Buffer[i]) * 100,0);                                                                                  

      plotChfBuffer[i] = NormalizeDouble((Pairs[AUDCHF].Buffer[i] + Pairs[CADCHF].Buffer[i] + Pairs[CHFJPY].Buffer[i] + Pairs[USDCHF].Buffer[i] +
                                         Pairs[EURCHF].Buffer[i] + Pairs[GBPCHF].Buffer[i] + Pairs[NZDCHF].Buffer[i]) * 100,0);

      plotNzdBuffer[i] = NormalizeDouble((Pairs[AUDNZD].Buffer[i] + Pairs[EURNZD].Buffer[i] + Pairs[GBPNZD].Buffer[i] + Pairs[NZDUSD].Buffer[i] +
                                         Pairs[NZDCAD].Buffer[i] + Pairs[NZDCHF].Buffer[i] + Pairs[NZDJPY].Buffer[i]) * 100,0);   

      plotAudBuffer[i] = NormalizeDouble((Pairs[AUDCAD].Buffer[i] + Pairs[AUDCHF].Buffer[i] + Pairs[AUDJPY].Buffer[i] + Pairs[AUDUSD].Buffer[i] +
                                         Pairs[AUDNZD].Buffer[i] + Pairs[EURAUD].Buffer[i] + Pairs[GBPAUD].Buffer[i]) * 100,0);

      plotCadBuffer[i] = NormalizeDouble((Pairs[AUDCAD].Buffer[i] + Pairs[CADCHF].Buffer[i] + Pairs[CADJPY].Buffer[i] + Pairs[USDCAD].Buffer[i] +
                                         Pairs[EURCAD].Buffer[i] + Pairs[GBPCAD].Buffer[i] + Pairs[NZDCAD].Buffer[i]) * 100,0);   

      Comment("EUR | Anterior: " + DoubleToString(plotEurBuffer[i-1],0) + " Atual: " + DoubleToString(plotEurBuffer[i],0)
              + "\n" +
              "GBP | Anterior: " + DoubleToString(plotGbpBuffer[i-1],0) + " Atual: " + DoubleToString(plotGbpBuffer[i],0)
              + "\n" + 
              "USD | Anterior: " + DoubleToString(plotUsdBuffer[i-1],0) + " Atual: " + DoubleToString(plotUsdBuffer[i],0)
              + "\n" +
              "JPY | Anterior: " + DoubleToString(plotJpyBuffer[i-1],0) + " Atual: " + DoubleToString(plotJpyBuffer[i],0)
              + "\n" +
              "CHF | Anterior: " + DoubleToString(plotChfBuffer[i-1],0) + " Atual: " + DoubleToString(plotChfBuffer[i],0)
              + "\n" +
              "NZD | Anterior: " + DoubleToString(plotNzdBuffer[i-1],0) + " Atual: " + DoubleToString(plotNzdBuffer[i],0)
              + "\n" + 
              "AUD | Anterior: " + DoubleToString(plotAudBuffer[i-1],0) + " Atual: " + DoubleToString(plotAudBuffer[i],0)
              + "\n" +
              "CAD | Anterior: " + DoubleToString(plotCadBuffer[i-1],0) + " Atual: " + DoubleToString(plotCadBuffer[i],0)
              );
      
     }
   return(rates_total);
  }
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
int FastCopyBuffer(int    handle,
                   int    buffer_num,
                   int    rates_total,
                   int    prev_calculated,
                   double &buffer[])
{
   int count  = rates_total - prev_calculated;
   count      = prev_calculated == 0 ? count : count + 1;
   ResetLastError();
   int copied = CopyBuffer(handle, buffer_num, 0, count, buffer);
   if (copied == -1)
      PrintFormat("Error code %d in CopyBuffer!", GetLastError());
   return copied;
} 
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
int FastCopyBuffer(bool            reload,
                   int             handle,
                   int             buffer_num,
                   double          &buffer[],
                   string          symbol    = NULL,
                   ENUM_TIMEFRAMES timeframe = PERIOD_CURRENT)
{
   int rates_total     = Bars(symbol, timeframe);
   int prev_calculated = ArraySize(buffer);
   int count           = rates_total - prev_calculated;
   count               = prev_calculated == 0 ? count : count + 1;
   ResetLastError();
   int copied = CopyBuffer(handle, buffer_num, 0, count, buffer);
   if (copied == -1) {
      PrintFormat("Error code %d in CopyBuffer!", GetLastError());
      //Print("Handle: ", handle, " Buffer: ", buffer_num, " Count: ", count, " Total: ", rates_total, " Calculated: ", prev_calculated);
   }
   return copied;
}
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
int GetMinPeriod()
{
   int min = INT_MAX;
   for (int i = 0; i < ArraySize(Pairs); i++)
   {
      min = MathMin(min, ArraySize(Pairs[i].Buffer));
   }
   return min;
}
//+------------------------------------------------------------------+

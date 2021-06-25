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
#property indicator_buffers 1
#property indicator_plots   1

#property indicator_label1  "plotEurBuffer"
#property indicator_type1   DRAW_NONE

input int      period=20;

// Plot
double plotEurBuffer[];

// EUR
double eurusdBuffer[];
double eurgbpBuffer[];
double eurcadBuffer[];
double euraudBuffer[];
double eurchfBuffer[];
double eurnzdBuffer[];
double eurjpyBuffer[];

// EUR
int eurusd = INVALID_HANDLE;
int eurgbp = INVALID_HANDLE;
int euraud = INVALID_HANDLE;
int eurcad = INVALID_HANDLE;
int eurchf = INVALID_HANDLE;
int eurnzd = INVALID_HANDLE;
int eurjpy = INVALID_HANDLE;

int a1,a2,a3,a4,a5,a6;
int final_result;

int limit;
int new_prev;



//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
int OnInit()
  {

   SetIndexBuffer(0,plotEurBuffer,INDICATOR_DATA);

   SymbolSelect("EURUSD",true);
   SymbolSelect("EURCAD",true);
   SymbolSelect("EURAUD",true);
   SymbolSelect("EURGBP",true);
   SymbolSelect("EURCHF",true);
   SymbolSelect("EURNZD",true);
   SymbolSelect("EURJPY",true);

   eurusd = iCustom("EURUSD",PERIOD_CURRENT,"overbs.ex5",period);
   if(eurusd == INVALID_HANDLE)
      return INIT_FAILED;
   eurgbp = iCustom("EURGBP",PERIOD_CURRENT,"overbs.ex5",period);
   if(eurgbp == INVALID_HANDLE)
      return INIT_FAILED;
   euraud = iCustom("EURAUD",PERIOD_CURRENT,"overbs.ex5",period);
   if(euraud == INVALID_HANDLE)
      return INIT_FAILED;
   eurcad = iCustom("EURCAD",PERIOD_CURRENT,"overbs.ex5",period);
   if(eurcad == INVALID_HANDLE)
      return INIT_FAILED;
   eurchf = iCustom("EURCHF",PERIOD_CURRENT,"overbs.ex5",period);
   if(eurchf == INVALID_HANDLE)
      return INIT_FAILED;
   eurnzd = iCustom("EURNZD",PERIOD_CURRENT,"overbs.ex5",period);
   if(eurnzd == INVALID_HANDLE)
      return INIT_FAILED;
   eurjpy = iCustom("EURJPY",PERIOD_CURRENT,"overbs.ex5",period);
   if(eurjpy == INVALID_HANDLE)
      return INIT_FAILED;

   return(INIT_SUCCEEDED);
  }

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
//---

   new_prev = 0;

   if(CopyBuffer(eurusd,0,0,rates_total,eurusdBuffer) <= 0)
      return 0;
   if(CopyBuffer(eurgbp,0,0,rates_total,eurgbpBuffer) <= 0)
      return 0;
   if(CopyBuffer(euraud,0,0,rates_total,euraudBuffer) <= 0)
      return 0;
   if(CopyBuffer(eurcad,0,0,rates_total,eurcadBuffer) <= 0)
      return 0;
   if(CopyBuffer(eurchf,0,0,rates_total,eurchfBuffer) <= 0)
      return 0;
   if(CopyBuffer(eurnzd,0,0,rates_total,eurnzdBuffer) <= 0)
      return 0;
   if(CopyBuffer(eurjpy,0,0,rates_total,eurjpyBuffer) <= 0)
      return 0;

   a1 = MathMin(ArraySize(eurusdBuffer),ArraySize(eurgbpBuffer)); // EURUSD E EURGBP
   a2 = MathMin(ArraySize(euraudBuffer),ArraySize(eurcadBuffer)); // EURAUD E EURCAD
   a3 = MathMin(ArraySize(eurchfBuffer),ArraySize(eurnzdBuffer)); // EURCHF E EURNZD
   a4 = MathMin(a1,a2);
   a5 = MathMin(a3,a4);
   a6 = MathMin(a5,ArraySize(eurjpyBuffer)); // EURJPY

   final_result = a6;

   new_prev = final_result;

   if(prev_calculated == 0)
      limit = 0;
   else
      limit = new_prev - 3;

   for(int i = limit; i < new_prev; i++)
     {
      if(i < 1)
         continue;

      plotEurBuffer[i] = 0.0;
      double test = NormalizeDouble(eurusdBuffer[i] + eurgbpBuffer[i] + euraudBuffer[i] + eurcadBuffer[i] +
                                    eurchfBuffer[i] + eurnzdBuffer[i] + eurjpyBuffer[i] * 100,0);
      plotEurBuffer[i] = test;

      Comment("EUR | Anterior: " + DoubleToString(plotEurBuffer[i-1],0) + " Atual: " + DoubleToString(plotEurBuffer[i],0));
      
     }
   return(rates_total);
  }
//+------------------------------------------------------------------+

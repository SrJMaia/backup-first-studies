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
#property indicator_buffers 8
#property indicator_plots   8

#property indicator_label1  "plotEurBuffer"
#property indicator_type1   DRAW_NONE

input int      period=20;

// Plot
double plotEurBuffer[];
double plotGbpBuffer[];
double plotUsdBuffer[];
double plotJpyBuffer[];
double plotChfBuffer[];
double plotNzdBuffer[];
double plotAudBuffer[];
double plotCadBuffer[];

// EUR
double eurusdBuffer[];
double eurgbpBuffer[];
double eurcadBuffer[];
double euraudBuffer[];
double eurchfBuffer[];
double eurnzdBuffer[];
double eurjpyBuffer[];

// GBP
double gbpaudBuffer[];
double gbpchfBuffer[];
double gbpjpyBuffer[];
double gbpcadBuffer[];
double gbpusdBuffer[];
double gbpnzdBuffer[];

// USD
double usdchfBuffer[];
double usdjpyBuffer[];
double audusdBuffer[];
double nzdusdBuffer[];
double usdcadBuffer[];

// JPY
double audjpyBuffer[];
double cadjpyBuffer[];
double chfjpyBuffer[];
double nzdjpyBuffer[];

// CHF
double audchfBuffer[];
double cadchfBuffer[];
double nzdchfBuffer[];

// NZD
double audnzdBuffer[];
double nzdcadBuffer[];

// AUD
double audcadBuffer[];

// CAD
// Already did it.

// EUR
int eurusd = INVALID_HANDLE;
int eurgbp = INVALID_HANDLE;
int euraud = INVALID_HANDLE;
int eurcad = INVALID_HANDLE;
int eurchf = INVALID_HANDLE;
int eurnzd = INVALID_HANDLE;
int eurjpy = INVALID_HANDLE;

// GBP
int gbpaud = INVALID_HANDLE;
int gbpchf = INVALID_HANDLE;
int gbpjpy = INVALID_HANDLE;
int gbpcad = INVALID_HANDLE;
int gbpusd = INVALID_HANDLE;
int gbpnzd = INVALID_HANDLE;

// USD
int usdchf = INVALID_HANDLE;
int usdjpy = INVALID_HANDLE;
int audusd = INVALID_HANDLE;
int nzdusd = INVALID_HANDLE;
int usdcad = INVALID_HANDLE;

// JPY
int audjpy = INVALID_HANDLE;
int cadjpy = INVALID_HANDLE;
int chfjpy = INVALID_HANDLE;
int nzdjpy = INVALID_HANDLE;

// CHF
int audchf = INVALID_HANDLE;
int cadchf = INVALID_HANDLE;
int nzdchf = INVALID_HANDLE;

// NZD
int audnzd = INVALID_HANDLE;
int nzdcad = INVALID_HANDLE;

// AUD
int audcad = INVALID_HANDLE;

// CAD
// Already did it.

int a1,a2,a3,a4,a5,a6;
int b1,b2,b3,b4,b5,b6;
int c1,c2,c3,c4,c5,c6;
int d1,d2,d3,d4,d5,d6;
int e1,e2,e3,e4,e5,e6;
int f1,f2,f3,f4,f5,f6;
int g1,g2,g3,g4,g5,g6;
int h1,h2,h3,h4,h5,h6;
int result1,result2,result3,result4,result5,result6,final_result;

int limit;
int new_prev;



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
   
   ArraySetAsSeries(eurusdBuffer,true);
   ArraySetAsSeries(eurgbpBuffer,true);
   ArraySetAsSeries(eurcadBuffer,true);
   ArraySetAsSeries(euraudBuffer,true);
   ArraySetAsSeries(eurchfBuffer,true);
   ArraySetAsSeries(eurnzdBuffer,true);
   ArraySetAsSeries(eurjpyBuffer,true);
   
   ArraySetAsSeries(gbpaudBuffer,true);
   ArraySetAsSeries(gbpchfBuffer,true);
   ArraySetAsSeries(gbpjpyBuffer,true);
   ArraySetAsSeries(gbpcadBuffer,true);
   ArraySetAsSeries(gbpusdBuffer,true);
   ArraySetAsSeries(gbpnzdBuffer,true);

   ArraySetAsSeries(usdchfBuffer,true);
   ArraySetAsSeries(usdjpyBuffer,true);
   ArraySetAsSeries(audusdBuffer,true);
   ArraySetAsSeries(nzdusdBuffer,true);
   ArraySetAsSeries(usdcadBuffer,true);

   ArraySetAsSeries(audjpyBuffer,true);
   ArraySetAsSeries(cadjpyBuffer,true);
   ArraySetAsSeries(chfjpyBuffer,true);
   ArraySetAsSeries(nzdjpyBuffer,true);

   ArraySetAsSeries(audchfBuffer,true);
   ArraySetAsSeries(cadchfBuffer,true);
   ArraySetAsSeries(nzdchfBuffer,true);

   ArraySetAsSeries(audnzdBuffer,true);
   ArraySetAsSeries(nzdcadBuffer,true);

   ArraySetAsSeries(audcadBuffer,true);

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

   gbpaud = iCustom("GBPAUD",PERIOD_CURRENT,"overbs.ex5",period);
   if(gbpaud == INVALID_HANDLE)
      return INIT_FAILED;
   gbpchf = iCustom("GBPCHF",PERIOD_CURRENT,"overbs.ex5",period);
   if(gbpchf == INVALID_HANDLE)
      return INIT_FAILED;
   gbpjpy = iCustom("GBPJPY",PERIOD_CURRENT,"overbs.ex5",period);
   if(gbpjpy == INVALID_HANDLE)
      return INIT_FAILED;
   gbpcad = iCustom("GBPCAD",PERIOD_CURRENT,"overbs.ex5",period);
   if(gbpcad == INVALID_HANDLE)
      return INIT_FAILED;
   gbpusd = iCustom("GBPUSD",PERIOD_CURRENT,"overbs.ex5",period);
   if(gbpusd == INVALID_HANDLE)
      return INIT_FAILED;
   gbpnzd = iCustom("GBPNZD",PERIOD_CURRENT,"overbs.ex5",period);
   if(gbpnzd == INVALID_HANDLE)
      return INIT_FAILED;

   usdchf = iCustom("USDCHF",PERIOD_CURRENT,"overbs.ex5",period);
   if(usdchf == INVALID_HANDLE)
      return INIT_FAILED;
   usdjpy = iCustom("USDJPY",PERIOD_CURRENT,"overbs.ex5",period);
   if(usdjpy == INVALID_HANDLE)
      return INIT_FAILED;
   audusd = iCustom("AUDUSD",PERIOD_CURRENT,"overbs.ex5",period);
   if(audusd == INVALID_HANDLE)
      return INIT_FAILED;
   nzdusd = iCustom("NZDUSD",PERIOD_CURRENT,"overbs.ex5",period);
   if(nzdusd == INVALID_HANDLE)
      return INIT_FAILED;
   usdcad = iCustom("USDCAD",PERIOD_CURRENT,"overbs.ex5",period);
   if(usdcad == INVALID_HANDLE)
      return INIT_FAILED;

   audjpy = iCustom("AUDJPY",PERIOD_CURRENT,"overbs.ex5",period);
   if(audjpy == INVALID_HANDLE)
      return INIT_FAILED;
   cadjpy = iCustom("CADJPY",PERIOD_CURRENT,"overbs.ex5",period);
   if(cadjpy == INVALID_HANDLE)
      return INIT_FAILED;
   chfjpy = iCustom("CHFJPY",PERIOD_CURRENT,"overbs.ex5",period);
   if(chfjpy == INVALID_HANDLE)
      return INIT_FAILED;
   nzdjpy = iCustom("NZDJPY",PERIOD_CURRENT,"overbs.ex5",period);
   if(usdcad == INVALID_HANDLE)
      return INIT_FAILED;

   audchf = iCustom("AUDCHF",PERIOD_CURRENT,"overbs.ex5",period);
   if(audchf == INVALID_HANDLE)
      return INIT_FAILED;
   cadchf = iCustom("CADCHF",PERIOD_CURRENT,"overbs.ex5",period);
   if(cadchf == INVALID_HANDLE)
      return INIT_FAILED;
   nzdchf = iCustom("NZDCHF",PERIOD_CURRENT,"overbs.ex5",period);
   if(nzdchf == INVALID_HANDLE)
      return INIT_FAILED;

   audnzd = iCustom("AUDNZD",PERIOD_CURRENT,"overbs.ex5",period);
   if(audnzd == INVALID_HANDLE)
      return INIT_FAILED;
   nzdcad = iCustom("NZDCAD",PERIOD_CURRENT,"overbs.ex5",period);
   if(nzdcad == INVALID_HANDLE)
      return INIT_FAILED;

   audcad = iCustom("AUDCAD",PERIOD_CURRENT,"overbs.ex5",period);
   if(audcad == INVALID_HANDLE)
      return INIT_FAILED;

   return(INIT_SUCCEEDED);
  }


//gbp = ['EURGBP','GBPAUD','GBPCHF','GBPJPY','GBPCAD','GBPUSD','GBPNZD']
//usd = ['GBPUSD','USDCHF','USDJPY','AUDUSD','NZDUSD','USDCAD','EURUSD']
//jpy = ['AUDJPY','CADJPY','CHFJPY','EURJPY','USDJPY','GBPJPY','NZDJPY']
//chf = ['AUDCHF','CADCHF','CHFJPY','USDCHF','EURCHF','GBPCHF','NZDCHF']
//nzd = ['AUDNZD','EURNZD','GBPNZD','NZDUSD','NZDCAD','NZDCHF','NZDJPY']
//aud = ['AUDCAD','AUDCHF','AUDJPY','AUDUSD','AUDNZD','EURAUD','GBPAUD']
//cad = ['AUDCAD','CADCHF','CADJPY','USDCAD','EURCAD','GBPCAD','NZDCAD']
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

   if(CopyBuffer(gbpaud,0,0,rates_total,gbpaudBuffer) <= 0)
      return 0;
   if(CopyBuffer(gbpchf,0,0,rates_total,gbpchfBuffer) <= 0)
      return 0;
   if(CopyBuffer(gbpjpy,0,0,rates_total,gbpjpyBuffer) <= 0)
      return 0;
   if(CopyBuffer(gbpcad,0,0,rates_total,gbpcadBuffer) <= 0)
      return 0;
   if(CopyBuffer(gbpusd,0,0,rates_total,gbpusdBuffer) <= 0)
      return 0;
   if(CopyBuffer(gbpnzd,0,0,rates_total,gbpnzdBuffer) <= 0)
      return 0;

   if(CopyBuffer(usdchf,0,0,rates_total,usdchfBuffer) <= 0)
      return 0;
   if(CopyBuffer(usdjpy,0,0,rates_total,usdjpyBuffer) <= 0)
      return 0;
   if(CopyBuffer(audusd,0,0,rates_total,audusdBuffer) <= 0)
      return 0;
   if(CopyBuffer(nzdusd,0,0,rates_total,nzdusdBuffer) <= 0)
      return 0;
   if(CopyBuffer(usdcad,0,0,rates_total,usdcadBuffer) <= 0)
      return 0;

   if(CopyBuffer(audjpy,0,0,rates_total,audjpyBuffer) <= 0)
      return 0;
   if(CopyBuffer(cadjpy,0,0,rates_total,cadjpyBuffer) <= 0)
      return 0;
   if(CopyBuffer(chfjpy,0,0,rates_total,chfjpyBuffer) <= 0)
      return 0;
   if(CopyBuffer(nzdjpy,0,0,rates_total,nzdjpyBuffer) <= 0)
      return 0;

   if(CopyBuffer(audchf,0,0,rates_total,audchfBuffer) <= 0)
      return 0;
   if(CopyBuffer(cadchf,0,0,rates_total,cadchfBuffer) <= 0)
      return 0;
   if(CopyBuffer(nzdchf,0,0,rates_total,nzdchfBuffer) <= 0)
      return 0;

   if(CopyBuffer(audnzd,0,0,rates_total,audnzdBuffer) <= 0)
      return 0;
   if(CopyBuffer(nzdcad,0,0,rates_total,nzdcadBuffer) <= 0)
      return 0;

   if(CopyBuffer(audcad,0,0,rates_total,audcadBuffer) <= 0)
      return 0;

   a1 = MathMin(ArraySize(eurusdBuffer),ArraySize(eurgbpBuffer)); // EURUSD E EURGBP
   a2 = MathMin(ArraySize(euraudBuffer),ArraySize(eurcadBuffer)); // EURAUD E EURCAD
   a3 = MathMin(ArraySize(eurchfBuffer),ArraySize(eurnzdBuffer)); // EURCHF E EURNZD
   a4 = MathMin(a1,a2);
   a5 = MathMin(a3,a4);
   a6 = MathMin(a5,ArraySize(eurjpyBuffer)); // EURJPY

   b1 = MathMin(ArraySize(eurgbpBuffer),ArraySize(gbpaudBuffer)); // EURGBP E GBPAUD
   b2 = MathMin(ArraySize(gbpchfBuffer),ArraySize(gbpjpyBuffer)); // GBPCHF E GBPJPY
   b3 = MathMin(ArraySize(gbpcadBuffer),ArraySize(gbpusdBuffer)); // GBPCAD E GBPUSD
   b4 = MathMin(b3,b4);
   b5 = MathMin(b1,b2);
   b6 = MathMin(b5,ArraySize(gbpnzdBuffer)); // GBPNZD

   c1 = MathMin(ArraySize(gbpusdBuffer),ArraySize(usdchfBuffer)); // GBPUSD E USDCHF
   c2 = MathMin(ArraySize(usdjpyBuffer),ArraySize(audusdBuffer)); // USDJPY E AUDUSD
   c3 = MathMin(ArraySize(nzdusdBuffer),ArraySize(usdcadBuffer)); // NZDUSD E USDCAD
   c4 = MathMin(c3,c4);
   c5 = MathMin(c1,c2);
   c6 = MathMin(c5,ArraySize(eurusdBuffer)); // EURUSD

   d1 = MathMin(ArraySize(audjpyBuffer),ArraySize(cadjpyBuffer)); // AUDJPY E CADJPY
   d2 = MathMin(ArraySize(chfjpyBuffer),ArraySize(eurjpyBuffer)); // CHFJPY E EURJPY
   d3 = MathMin(ArraySize(usdjpyBuffer),ArraySize(gbpjpyBuffer)); // USDJPY E GBPJPY
   d4 = MathMin(d1,d2);
   d5 = MathMin(d3,d4);
   d6 = MathMin(d5,ArraySize(nzdjpyBuffer)); // NZDJPY

   e1 = MathMin(ArraySize(audchfBuffer),ArraySize(cadchfBuffer)); // AUDCHF E CADCHF
   e2 = MathMin(ArraySize(chfjpyBuffer),ArraySize(usdchfBuffer)); // CHFJPY E USDCHF
   e3 = MathMin(ArraySize(eurchfBuffer),ArraySize(gbpchfBuffer)); // EURCHF E GBPCHF
   e4 = MathMin(e1,e2);
   e5 = MathMin(e3,e4);
   e6 = MathMin(e5,ArraySize(nzdchfBuffer)); // NZDCHF

   f1 = MathMin(ArraySize(audnzdBuffer),ArraySize(eurnzdBuffer)); // AUDNZD E EURNZD
   f2 = MathMin(ArraySize(gbpnzdBuffer),ArraySize(nzdusdBuffer)); // GBPNZD E NZDUSD
   f3 = MathMin(ArraySize(nzdcadBuffer),ArraySize(nzdchfBuffer)); // NZDCAD E NZDCHF
   f4 = MathMin(f1,f2);
   f5 = MathMin(f3,f4);
   f6 = MathMin(f5,ArraySize(nzdjpyBuffer)); // NZDJPY

   g1 = MathMin(ArraySize(audcadBuffer),ArraySize(audchfBuffer)); // AUDCAD E AUDCHF
   g2 = MathMin(ArraySize(audjpyBuffer),ArraySize(audusdBuffer)); // AUDJPY E AUDUSD
   g3 = MathMin(ArraySize(audnzdBuffer),ArraySize(euraudBuffer)); // AUDNZD E EURAUD
   g4 = MathMin(g1,g2);
   g5 = MathMin(g3,g4);
   g6 = MathMin(g5,ArraySize(gbpaudBuffer)); // GBPAUD

   h1 = MathMin(ArraySize(audcadBuffer),ArraySize(cadchfBuffer)); // AUDCAD E CADCHF
   h2 = MathMin(ArraySize(cadjpyBuffer),ArraySize(usdcadBuffer)); // CADJPY E USDCAD
   h3 = MathMin(ArraySize(eurcadBuffer),ArraySize(gbpcadBuffer)); // EURCAD E GBPCAD
   h4 = MathMin(h1,h2);
   h5 = MathMin(h3,h4);
   h6 = MathMin(h5,ArraySize(nzdcadBuffer)); // NZDCAD

   result1 = MathMin(a5,b5);
   result2 = MathMin(c5,d5);
   result3 = MathMin(e5,f5);
   result4 = MathMin(g5,h5);
   result5 = MathMin(result1,result2);
   result6 = MathMin(result3,result4);

   final_result = MathMin(result5,result6);

   new_prev = final_result;

   if(prev_calculated == 0)
      limit = 0;
   else
      limit = new_prev - 3;

   for(int i = limit; i < new_prev; i++)
     {
      if(i < 1)
         continue;

      plotAudBuffer[i] = 0.0;
      plotCadBuffer[i] = 0.0;
      plotChfBuffer[i] = 0.0;
      plotEurBuffer[i] = 0.0;
      plotGbpBuffer[i] = 0.0;
      plotJpyBuffer[i] = 0.0;
      plotNzdBuffer[i] = 0.0;
      plotUsdBuffer[i] = 0.0;

      plotEurBuffer[i] = NormalizeDouble(eurusdBuffer[i] + eurgbpBuffer[i] + euraudBuffer[i] + eurcadBuffer[i] +
                                         eurchfBuffer[i] + eurnzdBuffer[i] + eurjpyBuffer[i] * 1000,0);

      plotGbpBuffer[i] = NormalizeDouble(eurgbpBuffer[i] + gbpaudBuffer[i] + gbpchfBuffer[i] + gbpjpyBuffer[i] +
                                         gbpcadBuffer[i] + gbpusdBuffer[i] + gbpnzdBuffer[i] * 1000,0);   

      plotUsdBuffer[i] = NormalizeDouble(gbpusdBuffer[i] + usdchfBuffer[i] + usdjpyBuffer[i] + audusdBuffer[i] +
                                         nzdusdBuffer[i] + usdcadBuffer[i] + eurusdBuffer[i] * 1000,0);

      plotJpyBuffer[i] = NormalizeDouble(audjpyBuffer[i] + cadjpyBuffer[i] + chfjpyBuffer[i] + eurjpyBuffer[i] +
                                         usdjpyBuffer[i] + gbpjpyBuffer[i] + nzdjpyBuffer[i] * 1000,0);                                                                                  

      plotChfBuffer[i] = NormalizeDouble(audchfBuffer[i] + cadchfBuffer[i] + chfjpyBuffer[i] + usdchfBuffer[i] +
                                         eurchfBuffer[i] + gbpchfBuffer[i] + nzdchfBuffer[i] * 1000,0);

      plotNzdBuffer[i] = NormalizeDouble(audnzdBuffer[i] + eurnzdBuffer[i] + gbpnzdBuffer[i] + nzdusdBuffer[i] +
                                         nzdcadBuffer[i] + nzdchfBuffer[i] + nzdjpyBuffer[i] * 1000,0);   

      plotAudBuffer[i] = NormalizeDouble(audcadBuffer[i] + audchfBuffer[i] + audjpyBuffer[i] + audusdBuffer[i] +
                                         audnzdBuffer[i] + euraudBuffer[i] + gbpaudBuffer[i] * 1000,0);

      plotCadBuffer[i] = NormalizeDouble(audcadBuffer[i] + cadchfBuffer[i] + cadjpyBuffer[i] + usdcadBuffer[i] +
                                         eurcadBuffer[i] + gbpcadBuffer[i] + nzdcadBuffer[i] * 1000,0);   

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

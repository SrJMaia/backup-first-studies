//+------------------------------------------------------------------+
//|                                        Indicatorstesteoverbs.mq5 |
//|                        Copyright 2021, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2021, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property indicator_separate_window
#property indicator_buffers 1
#property indicator_plots   1
//--- plot
#property indicator_label1  "plotbuffer"
#property indicator_type1   DRAW_LINE
#property indicator_color1  clrRed
#property indicator_style1  STYLE_SOLID
#property indicator_width1  1
//--- input parameters
input int      period = 20;
//--- indicator buffers
double plotBuffer[];
double eurusdBuffer[];
double eurgbpBuffer[];
double eurcadBuffer[];
double euraudBuffer[];
double eurchfBuffer[];
double eurnzdBuffer[];
double eurjpyBuffer[];
// Handles de identificação dos indicadores
int eurusd = INVALID_HANDLE;
int eurcad = INVALID_HANDLE;
int euraud = INVALID_HANDLE;
int eurgbp = INVALID_HANDLE;
// limit para percorrer e limite para copiar do indicador
int limit;
//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit() {
//--- indicator buffers mapping
   SetIndexBuffer(0, plotBuffer, INDICATOR_DATA);
   SetIndexBuffer(1, eurusdBuffer, INDICATOR_CALCULATIONS);
   SetIndexBuffer(2, eurgbpBuffer, INDICATOR_CALCULATIONS);
   SetIndexBuffer(3, eurcadBuffer, INDICATOR_CALCULATIONS);
   SetIndexBuffer(4, euraudBuffer, INDICATOR_CALCULATIONS);
//---
   //SymbolSelect("EURUSD", true);
   //SymbolSelect("EURCAD", true);
   //SymbolSelect("EURAUD", true);
   //SymbolSelect("EURGBP", true);
//---
   eurusd = iMA("EURUSD", PERIOD_CURRENT, period, 0, MODE_SMA, PRICE_CLOSE);
   if(eurusd == INVALID_HANDLE)
      return INIT_FAILED;
   eurcad = iMA("EURCAD", PERIOD_CURRENT, period, 0, MODE_SMA, PRICE_CLOSE);
   if(eurcad == INVALID_HANDLE)
      return INIT_FAILED;
   euraud = iMA("EURAUD", PERIOD_CURRENT, period, 0, MODE_SMA, PRICE_CLOSE);
   if(euraud == INVALID_HANDLE)
      return INIT_FAILED;
   eurgbp = iMA("EURGBP", PERIOD_CURRENT, period, 0, MODE_SMA, PRICE_CLOSE);
   if(eurgbp == INVALID_HANDLE)
      return INIT_FAILED;
   return(INIT_SUCCEEDED);
}
//+------------------------------------------------------------------+
//| Custom indicator iteration function                              |
//+------------------------------------------------------------------+
int OnCalculate(const int rates_total, const int prev_calculated, const datetime &time[], const double &open[],
                const double &high[], const double &low[], const double &close[], const long &tick_volume[], const long &volume[], const int &spread[]) {
//---
   if(prev_calculated == 0) {
      limit       = 0;
   } else
      limit      = rates_total - 3;
   //---
   if(CopyBuffer(eurusd, 0, 0, rates_total, eurusdBuffer) <= 0) return 0;
   if(CopyBuffer(eurgbp, 0, 0, rates_total, eurgbpBuffer) <= 0) return 0;
   if(CopyBuffer(euraud, 0, 0, rates_total, euraudBuffer) <= 0) return 0;
   if(CopyBuffer(eurcad, 0, 0, rates_total, eurcadBuffer) <= 0) return 0;
   //---
   for(int i = limit; i < rates_total; i++) {
      plotBuffer[i] = 0.0;
      double calc = eurusdBuffer[i];
      plotBuffer[i] = calc;
      Comment(plotBuffer[i]);
   }
   return(rates_total);
}
//+------------------------------------------------------------------+

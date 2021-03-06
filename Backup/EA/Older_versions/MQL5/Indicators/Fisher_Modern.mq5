//+------------------------------------------------------------------+
//|                                                Fisher Modern.mq5 |
//|                              Copyright © 2020, Vladimir Karputov |
//|                     https://www.mql5.com/ru/market/product/43516 |
//+------------------------------------------------------------------+
#property copyright "Copyright © 2020, Vladimir Karputov"
#property link      "https://www.mql5.com/ru/market/product/43516"
#property version   "1.000"
#property indicator_separate_window
#property indicator_buffers 3
#property indicator_plots   1
//--- plot Fisher
#property indicator_label1  "Fisher"
#property indicator_type1   DRAW_COLOR_HISTOGRAM
#property indicator_color1  clrLime,clrRed
#property indicator_style1  STYLE_SOLID
#property indicator_width1  2
//--- input parameters
input int   Inp_ma_period  = 10; // Averaging period
//--- indicator buffers
double   FisherBuffer[];
double   FisherColor[];
double   IntermediateValue[];
//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- indicator buffers mapping
   SetIndexBuffer(0,FisherBuffer,INDICATOR_DATA);
   SetIndexBuffer(1,FisherColor,INDICATOR_COLOR_INDEX);
   SetIndexBuffer(2,IntermediateValue,INDICATOR_CALCULATIONS);
//--- set the accuracy of values to be displayed in the Data Window
   IndicatorSetInteger(INDICATOR_DIGITS,Digits()+1);
//--- set as an empty value 0
   PlotIndexSetDouble(0,PLOT_EMPTY_VALUE,0.0);
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
   if(rates_total<Inp_ma_period+3)
      return(0);
//---
   int limit=prev_calculated-1;
   if(prev_calculated==0)
     {
      limit=Inp_ma_period;
      for(int i=0; i<limit; i++)
        {
         FisherBuffer[i]=0.0;
         FisherColor[i]=0.0;
         IntermediateValue[i]=0.0;
        }
     }
   for(int i=limit; i<rates_total; i++)
     {
      double max_high            = high[ArrayMaximum(high,i,Inp_ma_period)];
      double min_low             = low[ArrayMinimum(low,i,Inp_ma_period)];
      double price               = (high[i]+low[i])/2.0;
      double intermediate_value  = (max_high-min_low==0.0)?0.0:0.33*2.0*((price-min_low)/(max_high-min_low)-0.5)+0.67*IntermediateValue[i-1];
      intermediate_value         = MathMin(MathMax(intermediate_value, -0.999), 0.999);
//---
      FisherBuffer[i]            = (1.0-intermediate_value==0.0)?0.0:0.5*MathLog((1.0+intermediate_value)/(1.0-intermediate_value))+0.5*FisherBuffer[i-1];
      
      if(FisherBuffer[i]<0.0)
         FisherColor[i]=1.0;
      else
         FisherColor[i]=0.0;
      IntermediateValue[i]=intermediate_value;
     }
//--- return value of prev_calculated for next call
   return(rates_total);
  }
//+------------------------------------------------------------------+

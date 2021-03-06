//+------------------------------------------------------------------+
//|                                                TestLibrary15.mq5 |
//|                        Copyright 2017, MetaQuotes Software Corp. |
//|                                              http://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Marcio Sales Santana"
#property link      ""
#property version   "1.0"
//--- Including the application class

int maxima_book = 0;
int minima_book = 0;

int pontosImportantes[];
int posicao_sell = 0;

int tamanho_ind = 5;

int qtd_buy_1_wdo_anterior = 0;
int qtd_sell_1_wdo_anterior = 0;

int qtd_buy_1_dol_anterior = 0;
int qtd_sell_1_dol_anterior = 0;

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit(void)
  {   
   if (_Symbol == "PETR4") {
      MarketBookAdd("PETR4");
   } else if (StringSubstr(_Symbol, 0, StringLen(_Symbol)-3) == "DOL") {
      MarketBookAdd("DOLJ20");
   } else if (StringSubstr(_Symbol, 0, StringLen(_Symbol)-3) == "WDO") {
//      MarketBookAdd("WDOJ20");
      MarketBookAdd("DOLJ20");
   } else if (StringSubstr(_Symbol, 0, StringLen(_Symbol)-3) == "IND") {
      MarketBookAdd("WINJ20");
      MarketBookAdd("INDJ20");
   } else if (StringSubstr(_Symbol, 0, StringLen(_Symbol)-3) == "WIN") { // WING19
      MarketBookAdd("WINJ20");
      MarketBookAdd("INDJ20");
   } else if (StringSubstr(_Symbol, 0, StringLen(_Symbol)-3) == "EP") { // EPZ19
      MarketBookAdd("EPH20");
      MarketBookAdd("MESH20");
   } else if (StringSubstr(_Symbol, 0, StringLen(_Symbol)-3) == "MES") { // MESZ19
      MarketBookAdd("EPH20");
      MarketBookAdd("MESH20");
   } else if (StringSubstr(_Symbol, 0, StringLen(_Symbol)-3) == "ENQ") { // MESZ19
   } else if (_Symbol == "EURUSD") { // MESZ19
   } else if (StringSubstr(_Symbol, 0, StringLen(_Symbol)-3) == "MNQ") { // MESZ19
   }   

//--- Initialization successful
   return(INIT_SUCCEEDED);
  }

void gravarPontoImportante(int &min, int &max) {
   bool achouPontoImportanteMin = false;
   bool achouPontoImportanteMax = false;
   for (int p = 0; p < ArraySize(pontosImportantes); p++) {
      if (pontosImportantes[p] == min) {
         achouPontoImportanteMin = true;
      }
      if (pontosImportantes[p] == max) {
         achouPontoImportanteMax = true;
      }
   }
   if (!achouPontoImportanteMin) {
      int tamanhoMin = ArraySize(pontosImportantes);
      ArrayResize(pontosImportantes,tamanhoMin+1);
      pontosImportantes[tamanhoMin] = min;
      long cid=ChartID();
      ResetLastError();
      if(!ObjectCreate(cid,"min_"+min,OBJ_HLINE,0,0,(double)min) || GetLastError()!=0)
         Print("Error creating object: ",GetLastError());
      else
         ChartRedraw(cid);
         
      ObjectSetInteger(cid,"min_"+min,OBJPROP_COLOR,clrRed);
   }
   if (!achouPontoImportanteMax) {
      int tamanhoMax = ArraySize(pontosImportantes);
      ArrayResize(pontosImportantes,tamanhoMax+1);
      pontosImportantes[tamanhoMax] = max;
      long cid=ChartID();
      ResetLastError();
      if(!ObjectCreate(cid,"max_"+max,OBJ_HLINE,0,0,(double)max) || GetLastError()!=0)
         Print("Error creating object: ",GetLastError());
      else
         ChartRedraw(cid);
         
      ObjectSetInteger(cid,"max_"+max,OBJPROP_COLOR,clrRed);
      
   }
}

//+------------------------------------------------------------------+
//| BookEvent function                                               |
//+------------------------------------------------------------------+
void OnBookEvent(const string &symbol) {
      //--- array of the DOM structures
      MqlBookInfo last_bookArray[];

      //--- get the book
      if(MarketBookGet(symbol,last_bookArray))
        {
         //--- process book data
         posicao_sell = 0;
         MqlBookInfo curr_info;
         for(int idx=0;(idx<ArraySize(last_bookArray));idx++) {
            curr_info=last_bookArray[idx];
            if (curr_info.type == BOOK_TYPE_BUY || curr_info.type == BOOK_TYPE_BUY_MARKET) {
               posicao_sell = idx;
               break;
            }
           }
           if (posicao_sell != 0) {

            double buy_1;
            int qtd_buy_1;

            double sell_1;
            int qtd_sell_1;
            
            curr_info=last_bookArray[posicao_sell];
            buy_1 = curr_info.price;
            qtd_buy_1 = curr_info.volume_real;

            // venda
            curr_info=last_bookArray[posicao_sell-1];
            sell_1 = curr_info.price;
            qtd_sell_1 = curr_info.volume_real;
            
            if (symbol == "PETR4") {
               minima_book = StringSubstr(buy_1,0,2) + "" + StringSubstr(DoubleToString(buy_1,2),3,2); // minima_book
               maxima_book = StringSubstr(sell_1,0,2) + "" + StringSubstr(DoubleToString(sell_1,2),3,2); // maxima_book
               //if (MathAbs(maxima_book - minima_book) > 10) {
                  //gravarPontoImportante(minima_book, maxima_book);
                  Alert("PETR4 = minima_book = ", minima_book, " maxima_book = ", maxima_book, " spread = ", MathAbs(maxima_book - minima_book));
               //}
            } else if (StringSubstr(symbol, 0, StringLen(symbol)-3) == "DOL") {
               minima_book = StringSubstr(DoubleToString(buy_1,2),0,4);
               maxima_book = StringSubstr(DoubleToString(sell_1,2),0,4);
               if (qtd_buy_1_dol_anterior == 0) {
                  qtd_buy_1_dol_anterior = qtd_buy_1 - 50;
               }
               if (qtd_sell_1_dol_anterior == 0) {
                  qtd_sell_1_dol_anterior = qtd_sell_1 - 50;
               }
               if ((MathAbs(maxima_book - minima_book) > 9) && (qtd_buy_1 > 5) && (qtd_sell_1 > 5) && 
                  ((MathAbs(qtd_buy_1_dol_anterior - qtd_buy_1) > 50) || (MathAbs(qtd_sell_1_dol_anterior - qtd_sell_1) > 50))) {
                  gravarPontoImportante(minima_book, maxima_book);
                  Alert("DOL = minima_book = ", minima_book, " maxima_book = ", maxima_book, " spread = ", MathAbs(maxima_book - minima_book));
                  qtd_buy_1_dol_anterior = qtd_buy_1;
                  qtd_sell_1_dol_anterior = qtd_sell_1;
               }
            } else if (StringSubstr(symbol, 0, StringLen(symbol)-3) == "WDO") {
               minima_book = StringSubstr(DoubleToString(buy_1,2),0,4);
               maxima_book = StringSubstr(DoubleToString(sell_1,2),0,4);
               if (qtd_buy_1_wdo_anterior == 0) {
                  qtd_buy_1_wdo_anterior = qtd_buy_1 - 20;
               }
               if (qtd_sell_1_wdo_anterior == 0) {
                  qtd_sell_1_wdo_anterior = qtd_sell_1 - 20;
               }
               if ((MathAbs(maxima_book - minima_book) > 9) && (qtd_buy_1 > 5) && (qtd_sell_1 > 5) && 
                  ((MathAbs(qtd_buy_1_wdo_anterior - qtd_buy_1) > 19) || (MathAbs(qtd_sell_1_wdo_anterior - qtd_sell_1) > 19))) {
                  //gravarPontoImportante(minima_book, maxima_book);
                  Alert("WDO = minima_book = ", minima_book, " maxima_book = ", maxima_book, " spread = ", MathAbs(maxima_book - minima_book));
                  qtd_buy_1_wdo_anterior = qtd_buy_1;
                  qtd_sell_1_wdo_anterior = qtd_sell_1;
               }
            } else if (StringSubstr(symbol, 0, StringLen(symbol)-3) == "IND") {
               minima_book = StringSubstr(buy_1,0,tamanho_ind);
               maxima_book = StringSubstr(sell_1,0,tamanho_ind);
               if (MathAbs(maxima_book - minima_book) > 150) {
                  gravarPontoImportante(minima_book, maxima_book);
                  //Alert("DOL = minima_book = ", minima_book, " maxima_book = ", maxima_book, " spread = ", MathAbs(maxima_book - minima_book));
               }
            } else if (StringSubstr(symbol, 0, StringLen(symbol)-3) == "WIN") {
               minima_book = StringSubstr(buy_1,0,tamanho_ind);
               maxima_book = StringSubstr(sell_1,0,tamanho_ind);
               if (MathAbs(maxima_book - minima_book) > 150) {
                  gravarPontoImportante(minima_book, maxima_book);
                  //Alert("DOL = minima_book = ", minima_book, " maxima_book = ", maxima_book, " spread = ", MathAbs(maxima_book - minima_book));
               }
            } else if (StringSubstr(symbol, 0, StringLen(symbol)-3) == "EP") { // EPZ19
               minima_book = StringSubstr(buy_1,0,4) + "" + StringSubstr(DoubleToString(buy_1,2),5,2);
               maxima_book = StringSubstr(sell_1,0,4) + "" + StringSubstr(DoubleToString(sell_1,2),5,2);
               gravarPontoImportante(minima_book, maxima_book);
            } else if (StringSubstr(symbol, 0, StringLen(symbol)-3) == "MES") { // MESZ19
               minima_book = StringSubstr(buy_1,0,4) + "" + StringSubstr(DoubleToString(buy_1,2),5,2);
               maxima_book = StringSubstr(sell_1,0,4) + "" + StringSubstr(DoubleToString(sell_1,2),5,2);
               gravarPontoImportante(minima_book, maxima_book);
            } else if (StringSubstr(symbol, 0, StringLen(symbol)-3) == "ENQ") { // MESZ19
               minima_book = StringSubstr(DoubleToString(buy_1,2),0,4);
               maxima_book = StringSubstr(DoubleToString(sell_1,2),0,4);
            } else if (StringSubstr(symbol, 0, StringLen(symbol)-3) == "MNQ") { // MESZ19
               minima_book = StringSubstr(DoubleToString(buy_1,2),0,4);
               maxima_book = StringSubstr(DoubleToString(sell_1,2),0,4);
            }
        }
      }
}


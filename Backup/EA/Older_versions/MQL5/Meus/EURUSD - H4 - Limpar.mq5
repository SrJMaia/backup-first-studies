//+------------------------------------------------------------------+
//|                                                                  |
//|                                                    MonstroV5.mq5 |
//|                                                                  |
//+------------------------------------------------------------------+
#property copyright "Your Holding"
#property version   "5.0"
//---
#include <Trade/Trade.mqh>
#include <Modulos_EA.mqh>
#include <expert/expertbase.mqh>
#include <trade/trade.mqh>
#include <indicators/indicators.mqh>
//---
enum LIGA
  {
   SIM,        // Sim
   NAO         // Não
  };
//---
enum ESTRATEGIA_ENTRADA
  {
   APENAS_MM,  // Apenas Médias Móveis
   MM_E_TEMA,    // Triple Exponencial & MM
   APENAS_UMA_MM // Fechamento acima da média
  };
//---
input group "-----Estratégia de Entrada-----"
input ESTRATEGIA_ENTRADA   estrategia      = APENAS_MM;            // Estratégia de Entrada Trader
input LIGA liga_breakeven                  = NAO;                  // Liga BreakEven
input LIGA liga_sl_movel                   = SIM;                  // Liga SL Movel
//---
input group "-----Parâmetros de Entrada MM Cruzamento-----"
input int mm_rapida_periodo                = 12;                   // Periodo Média Rápida
input int mm_lenta_periodo                 = 32;                   // Periodo Média Lenta
input ENUM_TIMEFRAMES mm_tempo_grafico     = PERIOD_CURRENT;       // Tempo Gráfico
input ENUM_MA_METHOD  mm_metodoRapida      = MODE_EMA;             // Método MM Rápida 
input ENUM_MA_METHOD  mm_metodoLenta       = MODE_EMA;             // Método MM Lenta
input ENUM_APPLIED_PRICE  mm_preco         = PRICE_CLOSE;          // Preço Aplicado
//---
input group "-----Parâmetros de Entrada TEMA-----"
input int tema_periodo                     = 12;                   // Periodo
input ENUM_TIMEFRAMES tema_tempo_grafico   = PERIOD_CURRENT;       // Tempo Gráfico
input ENUM_APPLIED_PRICE  tema_preco       = PRICE_CLOSE;          // Preço Aplicado
input group "-----Parâmetros de Entrada MM Solitária-----"
input int mm_solo                          = 32;                   // Periodo Média Solo
input ENUM_TIMEFRAMES mm_solo_tgrafico     = PERIOD_CURRENT;       // Tempo Gráfico
input ENUM_MA_METHOD  mm_metodoSolo        = MODE_EMA;             // Método MM Solo
input ENUM_APPLIED_PRICE  mm_solo_preco         = PRICE_CLOSE;          // Preço Aplicado
//---
input group "-----Gerenciamento-----"
//input double num_lots                      = 0.01;               // Número de Lotes
input double TK                            = 60;                   // Take Profit
input double SL                            = 30;                   // Stop Loss
input double TK2                           = 60;                   // Take Profit 2
input double SL2                           = 30;                   // Stop Loss 2
input int variavelDoLote                   = 10000;                // Valor a ser Dividido para obter o Lote
input double lote_parcial                  = 0.04;                 // Lote de saida parcial
input double divisorLote                   = 100000;               // Número para dividir capital para obter lote
input int posicoesEmAberto                 = 2;                    // Número Máximo de Ordens Simultâneas
//---
input group "-----Horários-----"
input string hora_limite_fecha_op         = "22:00";               // Horário Limite para Fechar Operação
input string inicio_op                    = "10:00";               // Hora de Inicio de Negociação
input string fim_op                       = "19:00";               //Hora de Fechamento de Negociação
input string inicio_op2                   = "10:00";               // Hora de Inicio de Negociação 2
input string fim_op2                      = "19:00";               //Hora de Fechamento de Negociação 2
//---
//+------------------------------------------------------------------+
//|  Variáveis para os indicadores                                   |
//+------------------------------------------------------------------+
//--- Médias Móveis
// RÁPIDA - menor período
int mm_rapida_Handle;      // Handle controlador da média móvel rápida
double mm_rapida_Buffer[]; // Buffer para armazenamento dos dados das médias

// LENTA - maior período
int mm_lenta_Handle;      // Handle controlador da média móvel lenta
double mm_lenta_Buffer[]; // Buffer para armazenamento dos dados das médias

// TEMA
int tema_Handle;
double tema_Buffer[];

// MM SOLO
int mm_solo_Handle;
double mm_solo_Buffer[];

int magic_number = 111;

//+------------------------------------------------------------------+
//| Variáveis para as funçoes                                        |
//+------------------------------------------------------------------+

MqlRates velas[];            // Variável para armazenar velas
MqlTick tick;                // Variável para armazenar ticks
MqlRates rates[];            // Variavel para armazenar preços

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//---
   mm_rapida_Handle = iMA(_Symbol,mm_tempo_grafico,mm_rapida_periodo,0,mm_metodoRapida,mm_preco);
   mm_lenta_Handle  = iMA(_Symbol,mm_tempo_grafico,mm_lenta_periodo,0,mm_metodoLenta,mm_preco);
   
   tema_Handle      = iTEMA(_Symbol,tema_tempo_grafico,tema_periodo,0,tema_preco);
   
   mm_solo_Handle   = iMA(_Symbol,mm_solo_tgrafico,mm_solo,0,mm_metodoSolo,mm_solo_preco);
      
   if(mm_rapida_Handle<0 || mm_lenta_Handle<0)
     {
      Alert("Erro ao tentar criar Handles para o indicador - erro: ",GetLastError(),"!");
      return(-1);
     }
    
    if(tema_Handle < 0)
     {
      Alert("Erro ao tentar criar Handles para o indicador - erro: ",GetLastError(),"!");
      return(-1);
     }
     
        if(mm_solo_Handle < 0)
     {
      Alert("Erro ao tentar criar Handles para o indicador - erro: ",GetLastError(),"!");
      return(-1);
     }
   
   CopyRates(_Symbol,_Period,0,4,velas);
   ArraySetAsSeries(velas,true);
   
   ArraySetAsSeries(rates,true);
   
   // Para adicionar no gráfico o indicador:
   ChartIndicatorAdd(0,0,mm_rapida_Handle); 
   ChartIndicatorAdd(0,0,mm_lenta_Handle);
   //
   ChartIndicatorAdd(0,0,tema_Handle);
   //
   ChartIndicatorAdd(0,0,tema_Handle);
   
   //---
   

   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//---
   IndicatorRelease(mm_rapida_Handle);
   IndicatorRelease(mm_lenta_Handle);
   
   IndicatorRelease(tema_Handle);
   
   IndicatorRelease(mm_solo_Handle);
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+

bool be_ativado = false;
bool PositionClosePartial = true;

void OnTick()
  {
//---
   
   if (CopyRates(_Symbol, _Period, 0, 3, rates)<0)
      {
         Alert("Erro ao obter as informações de MqlRates: ", GetLastError());
         return;
      }
   
//---
   //desenhaLinhaVertical("L1",tick.time,clrRed);
   // Copiar um vetor de dados tamanho três para o vetor mm_Buffer
    CopyBuffer(mm_rapida_Handle,0,0,4,mm_rapida_Buffer);
    CopyBuffer(mm_lenta_Handle,0,0,4,mm_lenta_Buffer);
    //
    CopyBuffer(tema_Handle,0,0,4,tema_Buffer);
    //
    CopyBuffer(mm_solo_Handle,0,0,4,mm_solo_Buffer);
        
    //--- Alimentar Buffers das Velas com dados:
    CopyRates(_Symbol,_Period,0,4,velas);
    ArraySetAsSeries(velas,true);
    
    // Ordenar o vetor de dados:
    ArraySetAsSeries(mm_rapida_Buffer,true);
    ArraySetAsSeries(mm_lenta_Buffer,true);
    //
    ArraySetAsSeries(tema_Buffer,true);
    //
    ArraySetAsSeries(mm_solo_Buffer,true);
    //---
    
    // Alimentar com dados variável de tick
    SymbolInfoTick(_Symbol,tick);
   
    // LOGICA PARA ATIVAR COMPRA 
    bool compra_mm_cros = mm_rapida_Buffer[0] > mm_lenta_Buffer[0] &&
                          mm_rapida_Buffer[2] < mm_lenta_Buffer[2] ;
                                                 
    // LÓGICA PARA ATIVAR VENDA
    bool venda_mm_cros = mm_lenta_Buffer[0] > mm_rapida_Buffer[0] &&
                         mm_lenta_Buffer[2] < mm_rapida_Buffer[2];
      
   //---
    bool compra_tema_cross = tema_Buffer[0] > mm_solo_Buffer[0] &&
                            tema_Buffer[2] < mm_solo_Buffer[2] ;
   
    bool venda_tema_cross  = mm_solo_Buffer[0] > tema_Buffer[0] &&
                            mm_solo_Buffer[2] < tema_Buffer[2] ;
          
   //---
    bool compra_mm_solo = rates[0].close > mm_solo_Buffer[0] &&
                          rates[2].close < mm_solo_Buffer[2];
    
    bool venda_mm_solo  = mm_solo_Buffer[0] > rates[0].close &&
                          mm_solo_Buffer[2] < rates[2].close;               
                            
                               
    bool Comprar = false; // Pode comprar?
    bool Vender  = false; // Pode vender?
    
    if(estrategia == APENAS_MM)
      {
       Comprar = compra_mm_cros;
       Vender  = venda_mm_cros;
      }else if(estrategia == MM_E_TEMA)
              {
               Comprar = compra_tema_cross;
               Vender = venda_tema_cross;
              }else if(estrategia == APENAS_UMA_MM)
                      {
                       Comprar = compra_mm_solo;
                       Vender = venda_mm_solo;                       
                      }
      
   //---
   
   double loteM15;
   double porcentagemM15 = 1.25/100;
   // Remover SymbolInfoDouble(_Symbol,SYMBOL_BID) para jpy e reduzir alavancagem para 100 ou conforme o SL
   double calcTesteM15 = (((AccountInfoDouble(ACCOUNT_BALANCE)*porcentagemM15)*500)/100000)/SymbolInfoDouble(_Symbol,SYMBOL_BID)/2;
   if(calcTesteM15 < 0.01)
     {
      loteM15 = 0.01;
     }else if(calcTesteM15 > 99.99)
             {
              loteM15 = 99.99;
             }else
               {
                loteM15 = (DoubleToString(calcTesteM15,2));
               }
   
   
   //---
   
     
   // retorna true se tivermos uma nova vela
    bool temosNovaVela = TemosNovaVela(); 
    
    // Toda vez que existir uma nova vela entrar nesse 'if'  
    if(temosNovaVela && inicioOperacao(inicio_op,fim_op))
      { 
       if(Comprar && PositionSelect(_Symbol)==false && PositionsTotal() < posicoesEmAberto &&
         (saberMesAno(TimeCurrent()) != 6 && saberMesAno(TimeCurrent()) != 5 && saberMesAno(TimeCurrent()) != 2 && saberMesAno(TimeCurrent()) != 10 &&
          saberMesAno(TimeCurrent()) != 7 && saberMesAno(TimeCurrent()) != 8 && saberMesAno(TimeCurrent()) != 9 && saberMesAno(TimeCurrent()) != 11))
         {
                    desenhaLinhaVertical("Compra",velas[1].time,clrBlue);
                    CompraAMercado(loteM15,tick.ask,TK,SL);
                    be_ativado = false;
         }
       
       // Condição de Venda:
       if(Vender && PositionSelect(_Symbol)==false && PositionsTotal() < posicoesEmAberto  &&
          (saberMesAno(TimeCurrent()) != 4 && saberMesAno(TimeCurrent()) != 8 && saberMesAno(TimeCurrent()) != 12 && saberMesAno(TimeCurrent()) != 11 &&
           saberMesAno(TimeCurrent()) != 3 && saberMesAno(TimeCurrent()) != 1 && saberMesAno(TimeCurrent()) != 9))
         {
                   desenhaLinhaVertical("Venda",velas[1].time,clrRed);
                   VendaAMercado(loteM15,tick.bid,TK2,SL2);
                   be_ativado = false; 
         }
          
        //---Breakeven
        if(liga_breakeven == SIM && PositionSelect(_Symbol) && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY)
          {
           double preco_entrada = PositionGetDouble(POSITION_PRICE_OPEN);
           double preco_sl      = PositionGetDouble(POSITION_SL);
           double preco_tp      = PositionGetDouble(POSITION_TP);
           double preco_medio   = (preco_entrada + preco_tp)/2;    
           
           desenhaLinhaHorizontal("Compra",preco_medio,clrMagenta); 
           
           if(tick.last >= preco_medio && !be_ativado)
             {
              trade.PositionModify(PositionGetTicket(0),preco_entrada,preco_tp);
              be_ativado = true;
             }   
                             
          }
        
        if(liga_breakeven == SIM && PositionSelect(_Symbol) && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_SELL)
          {
           double preco_entrada = PositionGetDouble(POSITION_PRICE_OPEN);
           double preco_sl      = PositionGetDouble(POSITION_SL);
           double preco_tp      = PositionGetDouble(POSITION_TP);
           double preco_medio   = (preco_entrada + preco_tp)/2;
           
           desenhaLinhaHorizontal("Compra",preco_medio,clrMagenta);
           
           if(tick.last <= preco_medio && !be_ativado)
             {
              trade.PositionModify(PositionGetTicket(0),preco_entrada,preco_tp);
              be_ativado = true;
             }       
          }  
          
             //--- STOP LOSS MOVEL
             
          if(liga_sl_movel == SIM && PositionSelect(_Symbol) && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY)
             {
              double preco_entrada = PositionGetDouble(POSITION_PRICE_OPEN);
              double preco_sl      = PositionGetDouble(POSITION_SL);
              double preco_tp      = PositionGetDouble(POSITION_TP);
              double novo_sl       = NormalizeDouble(tick.last-SL*_Point,_Digits);
               
              double dist_sl       = SL*_Point;
               
              if((tick.last - preco_sl) > dist_sl && preco_sl != novo_sl)
                 {
                  Print("Compra - SL atual = ", preco_sl, ", Novo = ", novo_sl, " , Preço de Entrada = ", preco_entrada);
                  trade.PositionModify(PositionGetTicket(0),novo_sl,preco_tp);
                 }
             }
             
           if(liga_sl_movel == SIM && PositionSelect(_Symbol) && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_SELL)
             {
              double preco_entrada = PositionGetDouble(POSITION_PRICE_OPEN);
              double preco_sl      = PositionGetDouble(POSITION_SL);
              double preco_tp      = PositionGetDouble(POSITION_TP);
              double novo_sl       = NormalizeDouble(tick.last+SL*_Point,_Digits);
               
              double dist_sl       = SL*_Point;
               
              if((preco_sl - tick.last) > dist_sl && preco_sl != novo_sl)
                 {
                  Print("Venda - SL atual = ", preco_sl, ", Novo = ", novo_sl, " , Preço de Entrada = ", preco_entrada);
                  trade.PositionModify(PositionGetTicket(0),novo_sl,preco_tp);
                 } 
             }  
      } 
  }
  
//+------------------------------------------------------------------+
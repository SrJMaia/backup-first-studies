//+------------------------------------------------------------------+
//|                                                  Robo_MM_IFR.mq5 |
//|                                             rafaelfvcs@gmail.com |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "rafaelfvcs@gmail.com"
#property link      "https://www.mql5.com"
#property version   "1.00"
//---
#include <Trade/Trade.mqh>
#include <Modulos_EA.mqh>
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
   APENAS_IFR, // Apenas IFR
   MM_E_IFR    // Médias mais IFR
  };
//---
input group "-----Estratégia de Entrada-----"
input ESTRATEGIA_ENTRADA   estrategia      = APENAS_MM;            // Estratégia de Entrada Trader
input LIGA liga_breakeven                  = NAO;                  // Liga BreakEven
input LIGA liga_sl_movel                   = SIM;                  // Liga SL Movel
//---
input group "-----Parâmetros de Entrada MM-----"
input int mm_rapida_periodo                = 12;                   // Periodo Média Rápida
input int mm_lenta_periodo                 = 32;                   // Periodo Média Lenta
input ENUM_TIMEFRAMES mm_tempo_grafico     = PERIOD_CURRENT;       // Tempo Gráfico
input ENUM_MA_METHOD  mm_metodoRapida      = MODE_EMA;             // Método MM Rápida 
input ENUM_MA_METHOD  mm_metodoLenta       = MODE_EMA;             // Método MM Lenta
input ENUM_APPLIED_PRICE  mm_preco         = PRICE_CLOSE;          // Preço Aplicado
//---
input group "-----Parâmetros de Entrada IFR-----"
input int ifr_periodo                      = 5;                    // Período IFR
input ENUM_TIMEFRAMES ifr_tempo_grafico    = PERIOD_CURRENT;       // Tempo Gráfico  
input ENUM_APPLIED_PRICE ifr_preco         = PRICE_CLOSE;          // Preço Aplicado
input int ifr_sobrecompra                  = 70;                   // Nível de Sobrecompra
input int ifr_sobrevenda                   = 30;                   // Nível de Sobrevenda
//---
input group "-----Gerenciamento-----"
input double num_lots                      = 0.01;                  // Número de Lotes
input double TK                            = 60;                   // Take Profit
input double SL                            = 30;                   // Stop Loss
input int posicoesEmAberto                 = 2;                    // Número Máximo de Ordens Simultâneas
//---
input group "-----Horários-----"
input string hora_limite_fecha_op         = "22:00";               // Horário Limite para Fechar Operação
input string inicio_op                    = "10:00";               // Hora de Inicio de Negociação
input string fim_op                       = "19:00";               //Hora de Fechamento de Negociação
//---
input group "-----Outros-----"
input int magic_number                    = 111;                   // Nº mágico do robo
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

//--- IFR
int ifr_Handle;           // Handle controlador para o IFR
double ifr_Buffer[];      // Buffer para armazenamento dos dados do IFR

//+------------------------------------------------------------------+
//| Variáveis para as funçoes                                        |
//+------------------------------------------------------------------+

MqlRates velas[];            // Variável para armazenar velas
MqlTick tick;                // variável para armazenar ticks 

//+------------------------------------------------------------------+
//| Classes Externas                                               |
//+------------------------------------------------------------------+

//CTrade trade;

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//---
   mm_rapida_Handle = iMA(_Symbol,mm_tempo_grafico,mm_rapida_periodo,0,mm_metodoRapida,mm_preco);
   mm_lenta_Handle  = iMA(_Symbol,mm_tempo_grafico,mm_lenta_periodo,0,mm_metodoLenta,mm_preco);
   
   ifr_Handle = iRSI(_Symbol,ifr_tempo_grafico,ifr_periodo,ifr_preco);
   
   if(mm_rapida_Handle<0 || mm_lenta_Handle<0 || ifr_Handle<0)
     {
      Alert("Erro ao tentar criar Handles para o indicador - erro: ",GetLastError(),"!");
      return(-1);
     }
   
   CopyRates(_Symbol,_Period,0,4,velas);
   ArraySetAsSeries(velas,true);
   
   // Para adicionar no gráfico o indicador:
   ChartIndicatorAdd(0,0,mm_rapida_Handle); 
   ChartIndicatorAdd(0,0,mm_lenta_Handle);
   ChartIndicatorAdd(0,1,ifr_Handle);
     
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
   IndicatorRelease(ifr_Handle);
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+

bool be_ativado = false;

void OnTick()
  {
//---
   //desenhaLinhaVertical("L1",tick.time,clrRed);
   // Copiar um vetor de dados tamanho três para o vetor mm_Buffer
    CopyBuffer(mm_rapida_Handle,0,0,4,mm_rapida_Buffer);
    CopyBuffer(mm_lenta_Handle,0,0,4,mm_lenta_Buffer);
    
    CopyBuffer(ifr_Handle,0,0,4,ifr_Buffer);
    
    //--- Alimentar Buffers das Velas com dados:
    CopyRates(_Symbol,_Period,0,4,velas);
    ArraySetAsSeries(velas,true);
    
    // Ordenar o vetor de dados:
    ArraySetAsSeries(mm_rapida_Buffer,true);
    ArraySetAsSeries(mm_lenta_Buffer,true);
    ArraySetAsSeries(ifr_Buffer,true);
    //---
    
    // Alimentar com dados variável de tick
    SymbolInfoTick(_Symbol,tick);
   
    // LOGICA PARA ATIVAR COMPRA 
    bool compra_mm_cros = mm_rapida_Buffer[0] > mm_lenta_Buffer[0] &&
                          mm_rapida_Buffer[2] < mm_lenta_Buffer[2] ;
                                             
    bool compra_ifr = ifr_Buffer[0] <= ifr_sobrevenda;
    
    // LÓGICA PARA ATIVAR VENDA
    bool venda_mm_cros = mm_lenta_Buffer[0] > mm_rapida_Buffer[0] &&
                         mm_lenta_Buffer[2] < mm_rapida_Buffer[2];
    
    bool venda_ifr = ifr_Buffer[0] >= ifr_sobrecompra;
   
   //---
    bool Comprar = false; // Pode comprar?
    bool Vender  = false; // Pode vender?
    
    if(estrategia == APENAS_MM)
      {
       Comprar = compra_mm_cros;
       Vender  = venda_mm_cros;
       
      }
    else if(estrategia == APENAS_IFR)
     {
        Comprar = compra_ifr;
        Vender  = venda_ifr;
     }
    else
      {
         Comprar = compra_mm_cros && compra_ifr;
         Vender  = venda_mm_cros && venda_ifr;
      } 
      
   //---
   

     
   // retorna true se tivermos uma nova vela
    bool temosNovaVela = TemosNovaVela(); 
    
    // Toda vez que existir uma nova vela entrar nesse 'if'
    if(temosNovaVela && inicioOperacao(inicio_op,fim_op))
      { 
       // Condição de Compra:
       if(Comprar && PositionSelect(_Symbol)==false && PositionsTotal() < posicoesEmAberto && 
          (saberDiaDaSemana(TimeCurrent()) == 2 || saberDiaDaSemana(TimeCurrent()) == 3 || saberDiaDaSemana(TimeCurrent()) == 4))
         {
          desenhaLinhaVertical("Compra",velas[1].time,clrBlue);
          CompraAMercado(num_lots,tick.ask,TK,SL);
          be_ativado = false;
         }
       
       // Condição de Venda:
       if(Vender && PositionSelect(_Symbol)==false && PositionsTotal() < posicoesEmAberto && 
          (saberDiaDaSemana(TimeCurrent()) == 2 || saberDiaDaSemana(TimeCurrent()) == 3 || saberDiaDaSemana(TimeCurrent()) == 4))
         {
          desenhaLinhaVertical("Venda",velas[1].time,clrRed);
          VendaAMercado(num_lots,tick.bid,TK,SL);
          be_ativado = false;
         }
       //---
       
      Print("Lucro Acumulado = ", LucroAcumulado());
        
         
        //---
        
        //---Breakeven
        if(liga_breakeven == SIM && PositionSelect(_Symbol) && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY)
          {
          //ARRUMAR ESSAS VARIAVEIS PRA PARTE GLOBAL!!!
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
    
    //---
     if(TimeToString(TimeCurrent(),TIME_MINUTES) == hora_limite_fecha_op && PositionSelect(_Symbol)==true)
        {
            Print("-----> Fim do Tempo Operacional: encerrar posições abertas!");
             
            FechaPosicao();
        }  
   
  }
//+------------------------------------------------------------------+
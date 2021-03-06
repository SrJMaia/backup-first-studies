//+------------------------------------------------------------------+
//|                                                      ProjectName |
//|                                      Copyright 2018, CompanyName |
//|                                       http://www.companyname.net |
//+------------------------------------------------------------------+
#property copyright "Copyright 2020, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
//---

#include <Trade\Trade.mqh>
CTrade trade;

enum ESTRATEGIA_ENTRADA
  {
   APENAS_MM, // Apneas Médias Móveis
  };

//---

input group "-----Estratégia de Entrada-----"
input ESTRATEGIA_ENTRADA estrategia = APENAS_MM;     // Estratégia de Entrada Trader

input group "-----Médias Móveis-----"

input int mm_rapida_periodo               = 21;             // Periodo Média Rápida Simples
input int mm_lenta_periodo                = 8;             // Periodo Média Lenta Exponencial
input ENUM_TIMEFRAMES mm_tempo_grafico    = PERIOD_CURRENT; // Tempo Gráfico
input ENUM_MA_METHOD  mm_metodo1          = MODE_SMA;       // Média Rapida
input ENUM_MA_METHOD  mm_metodo2          = MODE_EMA;       // Média Lenta
input ENUM_APPLIED_PRICE  mm_preco        = PRICE_CLOSE;    // Preço Aplicado

input group "-----Gerenciamento-----"
input double TK                           = 60;             // Take Profit
input double SL                           = 30;             // Stop Loss
input int posicoesEmAberto                = 2;              // Número Máximo de Ordens Simultâneas
input double lote                         = 0.01;           // Divisor de lote

input group "-----Horários-----"
input string hora_limite_fecha_op         = "22:00";        // Horário Limite para Fechar Operação
input int horaInicio = 10;                                  // Hora de Inicio de Negociação
input int horaFechamento = 19;                              // Hora de Fechamento de Negociação

input group "-----Outros-----"
input int magic_number                    = 111;         // Nº mágico do robo
//---

int mm_rapida_Handle;         // Handle Controlador da Média Movel Rapida
double mm_rapida_Buffer[];    // Buffer para Armazenamento dos dados das Médias

// Lenta - Maior Período
int mm_lenta_Handle;          // Handle Controlador da Média Móvel Lenta
double mm_lenta_Buffer[];     // Buffer para Armazenamento dos dados das Médias

//---


MqlRates velas[];             // Variável para armazenar velas
MqlTick tick;                 // Variável para armazenar ticks
MqlDateTime horaAtual;        // Hora atual

//---

int OnInit()
  {
//---

   mm_rapida_Handle  = iMA(_Symbol,mm_tempo_grafico,mm_rapida_periodo,0,mm_metodo1,mm_preco);
   mm_lenta_Handle   = iMA(_Symbol,mm_tempo_grafico,mm_lenta_periodo,0,mm_metodo2,mm_preco);

   CopyRates(_Symbol,_Period,0,4,velas);
   ArraySetAsSeries(velas,true);

// Para adicionar no gráfico o indicador:
   ChartIndicatorAdd(0,0,mm_rapida_Handle);
   ChartIndicatorAdd(0,0,mm_lenta_Handle);
   
//---

   if(horaInicio > horaFechamento)
     {
      Alert("Inconsistência de Horario de abertura e fechamento!");
      return(INIT_FAILED);
     }

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
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+

void OnTick()

  {
//---
//desenhaLinhaVertical("Li",tick.time,clrRed);
// Copiar um vetor de dados tamanho tr~es para o vetor mm_buffer
   CopyBuffer(mm_rapida_Handle,0,0,4,mm_rapida_Buffer);
   CopyBuffer(mm_lenta_Handle,0,0,4,mm_lenta_Buffer);

//---^Alimentar Buffers das velhas com dados;
   CopyRates(_Symbol,_Period,0,4,velas);
   ArraySetAsSeries(velas,true);

// Ordenar o vetor de dados
   ArraySetAsSeries(mm_rapida_Buffer,true);
   ArraySetAsSeries(mm_lenta_Buffer,true);
//---

// Alimentar com dados variável de tick
   SymbolInfoTick(_Symbol,tick);

// Logica para Ativar Compra
   bool compra_mm_cross = mm_rapida_Buffer[0] > mm_lenta_Buffer[0] &&
                          mm_rapida_Buffer[2] < mm_lenta_Buffer[2] ;

// Logica para Ativar Venda
   bool venda_mm_cross = mm_lenta_Buffer[0] > mm_rapida_Buffer[0] &&
                         mm_lenta_Buffer[2] < mm_rapida_Buffer[2] ;

//---
   bool Comprar = false;
   bool Vender = false;

   if(estrategia == APENAS_MM)
     {
      Comprar = compra_mm_cross;
      Vender = venda_mm_cross;
     }

//---
   
   
   
   if(horaNegociacao())
     {
      Comment("Dentro do Horário de Negociação!");
     }
   else
     {
      Comment("Fora do Horário de Negociação!");
     }

//---

     
//------------------------------------------------------------------------------------------------------------------------------------

// retornar true se tivermos uma nova vela
   bool temosNovaVela = TemosNovaVela();
// Toda vez que existir uma nova vela entrar nesse if
   if(temosNovaVela)
     {
      // Condição de Compra
      if(Vender && horaNegociacao() && PositionSelect(_Symbol)==false && PositionsTotal() < posicoesEmAberto)
        {

      desenhaLinhaVertical("Compra",velas[1].time,clrBlue);
      CompraAMercado();
        }
        
      if(Comprar && horaNegociacao() && PositionSelect(_Symbol)==false && PositionsTotal() < posicoesEmAberto)
        {

         desenhaLinhaVertical("Venda",velas[1].time,clrRed);
         VendaAMercado();
  
        }
        
     }

//---

   if(TimeToString(TimeCurrent(),TIME_MINUTES) == hora_limite_fecha_op && PositionSelect(_Symbol)==true)
     {
      Print("--------> Fim do Tempo Operacional: Encerrar posições abertas!");

      if(PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY)
        {
         FechaCompra();
        }
      else
         if(PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_SELL)
           {
            FechaVenda();
           }

     }


  }
  
//-------------------------------------------------------------------------------------------------
// FIM ON TICK
//-------------------------------------------------------------------------------------------------
//+------------------------------------------------------------------+
//| FUNÇÕES PARA AUXILIAR NA VISUALIZAÇÃO DA ESTRATÉGIA              |
//+------------------------------------------------------------------+

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void desenhaLinhaVertical(string nome, datetime dt, color cor = clrBlueViolet)
  {
   ObjectDelete(0,nome);
   ObjectCreate(0,nome,OBJ_VLINE,0,dt,0);
   ObjectSetInteger(0,nome,OBJPROP_COLOR,cor);
  }

//+------------------------------------------------------------------+
//| FUNÇÕES PARA ENVIO DE ORDENS                                     |
//+------------------------------------------------------------------+

// COMPRA A MERCADO

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+

 
  
void CompraAMercado() // deve ser na documentação ordem das variaveis
  {
   MqlTradeRequest requisicao;   // requisição
   MqlTradeResult resposta;      // resposta

   ZeroMemory(requisicao);
   ZeroMemory(resposta);

//--- Caracteristicas da ordem de Compra
   requisicao.action          = TRADE_ACTION_DEAL;                                  // Executa ordem a mercado
   requisicao.magic           = magic_number;                                       // Nº Mágico da Ordem
   requisicao.symbol          = _Symbol;                                            // Simbolo do Ativo
   requisicao.volume          = lote;                                             // Nº de Lotes
   requisicao.price           = NormalizeDouble(tick.ask,_Digits);                  // Preço para compra
   requisicao.sl              = NormalizeDouble(tick.ask - SL*_Point,_Digits);      // Preço SL
   requisicao.tp              = NormalizeDouble(tick.ask + TK*_Point,_Digits);      // Preço TP
   requisicao.deviation       = 0;                                                  // Desvio Permitido do Preço
   requisicao.type            = ORDER_TYPE_BUY;                                     // Tipo de Ordem
   requisicao.type_filling    = ORDER_FILLING_IOC;                                  // Tipo de Preenchimento da Ordem

//---
   OrderSend(requisicao,resposta);
//---
   if(resposta.retcode == 10008 || resposta.retcode == 10009)
     {
      Print("Ordem de Compra Executada com Sucesso!");
     }
   else
     {
      Print("Erro ao enviar Ordem de Compra. Erro =", GetLastError());
      ResetLastError();
     }
  }
  
  

// VENDA A MERCADO

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void VendaAMercado()
  {
   MqlTradeRequest requisicao;
   MqlTradeResult resposta;

   ZeroMemory(requisicao);
   ZeroMemory(resposta);

   requisicao.action          = TRADE_ACTION_DEAL;
   requisicao.magic           = magic_number;
   requisicao.symbol          = _Symbol;
   requisicao.volume          = lote;
   requisicao.price           = NormalizeDouble(tick.bid,_Digits);
   requisicao.sl              = NormalizeDouble(tick.bid + SL*_Point,_Digits);
   requisicao.tp              = NormalizeDouble(tick.bid - TK*_Point,_Digits);
   requisicao.deviation       = 0;
   requisicao.type            = ORDER_TYPE_SELL;
   requisicao.type_filling    = ORDER_FILLING_IOC;

   OrderSend(requisicao,resposta);

   if(resposta.retcode == 10008 || resposta.retcode == 10009)
     {
      Print("Ordem de Venda Executada com Sucesso!");
     }
   else
     {
      Print("Erro ao enviar Ordem de Venda. Erro = ", GetLastError());
      ResetLastError();
     }
  }

//---

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void FechaCompra()
  {
   MqlTradeRequest   requisicao;
   MqlTradeResult    resposta;

   ZeroMemory(requisicao);
   ZeroMemory(resposta);

   requisicao.action       = TRADE_ACTION_DEAL;
   requisicao.magic        = magic_number;
   requisicao.symbol       = _Symbol;
   requisicao.volume       = lote;
   requisicao.price        = 0;
   requisicao.type         = ORDER_TYPE_SELL;
   requisicao.type_filling = ORDER_FILLING_RETURN;

   OrderSend(requisicao,resposta);

   if(resposta.retcode == 10008 || resposta.retcode == 10009)
     {
      Print("Ordem de Venda executada com sucesso!");
     }
   else
     {
      Print("Erro ao enviar Ordem de Venda. Erro = ", GetLastError());
      ResetLastError();
     }
  }

//---

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void FechaVenda()
  {
   MqlTradeRequest   requisicao;
   MqlTradeResult    resposta;

   ZeroMemory(requisicao);
   ZeroMemory(resposta);

   requisicao.action       = TRADE_ACTION_DEAL;
   requisicao.magic        = magic_number;
   requisicao.symbol       = _Symbol;
   requisicao.volume       = lote;
   requisicao.price        = 0;
   requisicao.type         = ORDER_TYPE_BUY;
   requisicao.type_filling = ORDER_FILLING_RETURN;

   OrderSend(requisicao,resposta);

   if(resposta.retcode == 10008 || resposta.retcode == 10009)
     {
      Print("Ordem de Venda executada com sucesso!");
     }
   else
     {
      Print("Erro ao enviar Ordem de Venda. Erro = ",GetLastError());
      ResetLastError();
     }
  }

//---

// Para Mudança de Candle
bool TemosNovaVela()
  {
//--- memoriza o tempo de abertura da ultima vela numa variavel
   static datetime last_time=0;
//--- tempo atual
   datetime lastbar_time= (datetime) SeriesInfoInteger(Symbol(),Period(),SERIES_LASTBAR_DATE);

//--- se for a primeira chamada da função
   if(last_time==0)
     {
      //---atribuir valro temporal e sair
      last_time=lastbar_time;
      return(false);
     }

//--- se o tempo estiver diferente
   if(last_time!=lastbar_time)
     {
      //--- memorizar esse tempo e tornar true
      last_time=lastbar_time;
      return(true);
     }
//--- se passarmos desta linha, então a barra não é nova; retornar false
   return(false);
  }

//---

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool horaNegociacao()
  {
   TimeToStruct(TimeCurrent(), horaAtual);
   if(horaAtual.hour >= horaInicio && horaAtual.hour <= horaFechamento)
     {
      return true;
     }
   else
     {
      return false;
     }
   return false;
  }

//---



//+------------------------------------------------------------------+

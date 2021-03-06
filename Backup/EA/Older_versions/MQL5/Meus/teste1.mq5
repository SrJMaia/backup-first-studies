//+------------------------------------------------------------------+
//|                                                       teste1.mq5 |
//|                        Copyright 2020, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2020, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+

// Para adicionar comentarios
//+------------------------------------------------------------------+
//| // ou ctrl + . ou ctrl + ; ou /* */
// ctrl + ~ faz uma seleção virar comentario
// ctrl + ç faz inverte operação anterior
//+------------------------------------------------------------------+

//para importar uma biblioteca de terceiros
//#include <Charts/Chart.mqh>
//#include <Canvas/Charts/ChartCanvas.mqh>

//+------------------------------------------------------------------+
// Principais tipos de variaveis
//
// variavel nomeVariavel = valor; / variavel nomeVariavel; - valor igual a zero
//
// char - consome apenas 1 byte de memoria, valores no intervalo de -128 até 127
// short - consome 2 bytes de memoria, valores de -32.768 até 32.767
// int - consome 4 bytes de memoria, valores de -2.147.48.648 até 2.147.483.647
// uchar - consome 1 byte de memoria, valores positivos de 0 a 255
// ushort - consome 2 bytes de memoria, valores de 0 a 65.535
// uint - consome 4 bytes de memoria, valores positivos de 0 a 4.294.967.295
//
// Ponto flutuante - valores decimais (float e double) / A diferença é a capacidade de dados double > float
//
// Caracteres alfanumericos (string)
//
// logicos (bool) / true ou false
//
// datas (datetimes)
// D'aaaa.mm.dd hh:mm:ss'
// datetime exemplo = D'2020.04.15 00:00:00;
// datetime exemplo = D'2020.04.15 22; apenas a hora
// datetime exemplo = D'2020.04.15; apenas a data
//+------------------------------------------------------------------+
// Para declarar variaveis constantes devera declarar em cima da função oniti
#define PI 3.14
// $define NomeDeAlgo "nome" - não é necessario ;
//+------------------------------------------------------------------+
// Vetores - arrays
// Devera ser executado na função Ontimer - Exemplo esta la
//+------------------------------------------------------------------+
// laço de repetição
// Pode começar em um numero grande ir decrescendo - escreva for e aperte TAB
// for(int i=0;i<10;i++) = i começado em 0, enquanto for menor que 10, acrescente +1
// Exemplo em OnTimer
//+------------------------------------------------------------------+
// Tipo especial enum, e uma int - serve para alterar o nome de exibição
//enum EstacoesAno
//  {
//   primavera, //0
//   verao, //1
//   outono, //2
//   inverno, //3
   // ou
   // primavera = 77,
   // verao = 34,
   // outono = 99,
   // inverno = 106,
//   };
// Apos ter sido declarada, podera ser chamada em OnTimer
//+------------------------------------------------------------------+
// Variavel tipo InPut
// Esta relacionado aos valores que o usuario vai introduzir, Sl, TP, MMA etc.
// Fica debaixo da parte #properity e em cima de OnInit
// Pode se adicionar o enum aqui
//   enum EstacoesAno
//     {
//      primavera, //PRIMAVERA
//      verao, //VERAO
//      outono, //OUTONO
//     inverno, //INVERNO
//     };
//    input int numPeriodos = 11; //Nº de Períodos
//    input string comentario = ""; //Comentarios
//    input EstacoesAno estacao = outono; //Estações
//+------------------------------------------------------------------+
// Declarando Funções
//   void myFun (double a, double b)
//   {
//      double soma = a + b;
//      Print("Soma = " + soma);
//   }
// Ir para função OnTimer
// Outra Forma
// void myFun2 (double x, double y)
// {
// double divisao =x/y;
// return div;
// }
//+------------------------------------------------------------------+
// Variaveis locais e globais
// uma variavel global esta definida fora de um escolpo, ou função. Ela pode ser utilizada em todo o código
// int variavelGlobal = 3;
// Uma variavel local so pode ser definida dentro de uma função, sendo que a função podera ser chamada, mas nao a variavel dentro dela.
// void funcaoGlobal()
// {
// int valorLocal1 = 5;
// int valorLocal2 = 6;
// Print("Multiplicação =", valorLocal1*valorLocal2);
// }
//+------------------------------------------------------------------+
// Variaveis predefinidas pelo mql5
// Pode ser chamada dentro do codigo todo?
// Print("Simbolo = ", _Symbol);
// _Symbol = o nome do ativo financeiro
// Print("Periodo = ", _Period);
// Periodo Grafico
// Print("Pontos = ", _Point);
// Quantidade de pontos
// Print("Digitos = ", _Digits);
// Numero de digitos em pontos decimais do ativo atual
//+------------------------------------------------------------------+
// Operações Matematicas
// int exA = 5 + 2;
// double exB = 3.14 + exA;
// double exC » exB + exA;
// double exD » exB - exC;
// Multiplicação
// int exE = 7 * 10;
// double exF = 3 * 1.68;
// Divisão
// int exG = 9 / 3;
// double exH = 10 / 3;
// MQL5 oferece algumas operações como padrão
// Digitar apenas Math e escolher
//+------------------------------------------------------------------+
// Lógicas e Condicionais
// Lógicas
// A > B
// A < B
// A >= B
// A <= B
// A == B
// A != B
// || significa ou
// Condicionais
// int A = 7;
// int B = 7;
// int C = 10;
// Se a igual a B e A + B igual a C mostre ok
//if(A == B && A+B == C)
//{
//Print("Ok!");
//}
//if(A == B || A == C)
//{
//Print(true);
//}
//if(A > B)
//{
//Print("A > B");
//}
//else
//{
//Print("A < B");
//}
// Ha um erro nessa condição - Exemplo de inumeras condições
//if(A>B)
//  {
//   Print("A>B")
//  }else if(A == B)
//          {
//           Print ("A = B");
//          }
//   else if(A != B)
//          {
//           Print ("A !=B");
//          }
//   else
//     {
//      Print("Nada!");
//     }
//+------------------------------------------------------------------+
//Operador Ternários
//(condicional) ? (alternativa 1 se verdadeira): (alternativa 2 se falsa)
// Foi declarado uma condição onde e apresentado um dado
// Em segundo e declarado uma variavel resp, onde se cond for true resp ira admitir o primeiro valor, caso contrario o seugndo false
//bool cond = true;
//bool resp = cond ? true: false;
//Print(resp);
//+------------------------------------------------------------------+
// MQL5 e uma linguagem orientada apenas em funções e não a objetos
//+------------------------------------------------------------------+
int OnInit()
// Quando iniciado o robo, vai ser a primeira função a ser lida, dara acesso a conta com a corretora, validação de datas e outros.
  {
//--- create timer
   EventSetTimer(1);

//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
// Quando o robo for removido, sera executado essa função
  {


  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
// Quando um acordo é realizado, tick, a função OnTick é realizada
  {
//---

  }
//+------------------------------------------------------------------+
//| Timer function                                                   |
//+------------------------------------------------------------------+
void OnTimer()
// Devera ser exxecutado com o EventSetTimer(segundos);
// Quando especificar o segundos a contagem regressiva coemça para chamar a função OnTimer
  {  
//+------------------------------------------------------------------+
//int meuArray[3];
//meuArray[0] = 77;
//meuArray[1] = 5;
//meuArray[2] = 8;
//double meuArray2 [3] = {3.7, 8.1, 7.7};
//+------------------------------------------------------------------+
// ou for(int i=10;i>1;i--)
//for(int i=0;i<10;i++)
//{
//   Print("i =", i);
//   Print("i =", i+1);
//}
// Para misturar com vetoress, onde o total e ate que posição contar
//double meuArray2[3] = {3.7, 8.1, 7.7, 8.7};
//for(int i=0;i<4;i++)
  //{
   //Print("meuArray2[",i,"] = ", meuArray2[i]);
  //}
//  tambem pode ser simplificado, ele calcula o total do vetor e aplica
//double meuArray2[3] = {3.7, 8.1, 7.7, 8.7};
//for(int i=0;i<ArraySize(meuArray2);i++)
  //{
      //Print("meuArray2[",i,"] = ", meuArray2[i]);
  //}
//+------------------------------------------------------------------+
//      EstacoesAno estacao;
//      estacao = verao;
//      Print("Estação = ", estacao); 
//+------------------------------------------------------------------+
// 3 e 4 podem ser substituidos
//   myFun(3.14,4.79);
// 9 e 3 podem ser substituidos
// Print ("Div = ", myFun2(9,3));
//+------------------------------------------------------------------+
  }
//+------------------------------------------------------------------+

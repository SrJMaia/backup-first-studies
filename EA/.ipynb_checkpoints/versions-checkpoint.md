# *Versions*
- 1.0  
-- Primeiro teste  
- 1.1  
-- Trocado copy_rates_range para copy_rates_from_pos por conta da perda de dados  
-- Passando funções para robot_functions.py  
-- Primeira implementação de uma GUI  
- 1.2  
-- Colocado todos EUR  
-- Resolvido o bug 0001  
- 1.3
-- Importado ipynb para py  
-- Trocado o tempo do sleep de 0.5s para 0.1s  
-- Colocado restante dos pares  
- 1.4  
-- Removido botão exit, apenas sairá apertando X. Motivo: Irrelevante para já  
-- Janela é aberta em um tamanho de 960x320 e é possível ajusta-la  
-- Colocado balance, margin free e profit no topo, com cores e background  
- 1.5  
-- Resolvido bug 00002
-- Primeiro teste na AWS, houve problemas com a biblioteca myplotlib   
-- Printa a que preço foi comprado/vendido  
- 1.6  
-- Criado o get_data para pegar os dados, jogado no modulo
-- Passado risco como constante no módulo robot_functions.py  
-- Removido matplotlib e numpy  
-- Versão no topo da GUI é uma constante  
- 1.7  
-- Removido import do datetime, motivo: não estava sendo usado  
-- Dividido robot_functions em 3 outros modulos, mt5, financial e data  
-- Criado um novo modulo para lidar com a GUI  
-- Removido from IPython.display import clear_output, motivo: não era usado
-- Passado bestime e magic number como constantes  
- 1.8  
-- Ao inicializar, irá checar se o algotrading está ativado, caso não, desliga a ligação  
-- Colocado ping e estado da conexão na gui  
- 1.9  
-- Removido GUI para maior otimização
-- Removido account_info() do robo e passa para o proprio modulo, reduzido 2 parametros para abertura de ordem  
-- Ajustado erro grave em flags faltantes  
-- Resolvido bug 00003 e bug 00004  
-- Reduzido todos os if elif para uma lista de dicionarios  
- 2.0  
-- Resolvido bug 00005  
-- Agora em vez de lista, os eventos são apenas dicionarios  
-- Arrumado erro no login do mt5, apenas logava em uma conta em vez da conta passada coo parametro  
-- Mudada estrategia, em vez de besttime agora o valor tem que estar dentro de 2 desvios padroes
-- Robo agora opera por hora, no indice -2
-- Mudado o deviation de 0 para 10. Evitar erro 10004  
- 2.1  
-- Corrigindo o close position, enquanto não realizar a operação não sai do close
-- Forçado a abrir posição quando ha erro de preço novo  
- 2.2  
-- Mudado toda estratégia, adicionado TP e SL  

# *Bugs*  
### Abertos  

### Resolvidos  
- Bug 00001:  
-- Problema: Quando é feito uma operação bem sucedidade, uma mensagem de erro aparece. Esta retornando algum outro codigo.  
-- Solução: Estava retornando uma lista, apenas coloquei no if o result[0] para pegar o código 10009
-- Implementação: Feito na versão 1.2  
- Bug 00002:
-- Problema: Nome da função de fechar esta errada em tudo e excluir certos parametros  
-- Solução: Ajustei o nome removendo a letra a mais, como também tirei o parametro obrigatorio do magic number, ja não é mais necessario  
-- Implementação: Feito na versão 1.5  
- Bug 00003?:  
-- Possivel erro 10014, volume invalido?  
-- Solução: NZDCAD, NZDCHF e NZDJPY possuem um volume minimo de 0.1. Pelo menos na conta do MetaQuotes  
-- Implementação: Feito na versão 1.9  
- Bug 00004:  
-- Problema: Ping abaixo de 100ms continua amarelo  
-- Solução: Removido GUI  
-- Implementação: Feito na versão 1.9  
- Bug 00005:  
-- Problema: Erro 10004, nova cotação  
-- Solução: Colocado um elif diferenciado para saber diferenciar, apesar que não havia risco  
-- Implementação: Feito na versão 2.0  

# *Futuras Atualizações* 
-> Futuramente colocar schedule  
-> Futurametne colocar get_orders e checagem em uma faunção 
-> Salvar EVENTS em um arquivo  
-> Por o comentario da comrpa/venda no programa   
-> Possivel integração com o Telegram   
-> Desenho tanto do capital como variação dos numeros  
-> Mostrar operações ativas, assim como outras informações  
-> Importar py para um exe   
-> Manter os textso da gui em um lugar fixo conforme a tela aumenta
-> Retira GUI para ja, possivel diminuição do uso de CPU pela metade com um sleep de 0.1
-> Operar dobrado quando estiver acima de 2 desvios padrões?

# *Tarefas*
-> Entender o resultado do account_info  
-> O indice 0 é o mais antigo, o ultimo é o mais novo
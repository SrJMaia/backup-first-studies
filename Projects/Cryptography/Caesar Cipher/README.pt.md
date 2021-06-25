# O que é Cifra de César?  

Da Wikipedia: "Em criptografia, a Cifra de César, também conhecida como cifra de troca, código de César ou troca de César, 
é uma das mais simples e conhecidas técnicas de criptografia. É um tipo de cifra de substituição na qual cada letra do texto é 
substituída por outra, que se apresenta no alfabeto abaixo dela um número fixo de vezes. Por exemplo, com uma troca de três posições, 
A seria substituído por D, B se tornaria E, e assim por diante. O nome do método é em homenagem a Júlio César, que o usou para se comunicar com os seus generais"

É um metodo simples onde o alfabeto é empurrado para trás em n vezes. Se n for igual a 5 por exemplo, o alfabeto será:  

Plain | Cipher
------|--------
A     | F
B     | G
C     | H
D     | I
E     | J
F     | K
G     | L
H     | M
I     | N
J     | O
K     | P
L     | Q
M     | R
N     | S
O     | T
P     | U
Q     | V
R     | W
S     | X
T     | Y
U     | Z
V     | A
W     | B
X     | C
Y     | D
Z     | E

# Python

## *remove_characters* Parametro Explicado:


Se colocado como True na seguinte mensagem:  
```python
>>> message: "The Zen of Python, by Tim Peters !"

>>> encode_message = encode(message, 3, remove_characters=True)  

>>> encode_message  

'wkh chq ri sbwkrq eb wlp shwhuv'  

>>> decoded_message = decode(encode_message, 3)  

>>> decoded_message  

'the zen of python by tim peters'  
```

Se colocado como False:
```python
>>> encode_message = encode(message, 3, remove_characters=False)  

InvalidCharacter: The string contains a special character besides abcdefghijklmnopqrstuvwxyz.,àèìòùáéíóúýâêîôûãñõäëïöüÿ .
```

# GO


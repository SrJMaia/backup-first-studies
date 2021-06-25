 • [PT readme](https://github.com/SrJMaia/Projecs/blob/main/Cryptography/Caesar%20Cipher/README.pt.md) • 

# What is Caesar Cipher?  

From Wikipedia: "In cryptography, a Caesar cipher, also known as Caesar's cipher, the shift cipher, Caesar's code or Caesar shift, is one of the simplest and most widely known encryption techniques. It is a type of substitution cipher in which each letter in the plaintext is replaced by a letter some fixed number of positions down the alphabet. For example, with a left shift of 3, D would be replaced by A, E would become B, and so on. The method is named after Julius Caesar, who used it in his private correspondence."

It's a simple method where the alphabet is shifted by n and letters are replaced. If n is equal to 5 for example, the alphabet will be:

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

## The *remove_characters* Paramaters Explanation


If it's set to True the following steps will happen:  
```python
>>> message: "The Zen of Python, by Tim Peters !"

>>> encode_message = encode(message, 3, remove_characters=True)  

>>> encode_message  

'wkh chq ri sbwkrq eb wlp shwhuv'  

>>> decoded_message = decode(encode_message, 3)  

>>> decoded_message  

'the zen of python by tim peters'  
```

If it's set to False:
```python
>>> encode_message = encode(message, 3, remove_characters=False)  

InvalidCharacter: The string contains a special character besides abcdefghijklmnopqrstuvwxyz.,àèìòùáéíóúýâêîôûãñõäëïöüÿ .
```

# GO


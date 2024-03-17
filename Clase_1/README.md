# Datos y variables
normalmente siempre empezaremos el script importando las librerias que nos sean necesarias, Aunque podemos asignar cualquier nombre en la variable estas se asignan de forma que al leer el codigo en un futuro se pueda entender facilmente

```
# Importar librerías necesarias
import numpy as np
# Constantes y valores de referencia
R=8.314
T_R=298.15
P_R=1e5
```
a lo largo de este curso se usaran diversas librerias, a diferencia de matlab python es un lenguaje de programacion muy potente que dispone de una gran versatibilidad pero para muchas operaciones. para usarlas siempre sera necesario que usemos primero el nombre de la libreria y luego la funcion por ejemplo np.array, en el curso sera neceario importar distintas librerias o funciones especificas de estas la siguiente lista sera aquellas que usaremos 

- Numpy: siempre al importar la libreria le cambiaremos el nombre a np de forma que la linea sera import numpy as np aunque se puede dejar el nombre como numpy ya que la usaremos con frecuencia nos hara que leamos mas rapido el codigo, la biblioteca numpy nos sera necesaria para trabajar con los vectores (array), operaciones matematicas, booleanos ( devuelven un valor verdadero o falso estos operadores se usan en estructuras de control tipo while, if, for... ) o como base para otras bibliotecas
  
- scipy: esta biblioteca la usaremos especialmente para integracion numerica optimizacion y calculos iterativos.
  
- matplotlib.pyplot: esta biblioteca la acortaremos renombrandola como plt es decir que la linea quedaria tal que **import matplotlib.pyplot as plt** , esta biblioteca se usara para representar las graficas en la asignatura
  
> aunque en los scripts las tablas se muestran con un print estas se pueden hacer con la biblioteca pandas que normalmente se importa como import pandas as pd , esta biblioteca permite trabajar con tablas de datos (Dataframes) de forma que si queremos usar varias fuentes o automatizar el codigo para hacer un calculo de varias sustancias es muy comodo

# condiciones y datos tabulados 
```
# Calculo prop. termodinamicas CO2
# Condiciones 
T = 500 # K
P = 5e6 # Pa
# Datos tabulados
S0 = 213.8
DFH0 = -393.5e3
# Crear la una variable con los coeficientes en el orden que aparecen en tablas
ACP_tabla = np.array([19.8, 0.07344, -5.602e-5, 1.715e-8])
# Invertir para trabajar con polinomios en potencias en orden decreciente
ACP = ACP_tabla[::-1]
```
>[!NOTE] 
>$$ACP(T) = 1.715 \times 10^{-8} \cdot T^3 - 5.602 \times 10^{-5} \cdot T^2 + 0.07344 \cdot T + 19.8$$

El polinomio de la capacidad calorifica ACP podemos encontrarlo ordenado en orden creciente o decreciente, en este caso lo encontramos en orden creciente para volverlo en orden decreciente se puede realizar de 2 maneras

1. usando la funcion flip de la biblioteca numpy es decir ACP= np.flip(ACP)
2. usando sintaxis, [0:-1:-1]  en python como en la mayoria de lenguajes el primer elemento es el 0 el ultimo lo podriamos saber con la funcion len que nos devuelve la longitud del vector pero es mucho mas sencillo usar -1 siendo este el ultimo -2 el penultimo... , y el ultimo valor que hemos añadido en la sintaxis el -1 indica la distancia entre los elementos es decir decimos que nos cree un vector que tenga de longitud todo el inicial pero que vaya recorriendo la secuencia de forma inversa, normalmente al usar todo el vector podemos omitir la posicion del primero y el ultimo quedando tal que **[::-1]**.
   
# Calculo entalpia
 $$H^{ig} = \Delta_f H^o (g) + \int_{T}^{298.15} C_{{p}^{\,ig}} \, \ dT$$

entonces podemos calcular la entropia de la siguiente manera:
```

ACPi = np.polyint(ACP);
HIG = DFH0 + np.polyval(ACPi, T) - np.polyval(ACPi, T_R)
print('H^ig(', T, 'K ) = ', HIG.round(0)/1000, 'kJ/mol')
print(ACPi) 
```
donde con np.polyint integramos el polinomio de la capacidad calorifica con **polyint** este comando tiene la siguiente estructura:
np.polyint(p, m=None, k=None) donde p es el polinomio a integrar (en nuestro caso ACPi), m(opcional) es el grado del polinomio si no indicamos ninguno tomara el grado del polinomio p+1 , y k(opcional) el valor de la constante al integrar que por defecto usaremos el 0 

# # Calculo entropia
$$S^{ig}=S^{\circ} (g)\int^{T}_{298.15} \frac{Cp}{T}dT - R \ ln \frac{P}{10^5}$$
es decir  si definimos 
$$C_{{p}^{\,ig}} = \sum^{i=n}_{i=1}a_iT^{\ i-1}$$
$$S^{ig} = a_1 \ln\frac{T}{298.15} + \sum_{i=2}^{i=n} \frac {a_i} {(i - 1)} (T^{i-1}-298.15^{i-1})- R \ ln \frac{P}{10^5}$$
Por tanto queremos: 
- el logaritmo del primer termino del polinomio (recordemos que estaba en orden decreciente por tanto es el ultimo valor es decir -1)
- el polinomio quitando el primer termino  al usar polyval lo que hacemos es evaluar el polinomio que indicamos (ACPTi en las condiciones deseadas)

```
ACPTi = np.polyint(ACP[0:-1])  # Para integrar el término independiente aparte
SIG = S0 + ACP[-1] * np.log(T/T_R) + np.polyval(ACPTi, T)-np.polyval(ACPTi, T_R)-R*np.log(P/P_R)
```
en la primera linea con ACP[0:-1] lo que estamos haciendo es indiciar que nos integre el polinomio del vector ACP desde el primer elemento de este hasta el penultimo, aunque el -1 se usa para indicar que es el ultimo valor por defecto en python excluye el elemento en el indice de parada y al no asignarle la distancia es decir cada cuantos elementos queremos que lo haga toma por defecto el 1
# Calculo Volumen  y energia de gibbs
$$ V^{ig} = \frac{RT}{P}$$
$$ G^{ig} = H^{ig}-TS^{ig}$$
```
VIG = R*T/P
GIG = HIG-T*SIG
# Imprime propiedades
print('Propiedades del CO2 a P =', P/1e5, 'bar,  T = ', T, 'K')
print('S^ig = ', SIG.round(1), 'J/mol K')
print('H^ig = ', HIG.round(-1)/1000, 'kJ/mol')
print('G^ig = ', GIG.round(0)/1000, 'kJ/mol')
```
como en las operaciones estamos usando numeros flotantes a la hora de ver en pantalla no nos hace falta tantos decimales, para ello usaremos round(Z) donde z ser el numero de decimales que queremos al usar 0 indicamos que nos redondee al numero entero, con 1 decimos que queremos un decimal y con -1 queremos que en vez de redondear la unidad que sea a la decena
>[!IMPORTANT]
> este paso se debe realizar siempre al acabar, ya que arrastraria el error del redondeo en las operaciones
# Ejemplos a calcular:
| DATOS  |Dióxido de carbono, C<sub style="margin-left: 0.15em;"></sub>O<sub>2</sub> |Difluorometano, CH<sub>2</sub>F<sub>2</sub>| Benceno, C<sub>6</sub>H<sub>6</sub>|
| :------------- | :-------------: |:-------------: |:-------------: |
| P (bar)  | 5 | 6|5|
| T (K)  | 500  | 650| 575|
| Δ<sub>f</sub>H<sup>°</sup>(g) , (kJ/mol)   | -393.5  | -452.3|  82.9|
| S<sup>°</sup>(g) , J/(mol K) | 213.8   | 246.7 |  269.2|
| C<sub>p</sub><sup>ig</sup> , J/(mol K)| 19.80 + 0.07344 𝑇 − 5.602 · 10<sup>-5</sup> 𝑇<sup>2</sup> + 1.715 · 10<sup>-8</sup> 𝑇<sup>3</sup>   | 11.79 + 0.1181 𝑇 − 4.843 · 10<sup>-5</sup> 𝑇<sup>2</sup> + 2.125 · 10<sup>-9</sup> 𝑇<sup>3</sup>|  -33.92 + 0.4739 𝑇 − 3.017 · 10<sup>-4</sup> 𝑇<sup>2</sup> + 7.130 · 10<sup>-8</sup> 𝑇<sup>3</sup>|
# Influencia de la temperatura
```
# Crea un vector de temperaturas
T = np.linspace(200, 1000)
# Calcula H y S como gas ideal en función de T
HIG = DFH0 + np.polyval(ACPi, T)-np.polyval(ACPi, T_R)
ACPTi = np.polyint(ACP[0:-1])  # Para integrar sin el término independiente
SIG = S0 + ACP[-1]*np.log(T/T_R)+np.polyval(ACPTi, T)-np.polyval(ACPTi, T_R)-R*np.log(P/P_R)
```
con la funcion linspace de numpy lo que hacemos es crear un vector que vaya desde el 200 hasta el 1000, al no asignarle la distancia que hay entre cada elemento esta toma por defecto uno, si quisieramos en vez de que tomara esa distancia que se dieran una serie de puntos por ejemplo 50 seria np.linspace(200, 1000,50)

## Representacion H<sub>ig</sub> y S<sub>ig</sub> frente a la temperatura
```
import matplotlib.pyplot as plt
# Importa librería para gráficos
# Representa Hig y Sig
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(T, HIG/1000, 'r', label="H^ig")
axes[0].set_xlabel('T, K')
axes[0].set_ylabel('H$^{ig}$, kJ/mol K')
axes[1].plot(T, SIG, 'b', label="S^ig")
axes[1].set_xlabel('T, K')
axes[1].set_ylabel('S$^{ig}$, J/mol')
plt.show()
```
aqui lo que hacemos es importar la libreria con la que vamos a trazar los graficos,  con la linea '' fig, axes = plt.subplots(1, 2, figsize=(12, 4))'' lo que hacemos es crear un objeto que sera la figura (fig) que contendra la lista de subfiguras (axes)  con la parte de ''plt.subplots(1, 2, ) '' lo que se hace es crear la figura con 1 fila  y 2 columnas, y con la parte de figsize=(12, 4) lo que hacemos es asignarle el tamaño de la figura en pulgadas (En este nos referimos al tamaño de la figura principal, no el de las subfiguras que serian axes[0] y axes[1])

## Representacion U<sub>ig</sub> , G<sub>ig</sub> y A<sub>ig</sub> frente a la temperatura
$$ U^{ig} = H^{ig}-PV^{ig}= H^{ig}-RT$$
$$ G^{ig} = H^{ig}-TS^{ig}$$
$$ A^{ig} = U^{ig}-TS^{ig}$$
```
# Representa el resto de propiedades: Uig, Gig, Aig
fig2, axes2 = plt.subplots(1, 2, figsize=(14, 4))
# Figura un poco más ancha para que estén separadas
axes2[0].plot(T, (HIG-R*T)/1000,  'b', label="U$^{ig}")
axes2[0].set_xlabel('T, K')
axes2[0].set_ylabel('U$^{ig}$, kJ/mol K')
axes2[1].plot(T, (HIG-T*SIG)/1000, 'b', label="G^ig")
axes2[1].plot(T, (HIG-R*T-T*SIG)/1000, 'r', label="A^ig")
axes2[1].legend()
axes2[1].set_xlabel('T, K')
axes2[1].set_ylabel('G$^{ig}$, A$^{ig}$, kJ/mol K')
plt.show()
```
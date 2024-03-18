# Datos y variables
Importaremos las bibliotecas necesarias al comienzo del script. Generalmente, asignaremos nombres descriptivos a nuestras variables para que el código sea fácil de entender en el futuro.

```Python
# Importar librerías necesarias
import numpy as np
# Constantes y valores de referencia
R=8.314
T_R=298.15
P_R=1e5
```
A lo largo de este curso se utilizarán diversas librerías. A diferencia de MATLAB, Python es un lenguaje de programación muy potente que ofrece una gran versatilidad, pero para muchas operaciones siempre será necesario utilizar primero el nombre de la librería y luego la función. Por ejemplo, np.array. Durante el curso, será necesario importar distintas librerías o funciones específicas de estas. Las principales que usaremos seran:
<br>

- Numpy: Siempre al importar la librería, le cambiaremos el nombre a np, de forma que la línea será import numpy as np. Aunque se puede dejar el nombre como numpy, dado que la utilizaremos con frecuencia, esto nos facilitará la lectura del código. La biblioteca NumPy será necesaria para trabajar con los vectores (array), realizar operaciones matemáticas y trabajar con booleanos (Operadores logicos,que devuelven un valor verdadero o falso como son AND, OR, NOT, == , != , < , > , =< , >=  estos operadores se utilizan en estructuras de control tipo while, if, for, etc.) o como base para otras bibliotecas.
  
- scipy: Esta biblioteca la usaremos especialmente para integración numérica, optimización y cálculos iterativos.
  
- matplotlib.pyplot: **Esta biblioteca la acortaremos renombrándola como plt**, es decir, la línea quedaría así: import matplotlib.pyplot as plt. Esta biblioteca se usará para representar las **gráficas** en la asignatura.
  
> Aunque en los scripts las tablas se muestran con un print, estas se pueden hacer con la biblioteca pandas, que normalmente se importa como import pandas as pd. Esta biblioteca permite trabajar con tablas de datos (Dataframes), de forma que si queremos usar varias fuentes o automatizar el código para hacer un cálculo de varias sustancias, es muy cómodo.

# Condiciones y datos tabulados.
```Python
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
Con np.array lo que hacemos es crear un vector. En caso de introducir solo un valor numérico, también se puede introducir una cadena de texto ('string') para trabajar con ella. Siempre el vector que queremos va entre [ ], y como todas las funciones, el objetivo sobre el que realizamos la función va entre ( ). Es decir, si por ejemplo hubiéramos definido un vector ACP como ACP = [19.8, 0.07344, -5.602e-5, 1.715e-8], en la siguiente línea se usaría np.array(ACP).<br><br>
>[!NOTE] Recordatorio útil
>$$ACP(T) = 1.715 \times 10^{-8} \cdot T^3 - 5.602 \times 10^{-5} \cdot T^2 + 0.07344 \cdot T + 19.8$$
<br>

El polinomio de la capacidad calorífica, ACP, puede encontrarse ordenado en orden creciente o decreciente. En este caso, lo encontramos en orden creciente. Para volverlo en orden decreciente:

1. Usando la función flip de la biblioteca NumPy, es decir, ACP = np.flip(ACP).
   
2. Usando la sintaxis [0:-1:-1] en Python, como en la mayoría de los lenguajes, el primer elemento es el 0 y el último se puede conocer con la función len, que nos devuelve la longitud del vector. Sin embargo, es mucho más sencillo usar -1 para representar el último elemento y -2 para el penúltimo. El último valor en la sintaxis -1 indica la distancia entre los elementos. Es decir, creamos un vector que tenga la misma longitud que el inicial, pero que vaya recorriendo la secuencia en orden inverso. Al usar todo el vector, podemos omitir la posición del primero y el último, quedando simplemente como **[::-1]**.
<br>   
# Cálculo de entalpía.
 $$H^{ig} = \Delta_f H^o (g) + \int_{T}^{298.15} C_{{p}^{\,ig}} \, \ dT$$

Entonces, podemos calcular la entropía de la siguiente manera:
```python

ACPi = np.polyint(ACP);
HIG = DFH0 + np.polyval(ACPi, T) - np.polyval(ACPi, T_R)
print('H^ig(', T, 'K ) = ', HIG.round(0)/1000, 'kJ/mol')
print(ACPi) 
```
Donde con np.polyint integramos el polinomio de la capacidad calorífica con polyint. Este comando tiene la siguiente estructura: np.polyint(p, m=None, k=None), donde p es el polinomio a integrar (en nuestro caso ACPi), m (opcional) es el grado del polinomio. Si no se indica ninguno, tomará el grado del polinomio p + 1, y k (opcional) es el valor de la constante al integrar, que por defecto usaremos el 0. Con polyval, el primer argumento será el polinomio y el segundo las condiciones donde se evalúa.

# Cálculo de entropía
$$S^{ig}=S^{\circ} (g)\int^{T}_{298.15} \frac{Cp}{T}dT - R \ ln \frac{P}{10^5}$$
Es decir  si definimos: 
$$C_{{p}^{\,ig}} = \sum^{i=n}_{i=1}a_iT^{\ i-1}$$
$$S^{ig} = a_1 \ln\frac{T}{298.15} + \sum_{i=2}^{i=n} \frac {a_i} {(i - 1)} (T^{i-1}-298.15^{i-1})- R \ ln \frac{P}{10^5}$$
Por tanto, queremos:
- El logaritmo del primer término del polinomio (recordemos que estaba en orden decreciente, por lo tanto, es el último valor, es decir, -1).
  
- El polinomio quitando el primer término. Al usar polyval, lo que hacemos es evaluar el polinomio que indicamos (ACPTi) en las condiciones deseadas.

```python
ACPTi = np.polyint(ACP[0:-1])  # Para integrar el término independiente aparte
SIG = S0 + ACP[-1] * np.log(T/T_R) + np.polyval(ACPTi, T)-np.polyval(ACPTi, T_R)-R*np.log(P/P_R)
```
En la primera línea, con ACP[0:-1], lo que estamos haciendo es indicar que nos integre el polinomio del vector ACP desde el primer elemento de este hasta el penúltimo. Aunque el -1 se usa para indicar que es el último valor, por defecto en Python excluye el elemento en el índice de parada. Al no asignarle la distancia, es decir, cada cuántos elementos queremos que lo haga, toma por defecto el 1.
# Calculo Volumen  y energia de gibbs
$$ V^{ig} = \frac{RT}{P}$$
$$ G^{ig} = H^{ig}-TS^{ig}$$
```Python
VIG = R*T/P
GIG = HIG-T*SIG
# Imprime propiedades
print('Propiedades del CO2 a P =', P/1e5, 'bar,  T = ', T, 'K')
print('S^ig = ', SIG.round(1), 'J/mol K')
print('H^ig = ', HIG.round(-1)/1000, 'kJ/mol')
print('G^ig = ', GIG.round(0)/1000, 'kJ/mol')
```
Como en las operaciones estamos usando números flotantes, a la hora de visualizarlos en pantalla no necesitamos tantos decimales. Para ello, usaremos round(Z), donde Z es el número de decimales que queremos. Al usar 0, indicamos que queremos redondear al número entero; con 1, decimos que queremos un decimal, y con -1, queremos que en vez de redondear la unidad, lo haga a la decena.
> Datos tomados de:
> * The 84th Edition of the CRC Handbook of Chemistry and Physics, Lide (2003) Section 5: Standard Thermodynamic Properties of Chemical Substances
> 
> * The Properties of Gases and Liquids, Reid, Prausnitz y Poling, fourth edition (1987) Appendix A: Property Data Bank

>[!IMPORTANT]
> Este paso se debe realizar siempre al final, ya que arrastraría el error del redondeo en las operaciones.
# Ejemplos a calcular:
| DATOS  |Dióxido de carbono, C<sub style="margin-left: 0.15em;"></sub>O<sub>2</sub> |Difluorometano, CH<sub>2</sub>F<sub>2</sub>| Benceno, C<sub>6</sub>H<sub>6</sub>|
| :------------- | :-------------: |:-------------: |:-------------: |
| P (bar)  | 5 | 6|5|
| T (K)  | 500  | 650| 575|
| Δ<sub>f</sub>H<sup>°</sup>(g) , (kJ/mol)   | -393.5  | -452.3|  82.9|
| S<sup>°</sup>(g) , J/(mol K) | 213.8   | 246.7 |  269.2|
| C<sub>p</sub><sup>ig</sup> , J/(mol K)| 19.80 + 0.07344 𝑇 − 5.602 · 10<sup>-5</sup> 𝑇<sup>2</sup> + 1.715 · 10<sup>-8</sup> 𝑇<sup>3</sup>   | 11.79 + 0.1181 𝑇 − 4.843 · 10<sup>-5</sup> 𝑇<sup>2</sup> + 2.125 · 10<sup>-9</sup> 𝑇<sup>3</sup>|  -33.92 + 0.4739 𝑇 − 3.017 · 10<sup>-4</sup> 𝑇<sup>2</sup> + 7.130 · 10<sup>-8</sup> 𝑇<sup>3</sup>|
# Influencia de la temperatura
```Python
# Crea un vector de temperaturas
T = np.linspace(200, 1000)
# Calcula H y S como gas ideal en función de T
HIG = DFH0 + np.polyval(ACPi, T)-np.polyval(ACPi, T_R)
ACPTi = np.polyint(ACP[0:-1])  # Para integrar sin el término independiente
SIG = S0 + ACP[-1]*np.log(T/T_R)+np.polyval(ACPTi, T)-np.polyval(ACPTi, T_R)-R*np.log(P/P_R)
```
Con la función linspace de NumPy lo que hacemos es crear un vector que vaya desde el 200 hasta el 1000. Al no asignarle la distancia que hay entre cada elemento, esta toma por defecto uno. Si quisiéramos en vez de que tomara esa distancia, se dieran una serie de puntos, por ejemplo 50, sería np.linspace(200, 1000, 50).

## Representacion H<sub>ig</sub> y S<sub>ig</sub> frente a la temperatura
```Python
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
En esta sección, importamos la biblioteca que usaremos para trazar gráficos. La línea fig, axes = plt.subplots(1, 2, figsize=(12, 4)) crea un objeto llamado fig, que será la figura principal que contendrá nuestras subfiguras, representadas por la lista axes. Con plt.subplots(1, 2), creamos una figura con una fila y dos columnas para las subfiguras. Además, con figsize=(12, 4), especificamos las dimensiones de la figura principal en pulgadas. Es importante destacar que estas dimensiones se aplican a la figura principal, no a las subfiguras representadas por axes[0] y axes[1]."
## Representacion U<sub>ig</sub> , G<sub>ig</sub> y A<sub>ig</sub> frente a la temperatura
$$ U^{ig} = H^{ig}-PV^{ig}= H^{ig}-RT$$
$$ G^{ig} = H^{ig}-TS^{ig}$$
$$ A^{ig} = U^{ig}-TS^{ig}$$
```Python
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
Cuando usamos set_xlabel o set_ylabel, ya sea detrás de axes o de un plot, lo que hacemos es asignar un nombre a la etiqueta del eje correspondiente. Además, con legend mostramos la leyenda, que nos permite entender qué representa cada línea del diagrama. Finalmente, con plt.show() conseguimos que se muestre la figura que hemos creado.
# Estimación de la Cp del propano como gas ideal
4. A partir de los siguientes datos para la capacidad calorífica del propano (M=44.097 g/mol) a
distintas presiones y temperaturas, calcular los coeficientes de un ajuste polinomial para la
capacidad calorífica como gas ideal

|           |             |         | CP, J mol<sup>-1</sup> K<sup>-1</sup> |         |          |
| :------------: | ------------ | ------------ | ------------ | ------------ | ------------ |
| P, kg/cm<sup>2</sup>  / T  |              | 20°C         | 40°C         | 60°C         | 80°C         |
|    0.5       |             | 73.06        | 76.53        | 80.55        | 84.59        |
|    1.0       |             | 73.51        | 76.95        | 80.93        | 84.79        |
|    2.0       |             | 74.47        | 77.79        | 81.54        | 85.36        |
|    3.5       |             | 76.32        | 79.19        | 82.56        | 86.19        |
|    5.0       |             | 78.48        | 80.63        | 83.56        | 86.97        |
|    6.5       |             | 81.13        | 82.44        | 85.00        | 88.01        |
|    8.0       |             | 84.57        | 84.61        | 86.45        | 89.02        |
|    10        |             |              | 88.01        | 88.65        | 90.65        |
|    12        |             |              | 93.18        | 91.28        | 92.39        |
|    14        |             |              |              | 94.95        | 94.37        |



```Python
import numpy as np
import matplotlib.pyplot as plt
# Cp J mol-1 K-1
# Datos
T = 273.15+np.array([20,40,60,80])#K
P20 = np.array([0.5,1,2,3.5,5,6.5,8])
Cp20 = np.array([73.06,73.51,74.47,76.32,78.48,81.13,84.57])
P40 = np.array([0.5,1,2,3.5,5,6.5,8,10,12])
Cp40 = np.array([76.53,76.95,77.79,79.19,80.63,82.44,84.61,88.01,93.18])
P60 = np.array([0.5,1,2,3.5,5,6.5,8,10,12,14])
Cp60 = np.array([80.55,80.93,81.54,82.56,83.56,85,86.45,88.65,91.28,94.95])
P80 = np.array([0.5,1,2,3.5,5,6.5,8,10,12,14])
Cp80 = np.array([84.59,84.79,85.36,86.19,86.97,88.01,89.02,90.65,92.39,94.37])
```
En esta parte del código, simplemente hemos importado las librerías que vamos a necesitar y creado los vectores de presión y la capacidad calorífica que tiene el propano en cada temperatura, es decir, a qué valores de presión (P) y capacidad calorífica (CP) corresponde cada temperatura (T).
```Python
# Ajuste de Cp con la presión a cada temperatura
# orden del polinomio de ajuste
n=4;

print('Ajuste de Cp_exp con n = ',n)
#Ajuste polinomial de los datos experimentales a 20°C
A20=np.polyfit(P20,Cp20,n)
Pgr20 = np.linspace(0,P20[-1],100)
fig, ax = plt.subplots(1, 2, figsize=(16, 8)) #creamos 1 figura con 2 subtramas 
ax[0].plot(P20, Cp20, 'ob', label='T= 20')
ax[0].plot(Pgr20, np.polyval(A20,Pgr20),'-b', label = 'Ajuste 20')
```
- Establecemos el orden del polinomio que vamos a querer, normalmente con el grado 3 ya da buenos resultados y a partir del grado 4 no tendremos una gran diferencia. Luego, con polyfit, lo que hacemos es ajustar dos vectores a un polinomio donde 'p' es el vector de presiones, 'cp' es el de la capacidad calorífica y 'n' es el grado de este. Como queremos graficar y tenemos pocos puntos, lo que haremos será crear un vector que vaya desde el primer punto (0) hasta el último (-1), espaciándolo de forma que nos dé 100 puntos.<br>
  
- En ax[0], es decir, la primera subfigura, vamos a dibujar con la primera línea los puntos experimentales. Al usar o*, el o indica que son puntos y el * será la letra que asigna el color. Si, por el contrario, en vez de o usamos -, indicamos que sea una línea continua que vaya entre los puntos. Como en pgr20 habíamos creado el vector con 100 puntos, para representarlo es necesario evaluar en el polinomio que habíamos creado previamente, a20, en los valores de cada punto, es decir, pgr20.
  
- Con label, lo que hacemos es darle una etiqueta a lo que hemos representado, para luego poder verlo en la leyenda. Es decir, nos aparecerá en la leyenda que los puntos azules son T=20 y la línea azul es el ajuste.
```Python
A40=np.polyfit(P40,Cp40,n)
Pgr40 = np.linspace(0,P40[-1],100)
ax[0].plot(P40, Cp40, 'og', label = 'T= 40')
ax[0].plot(Pgr40, np.polyval(A40,Pgr40),'-g', label = 'Ajuste 40')

A60=np.polyfit(P60,Cp60,n)
Pgr60 = np.linspace(0,P60[-1],100)
ax[0].plot(P60, Cp60, 'om', label = 'T= 60')
ax[0].plot(Pgr60, np.polyval(A60,Pgr60),'-m', label = 'Ajuste 60')

A80=np.polyfit(P80,Cp80,n)
Pgr80 = np.linspace(0,P80[-1],100)
ax[0].plot(P80, Cp80, 'or', label = 'T= 80')
ax[0].plot(Pgr80, np.polyval(A80,Pgr80),'-r', label = 'Ajuste 80')
```
```Python
ax[0].set_xlabel('$P, kg/cm^{2}$')
ax[0].set_ylabel('$C_{p}, J mol^{-1} K^{-1}$')

ax[0].legend()
```
Es importante que todas las gráficas estén etiquetadas, por ello en cada una se debe usar set_xlabel y set_ylabel. La cadena de texto (string) va entre comillas simples (''). Si queremos poner superíndices o subíndices, se usa el formato de LaTeX, es decir, irá entre $ $. Además, si es solo una letra, puede ir solo siendo subíndice con _ o siendo superíndice con ^, pero si van varias, debe ir forzosamente entre { }.
```Python
#Crear vector con los términos independientes
Cp_ig=np.array([A20[-1], A40[-1], A60[-1], A80[-1]])
print('Valores de C_p como gas ideal, extrapolando a P=0')
print('T/K :         ', T)
print('a_0 J/mol K   ', Cp_ig)
```
Comparar el resultado con el obtenido a partir de los datos propuestos por Chao (1973):
| Temperatura (K) | Capacidad Calorífica ( J/mol<sup>-1</sup> K<sup>-1</sup>) |
| --------------- | ------------------------------ |
| 200             | 56.07                          |
| 273.15          | 68.74                          |
| 298.15          | 73.6                           |
| 300             | 73.93                          |
| 400             | 94.01                          |
| 500             | 112.59                         |
| 600             | 128.70                         |
| 700             | 142.67                         |
| 800             | 154.77                         |
| 900             | 165.35                         |
| 1000            | 174.6                          |

```Python
# Comparación con valores de Chao, 1973
Texp=np.array([200,273.15,298.15,300,400,500,600,700,800,900,1000])
Cpexp=np.array([56.07,68.74,73.6,73.93,94.01,112.59,128.70,142.67,154.77,165.35,174.6])
# Ajuste de Cp_exp con el orden (n) anteriorme indicado 
Aexp=np.polyfit(Texp,Cpexp,n);
```
Creamos un polinomio a partir de los datos experimentales con el mismo orden que los que hemos creado anteriormente, para poder compararlos mejor.
```Python
ax[1].plot(Texp,Cpexp,'+b', label ='Datos Chao, 1973')
xexp=np.linspace(Texp[0],Texp[-1],200);
ax[1].plot(xexp,np.polyval(Aexp,xexp), '-b', label = 'Ajuste datos Chao')
ax[1].plot(T,Cp_ig,'or') # representando el ultimo punto de cada vector T para la maxima presion documentada
ax[1].set_xlabel('$T, K$')
ax[1].set_ylabel('$C_{p}, J mol^{-1} K^{-1}$')
ax[1].legend()
```
En la segunda subgráfica representamos los puntos que tenemos de bibliografía, los puntos evaluados del polinomio que hemos encontrado y los puntos de la capacidad calorífica de la primera bibliografía en su presión máxima para las distintas T.
```Python
# Diferencia entre los dos cálculos
Cpcal=np.polyval(Aexp,T)
print('Cpcal J/mol K ',Cpcal)
print('Diferencia, %:',(Cpcal-Cp_ig)/Cpcal*100)
```
![](Clase_1\imagenes\Cp_Prop.png)
Calculamos la capacidad calorífica con el polinomio obtenido de Chao (con la función polyval) y lo comparamos con el último punto que teníamos en la primera bibliografía para cada T. Cuando usamos el argumento '%' en el segundo print, es para que este nos lo devuelva automáticamente en formato de porcentaje

# Modelo de Joback-Reid y Rarey-Nannolal
En algunas ocasiones, es posible que no se disponga de datos bibliográficos para nuestra sustancia. En estas situaciones, es conveniente recurrir a métodos alternativos. Ambos métodos se basan en la contribución por grupos, lo que significa que cada grupo presente en nuestra molécula contribuye a un parámetro específico. Consideremos el caso del 1-hexeno, C<sub>6</sub>H<sub>12</sub>. <br>
![1-hexene](https://github.com/ChristianPh404/TQA_2024-2025/blob/main/Clase_1/imagenes/1-hexene.png)

tendriamos:
grupos que contribuyen:
- -CH3: 1.0
- -CH2-: 3.0
- =CH2: 1.0
- =CH-: 1.0
esto lo podemos comprobar en [Joback](Joback.py). el modelo de rarey-Nannoal tiene en cuenta mas parametros por lo que nos dara un mejor resultado
>[!WARNING] Aspecto a considerar
> La capacidad calorífica siempre estará definida dentro de un rango de temperatura. En los cálculos, es más preciso utilizar el polinomio de capacidad calorífica proporcionado por la bibliografía, si está disponible, en lugar de uno calculado a partir de datos experimentales. Además, el polinomio calculado con datos experimentales será más confiable que aquel generado mediante modelos de contribución de grupos.

# Ejercicio propuesto:
- Comparar el valor de la capacidad calorífica calculada con Chao's con la primera presión tabulada de la bibliografía para cada T y ver cuál es el error respecto del último.
  
- Calcular y representar la capacidad calorífica como gas ideal y la entalpía, entropía y energía de Gibbs de la sustancia asignada.
   1. Cálculo: entre 300 y 1500 K, cada 100 K
   2. Gráfica:
       - entre 300 y 1500 K, cada 10 K
       - H: color rojo
       - S: color azul
       - G: color negro
- Calcular el polinomio de la capacidad calorífica utilizando modelos de contribución de grupos.
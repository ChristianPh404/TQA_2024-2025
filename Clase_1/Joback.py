import numpy as np
from IPython.display import display, Math
import pandas as pd
# Crear un diccionario para almacenar los grupos químicos y sus valores
grupos_químicos = {}

# Lista de grupos químicos necesarios
grupos_necesarios = [
    '-CH3', '-CH2-', '>CH-', '>C<', '=CH2', '=CH-', '=C<', '=C=', '≡CH', '≡C-', '-CH2- ring', '>CH- ring',
    # el simbolo ≡ deberia salir con $\equiv pero no se muestra en pantalla
    '>C< ring', '=CH- ring', '=C< ring', '-F', '-Cl', '-Br', '-I', '-0H (alcohol)', '-0H (phenol)', '-O- (nonring)',
    '-O- (ring)', '>C=O (nonring)', '>C=O (ring)', 'O=CH- (aldehyde)', '-COOH (acid)', '-COO- (ester)', '=O (except -NO2)',
    '-NH2', '>NH (nonring)', '>NH (ring)', '>N- (nonring)', '-N= (nonring)', '-N= (ring)', '=NH', '-CN', '-NO2', '-SH',
    '-S- (nonring)', '-S- (ring)'
]
# en nuestro caso es 1 grupo -CH3, 1 =CH2, 1 -CH=,3 -CH2- es decir 1,3, , ,1,1,exit
# Inicializar el contador de grupos químicos seleccionados
grupos_seleccionados = 0

# Crear un diccionario con todas las claves predeterminadas establecidas en 0
grupos_químicos = {grupo: 0 for grupo in grupos_necesarios}

# Pedir al usuario que ingrese valores para los grupos químicos
for i in range(len(grupos_necesarios)):
    grupo_quimico = grupos_necesarios[i]
    valor = input(f'Introducir cantidad de "{
                  grupo_quimico}":, pulsar enter para que cuente como 0 o "exit" para finalizar: ')

    # Si presionas Enter sin ingresar un valor, se entenderá como 0.
    if valor == '':
        valor = 0
    elif valor.lower() == 'exit':
        # Establecer el valor del grupo químico actual en 0 y los grupos restantes en 0.
        grupos_químicos[grupo_quimico] = 0
        for j in range(i + 1, len(grupos_necesarios)):
            grupos_químicos[grupos_necesarios[j]] = 0
        break
    else:
        # Intenta convertir el valor ingresado en un número.
        try:
            valor = float(valor)
        except ValueError:
            print('Valor no válido. Intente de nuevo.')
            continue

    grupos_químicos[grupo_quimico] = valor
    grupos_seleccionados += 1

print("grupos que contribuyen:")
for grupo, valor in grupos_químicos.items():
    if valor > 0:
        print(f'{grupo}: {valor}')

# vectores Joback (los vectores no han sido modificados)
Tc = np.array([0.0141, 0.0189, 0.0164, 0.0067, 0.0113, 0.0129, 0.0117, 0.0026, 0.0027, 0.0020, 0.0100, 0.0122, 0.0042, 0.0082, 0.0143,
               0.0111, 0.0105, 0.0133, 0.0068, 0.0741, 0.0240, 0.0168, 0.0098, 0.0380, 0.0284, 0.0379, 0.0791, 0.0481,
               0.0143, 0.0243, 0.0295, 0.0130, 0.0169, 0.0255, 0.0085, None, 0.0496, 0.0437, 0.0031, 0.0119, 0.0019])
Pc = np.array([-0.0012, 0, 0.0020, 0.0043, -0.0028, -0.0006, 0.0011, 0.0028, -0.0008, 0.0016, 0.0025, 0.0004, 0.0061,
               0.0011, 0.0008, -0.0057, -0.0049, 0.0057, -
               0.0034, 0.0112, 0.0184, 0.0015, 0.0048, 0.0031, 0.0028, 0.0030,
               0.0077, 0.0005, 0.0101, 0.0109, 0.0077, 0.0114, 0.0074, -0.0099, 0.0076, None, -0.0101, 0.0064, 0.0084, 0.0049, 0.0051])
Vc = np.array([65, 56, 41, 27, 56, 46, 38, 36, 46, 37, 48, 38, 27, 41, 32, 27, 58, 71, 97, 28, -25, 18, 13, 62, 55, 82, 89, 82, 36, 38, 35, 29, 9, None,
               34, None, 91, 91, 63, 54, 38])
Tb = np.array([23.58, 22.88, 21.74, 18.25, 18.18, 24.96, 24.14, 26.15, 9.20, 27.38, 27.15, 21.78, 21.32,
               26.73, 31.01, -0.03, 38.13, 66.86, 93.84, 92.88,
               76.34, 22.42, 31.22, 76.75, 94.97, 72.24, 169.09, 81.10, -
               10.50, 73.23, 50.17, 52.82, 11.74,
               74.60, 57.55, 83.08, 125.66, 152.54, 63.56,
               68.78, 52.10])
Tf = np.array([-5.10, 11.27, 12.64, 46.43, -4.32, 8.73, 11.14, 17.78, -11.18, 64.32, 7.75, 19.88, 60.15, 8.13, 37.02,
               -15.78, 13.55, 43.43, 41.69, 44.45,
               82.83, 22.23, 23.05, 61.20, 75.97, 36.90, 155.50, 53.60, 2.08, 66.89, 52.66, 101.51, 48.84, None,
               68.40, 68.91, 59.89, 127.24, 20.09, 34.40, 79.93])
AHF = np.array([-76.45, -20.64, 29.89, 82.23, -9.63, 37.97, 83.99, 142.14, 79.30, 115.51, -26.80, 8.67, 79.72, 2.09,
                46.43, -251.92, -71.55, -29.48, 21.06, -208.04,
                -221.65, -132.22, -138.16, -133.22, -164.50, -162.03, -
                426.72, -337.92, -247.61, -22.02, 53.47, 31.65,
                123.34, 23.61, 55.52, 93.70, 88.43, -66.57,
                -17.33, 41.87, 39.10])
AGF = np.array([-43.96, 8.42, 58.36, 116.02, 3.77, 48.53, 92.36, 136.70, 77.71, 109.82, -3.68, 40.99, 87.88, 11.30,
                54.05, -247.19, -64.31, -38.06, 5.74, -189.20,
                -197.37, -105.00, -98.22, -120.50, -126.27, -
                143.48, -387.87, -301.95, -250.83, 14.07, 89.39,
                75.61, 163.16, None, 79.93, 119.66, 89.22, -16.83,
                -22.99, 33.12, 27.76])
IGCa = np.array([1.95E1, -9.09E-1, -2.30E+1, -6.62E+1, 2.36E+1, -8.00, -2.81E1, 2.74E1, 2.45E1, 7.87, -6.03,
                 -2.05E+1, -9.09E+1, -2.14, -8.25, 2.65E+1, 3.33E+1,
                 2.86E+1, 3.21E1, 2.57E+1, -
                 2.81, 2.55E+1, 1.22E+1, 6.45, 3.04E+1, 3.09E+1, 2.41E+1, 2.45E+1,
                 6.82, 2.69E+1, -1.21, 1.18E+1, -3.11E+1, None,
                 8.83, 5.69, 3.65E+1, 2.59E+1, 3.53E+1, 1.96E+1, 1.67E+1])
IGCb = np.array([-8.08E-3, 9.50E-2, 2.04E-1, 4.27E-1, -3.81E-2, 1.05E-1, 2.08E-1, -5.57E-2, -2.71E-2, 2.01E-2,
                 8.54E-2, 1.62E-1, 5.57E-1, 5.74E-2, 1.01E-1, -9.13E-2,
                 -9.63E-2, -6.49E-2, -6.41E-2, -6.91E-2, 1.11E-1, -
                 6.32E-2, -1.26E-2, 6.70E-2, -8.29E-2, -3.36E-2,
                 4.27E-2, 4.02E-2, 1.96E-2, 4.12E-2, 7.62E-2,
                 -2.30E-2, 2.27E-1, None, -3.84E-3, -4.12E-3, -7.33E-2, -3.74E-3, -7.58E-2, -5.61E-3, 4.81E-3])
IGCc = np.array([1.53E-4, -5.44E-5, -2.65E-4, -6.41E-4, 1.72E-4, -9.63E-5, -3.06E-4, 1.01E-4, 1.11E-4, -8.33E-6,
                 -8.00E-6, -1.6E-4, -9.00E-4, -1.64E-6, -1.42E-4,
                 1.91E-4, 1.87E-4, 1.36E-4, 1.26E-4, 1.77E-4, -
                 1.16E-4, 1.11E-4, 6.03E-5, -3.57E-5, 2.36E-4, 1.60E-4,
                 8.04E-5, 4.02E-5, 1.27E-5, 1.64E-4, -4.86E-5,
                 1.07E-4, -3.20E-4, None, 4.35E-5, 1.28E-4, 1.84E-46, 1.29E-4, 1.85E-4, 4.02E-5, 2.77E-5])
IGCd = np.array([-9.67E-8, 1.19E-8, 1.20E-7, 3.01E-7, -1.03E-7, 3.56E-8, 1.46E-7, -5.02E-8, -6.78E-8, 1.39E-9, -1.80E-8,
                 6.24E-8, 3.06E-7, 2.24E-9, 2.39E-8, -3.44E-8,
                 -5.10E-8, -3.38E-8, -2.94E-8, -4.53E-8, -1.12E-7, -
                 3.18E-8, -6.94E-9, 2.68E-8, -4.20E-8, -1.19E-8,
                 -1.21E-8, 3.92E-9, -2.02E-8, -5.90E-8, -5.88E-9,
                 4.80E-8, -3.60E-7, None, 8.22E-9, 7.04E-9, -5.48E-8, 6.10E-9, -7.19E-8, 8.04E-9, -1.24E-8])
AHV = np.array([2.373, 2.226, 1.691, 0.636, 1.724, 2.205, 2.138, 2.661, 1.155, 3.302, 2.398, 1.942, 0.644, 2.544, 3.059, -0.670, 4.532,
                6.582, 9.520, 16.826, 12.499, 2.410, 4.682, 8.972,
                6.645, 9.093, 19.537, 9.633, 5.909, 10.788, 6.436, 6.930, 1.896, 3.335, 6.528, 12.169, 12.851, 16.738, 6.884, 6.817, 5.984])
AHfl = np.array([0.908, 2.590, 0.749, -1.460, -0.473, 2.691, 3.063, 4.720, 2.322, 4.151, 0.490, 3.243, -1.373, 1.101, 2.394, 1.398, 2.515,
                 3.603, 2.724, 2.406, 4.490, 1.188, 5.879, 4.189,
                 None, 3.197, 11.051, 6.959, 3.624, 3.515, 5.009, 7.490, 4.703, None, 3.649, None, 2.414, 9.679, 2.360, 4.130, 1.557])
na = np.array([548.29, 94.16, -322.15, -573.56, 495.01, 82.28, None, None, None, None, 307.53, -394.29, None, 259.65, -245.74, None, 625.45,
               738.91, 809.55, 2173.72, 3018.17, 122.09,
               440.24, 340.35, None, 740.92, 1317.23, 483.88, 675.24, None, None, None, None, None, None, None, None, None, None, None, None])
nb = np.array([-1.719, -0.199, 1.187, 2.307, -1.539, -0.242, None, None, None, None, -0.798, 1.251, None, -0.702, 0.912, None, -1.814, -2.038,
               -2.224, -5.057, -7.314, -0.386, -0.953,
               -0.350, None, -1.713, -2.578, -0.966, -1.340, None, None, None, None, None, None, None, None, None, None, None, None])
NA = np.array([4, 3, 2, 1, 3, 2, 1, 1, 2, 1, 3, 2, 1, 2, 1, 1, 1, 1, 1, 2, 2, 1,
              1, 2, 2, 3, 4, 3, 1, 3, 2, 2, 1, 1, 1, 2, 2, 3, 2, 1, 1])  # Numero de atomos
MW = np.array([15.03461, 14.02664, 13.01867, 12.0107, 14.02664, 13.01867, 12.0107, 12.0107, 13.01867, 12.0107, 14.02664, 13.01867, 12.0107,
               13.01867, 12.0107, 18.9984032, 35.453,
               79.909, 126.90447, 17.00737, 17.00737, 15.9994, 15.9994, 28.0101, 28.0101, 29.01807, 45.01747, 44.0095, 15.9994, 16.02294,
               15.01497, 15.01497, 14.007, 14.007, 14.007,
               15.01497, 26.0177, 46.0058, 33.07297, 32.065, 32.065])  # masas moleculares
# Crear una función para reemplazar None por 0.00 en un vector


def replace_none_with_zero(vector):
    return np.array([0.00 if x is None else x for x in vector])


# Reemplazar None en todos los vectores
Tc = replace_none_with_zero(Tc)
Pc = replace_none_with_zero(Pc)
Vc = replace_none_with_zero(Vc)
Tb = replace_none_with_zero(Tb)
Tf = replace_none_with_zero(Tf)
AHF = replace_none_with_zero(AHF)
AGF = replace_none_with_zero(AGF)
IGCa = replace_none_with_zero(IGCa)
IGCb = replace_none_with_zero(IGCb)
IGCc = replace_none_with_zero(IGCc)
IGCd = replace_none_with_zero(IGCd)
AHV = replace_none_with_zero(AHV)
AHfl = replace_none_with_zero(AHfl)
na = replace_none_with_zero(na)
nb = replace_none_with_zero(nb)

# Crear un diccionario con las propiedades y sus valores
suma_contribuciones = {
    '$\mathrm{T_b}$ (K)': 198.2 + np.sum(Tb * np.array([grupos_químicos[grupo] for grupo in grupos_necesarios])),
    '$\mathrm{T_c}$ (K)': (198.2 + np.sum(Tb * np.array([grupos_químicos[grupo] for grupo in grupos_necesarios]))) *
    ((0.584 + (0.965 * np.sum(Tc * np.array([grupos_químicos[grupo] for grupo in grupos_necesarios]))) -
      (np.sum(Tc * np.array([grupos_químicos[grupo] for grupo in grupos_necesarios])))**2))**(-1),
    '$\mathrm{P_c}$ (bar)': (0.113 + (0.0032 * np.sum(NA * np.array([grupos_químicos[grupo] for grupo in grupos_necesarios]))) -
                             # error
                             (np.sum(Pc * np.array([grupos_químicos[grupo] for grupo in grupos_necesarios]))))**(-2),
    '$\mathrm{V_c}$ $\mathrm{(cm^3/mol)}$': np.sum(Vc * np.array([grupos_químicos[grupo] for grupo in grupos_necesarios])) + 17.5,
    '$\mathrm{T_f}$ (K)': 122.5 + np.sum(Tf * np.array([grupos_químicos[grupo] for grupo in grupos_necesarios])),
    'ΔH$\mathrm{_{f,298}^°}$ (KJ/mol)': 68.29 + np.sum(AHF * np.array([grupos_químicos[grupo] for grupo in grupos_necesarios])),
    'ΔG$\mathrm{_{f,298}^°}$ (KJ/mol)': 53.88 + np.sum(AGF * np.array([grupos_químicos[grupo] for grupo in grupos_necesarios])),
    'ΔH$\mathrm{_{v,b}}$ (KJ/mol)': 15.3 + np.sum(AHV * np.array([grupos_químicos[grupo] for grupo in grupos_necesarios])),
    'ΔH$\mathrm{_f}$ (KJ/mol)': 0.88 + np.sum(AHfl * np.array([grupos_químicos[grupo] for grupo in grupos_necesarios])),
    'IGCa': -37.93 + np.sum(IGCa * np.array([grupos_químicos[grupo] for grupo in grupos_necesarios])),
    'IGCb': 0.210 + np.sum(IGCb * np.array([grupos_químicos[grupo] for grupo in grupos_necesarios])),
    'IGCc': -3.91e-4 + np.sum(IGCc * np.array([grupos_químicos[grupo] for grupo in grupos_necesarios])),
    'IGCd': 2.06e-7 + np.sum(IGCd * np.array([grupos_químicos[grupo] for grupo in grupos_necesarios])),
    'η$\mathrm{_a }$ ($ \mathrm{ N \cdot s/m^2}$)': np.sum(na * np.array([grupos_químicos[grupo] for grupo in grupos_necesarios])),
    'η$\mathrm{_b} $ ($\mathrm{ N s/m^2}$)': np.sum(nb * np.array([grupos_químicos[grupo] for grupo in grupos_necesarios])),
}
# Crear un DataFrame de una fila con los valores de las propiedades
df_suma_contribuciones = pd.DataFrame([suma_contribuciones])
# calcular columna de Zc en el dataframe
dataframe2 = (df_suma_contribuciones.iloc[:, 2] * 1e5 * df_suma_contribuciones.iloc[:, 3]) / (
    df_suma_contribuciones.iloc[:, 1] * 8.314*1e6)
dataframe2 = dataframe2.rename('Zc')
# calcular columna de  en el dataframe
Densidad_critica = np.sum(MW * np.array([grupos_químicos[grupo]
                          for grupo in grupos_necesarios]))/(df_suma_contribuciones.iloc[:, 3])
Densidad_critica = dataframe2.rename('$ρ_c$ (kg/m³)')
# # Concatenar tabla joback y zc
# df4 = pd.concat([df_suma_contribuciones, dataframe2], axis=1)

# # Concatenar tabla anterior con tabla de densidad critica
# df3 = pd.concat([df4, Densidad_critica], axis=1)

# # Redondear todas las columnas (excepto 'IGCc' y 'IGCd') a 3 decimales
# columnas_redondear = df3.columns.difference(['IGCc', 'IGCd'])
# df3[columnas_redondear] = df3[columnas_redondear].round(3)

# # Aplicar formato científico a las columnas 'IGCc' y 'IGCd' en el estilo
# df3.style.format({'IGCc': '{:e}', 'IGCd': '{:e}'}).hide(axis="index")


# Concatenar tabla joback y zc
df4 = pd.concat([df_suma_contribuciones, dataframe2], axis=1)

# Concatenar tabla anterior con tabla de densidad crítica
df3 = pd.concat([df4, Densidad_critica], axis=1)

# Redondear todas las columnas (excepto 'IGCc' y 'IGCd') a 3 decimales
columnas_redondear = df3.columns.difference(['IGCc', 'IGCd'])
df3[columnas_redondear] = df3[columnas_redondear].round(3)

# Formatear 'IGCc' y 'IGCd' a notación científica
df3['IGCc'] = df3['IGCc'].apply(lambda x: "{:e}".format(x))
df3['IGCd'] = df3['IGCd'].apply(lambda x: "{:e}".format(x))

# Establecer la opción de visualización para mostrar solo 3 decimales
pd.set_option('display.float_format', '{:.3f}'.format)

# Mostrar el DataFrame
df3
# en nuestro caso es 1 grupo -CH3, 1 =CH2, 1 -CH=,3 -CH2- es decir 1,3, , ,1,1,exit

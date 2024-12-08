# Inclusión de dependencias del proyecto...
import matplotlib.pyplot as plt
import random
import math

# Parámetros del algoritmo PSO
max_iteraciones = 5  # Número máximo de iteraciones
tamaño_población = 5  # Tamaño del enjambre (número de partículas)
w = 0.9              # Peso de inercia
alpha = 0.6          # Factor cognitivo (aprendizaje individual)
beta = 0.6           # Factor social (aprendizaje grupal)

# Definición de variables globales [Importante: otras variables y la ejecución del algoritmo se encuentran al final de este archivo]...
nombres = ['inversion1', 'inversion2', 'inversion3', 'inversion4', 'inversion5', 'inversion6', 'inversion7']
beneficios = [35, 85, 135, 10, 25, 2, 94]
pesos = [8, 7, 8, 9, 7, 9, 9]
maxPeso = 25

random_vector = [random.random() for _ in range(700)] #son 525 con esta configuracion
contador = 0

# Función que intentamos maximizar...
def fncMax(x):
    t = fncSumaBeneficio(x)
    return t + fncSumaPeso(x, t)


def fncSumaBeneficio(x):
    total = 0
    for i in range(len(x)):
        total += x[i] * beneficios[i]  # Cantidad * Beneficio
    return total


def fncSumaPeso(x, penalizacion):
    total = 0
    for i in range(len(x)):
        total += x[i] * pesos[i]  # Cantidad * Peso

    if total <= maxPeso:
        if total <= penalizacion:
            return penalizacion - total
        else:
            return 0
    else:
        return -penalizacion

    """
        Si el peso excede el máximo permitido (maxPeso),
        la función devuelve una penalización negativa equivalente al valor de la primera función,
        anulando el valor actual para evitar que sea considerado...
    """


# Clase para representar las partículas...
import numpy as np

class Particula:
    def __init__(self, valoresIniciales):
        self.posicion = []       # Posición de la partícula
        self.velocidad = []      # Velocidad de la partícula
        self.pBest = []          # Mejor posición personal
        self.pBestAproximacion = -1  # Mejor aproximación personal
        self.aproximacion = -1       # Aproximación actual

        for i in range(numVariables):
            self.velocidad.append(random.uniform(-1, 1))
            self.posicion.append(valoresIniciales[i])

    # Calcula la aptitud de la partícula...
    def calcular(self, funcion):
        self.aproximacion = funcion(self.posicion)

        # Actualiza el mejor valor personal si es necesario...
        if self.aproximacion > self.pBestAproximacion or self.pBestAproximacion == -1:
            self.pBest = list(self.posicion)
            self.pBestAproximacion = self.aproximacion

    # Actualiza la velocidad de la partícula...
    def actualizar_velocidad(self, mejorPosicionGrupo, random_vector):
        global w,alpha,beta

        for i in range(numVariables):
            global contador
            r1 = random_vector[contador]  # Aleatorio predefinido para peso cognitivo
            contador +=1
            r2 = random_vector[contador]  # Aleatorio predefinido para peso social
            contador +=1

            velocidadCognitiva = alpha * r1 * (self.pBest[i] - self.posicion[i])
            velocidadSocial = beta * r2 * (mejorPosicionGrupo[i] - self.posicion[i])
            self.velocidad[i] = w * self.velocidad[i] + velocidadCognitiva + velocidadSocial

    # Actualiza la posición basada en la nueva velocidad (binaria)...
    def actualizar_posicion(self, limites):
        for i in range(numVariables):
            global contador
            probabilidad = 1 / (1 + math.exp(-self.velocidad[i]))  # Sigmoid para convertir a probabilidad
            self.posicion[i] = 1 if random_vector[contador] < probabilidad else 0
            contador +=1


class PSO:
    historialBeneficios, historialPesos, mejorPosicionGrupo, mejorAproximacionGrupo = [], [], [], -1

    def __init__(self, funcion, valoresIniciales, limites, tamanoGrupo, maxIter, random_vector, mostrarProgreso=True):
        global numVariables

        numVariables = len(valoresIniciales)
        self.mejorAproximacionGrupo = -1  
        self.mejorPosicionGrupo = []  

        # Inicialización del enjambre...
        enjambre = []
        for i in range(tamanoGrupo):
            enjambre.append(Particula(valoresIniciales))

        # Ciclo de optimización...
        for iteracion in range(maxIter):
            # Evaluación de cada partícula...
            for particula in enjambre:
                particula.calcular(funcion)

                # Actualización de la mejor posición global si es necesario...
                if particula.aproximacion > self.mejorAproximacionGrupo or self.mejorAproximacionGrupo == -1:
                    self.mejorPosicionGrupo = list(particula.posicion)
                    self.mejorAproximacionGrupo = float(particula.aproximacion)

            # Actualización de velocidades y posiciones...
            for particula in enjambre:
                particula.actualizar_velocidad(self.mejorPosicionGrupo, random_vector)
                particula.actualizar_posicion(limites)

            # Registro de beneficios y pesos...
            beneficioTotal = sum(self.mejorPosicionGrupo[i] * beneficios[i] for i in range(numVariables))
            pesoTotal = sum(self.mejorPosicionGrupo[i] * pesos[i] for i in range(numVariables))
            self.historialBeneficios.append(beneficioTotal)
            self.historialPesos.append(pesoTotal)

            if mostrarProgreso:
                print(f"Iteración {iteracion + 1}: {self.mejorPosicionGrupo}")

    def imprimir_resultados(self):
        print('\nRESULTADOS:\n')
        beneficioTotal = 0
        pesoTotal = 0
        for i, nombre in enumerate(nombres):
            print(f"{nombre}: {self.mejorPosicionGrupo[i]} unidades")
            beneficioTotal += self.mejorPosicionGrupo[i] * beneficios[i]
            pesoTotal += self.mejorPosicionGrupo[i] * pesos[i]
        print('#' * 50)
        print(f"Beneficio obtenido: {beneficioTotal}, Peso total: {pesoTotal}")

    def graficar_resultados(self, nombreArchivo=''):
        plt.plot(self.historialPesos, self.historialBeneficios)
        plt.xlabel('Peso (kg)')
        plt.ylabel('Beneficio obtenido')
        plt.title('Gráfico Beneficio-Peso')
        plt.grid(True)

        if nombreArchivo:
            plt.savefig(f"{nombreArchivo}.png")

        plt.show()


# Configuración inicial y ejecución del algoritmo...
valoresIniciales = [0] * len(nombres)  # Comienza sin objetos seleccionados
limites = [(0, 1)] * len(nombres)  # Límites binarios para todos los objetos

# Vector de elementos aleatorios predefinidos
#random_vector = [[random.random(), random.random()] for _ in range(len(nombres))]

print(f"vercor randomico: \t", random_vector)

print("[nombre_objeto: limite_inferior - limite_superior]\n")
for i, nombre in enumerate(nombres):
    print(f"{nombre}: {limites[i][0]} - {limites[i][1]}")
print(f"\nUn total de {len(nombres)} variables...\n")

pso = PSO(
    funcion=fncMax,
    valoresIniciales=valoresIniciales,
    limites=limites,
    tamanoGrupo=5,  # popSize
    maxIter=5,  # MaxIter
    random_vector=random_vector,
    mostrarProgreso=True
)
pso.imprimir_resultados()
pso.graficar_resultados(nombreArchivo='resultado')
print(f"contador: {contador}")
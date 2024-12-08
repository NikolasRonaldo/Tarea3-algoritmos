# PSEUDOCODIGO:

# Inicialización de parámetros
max_iteraciones <- 5
tamaño_población <- 5
w <- 0.9
alpha <- 0.6
beta <- 0.6

nombres <- ["Televisor", "Cámara", "Proyector", "Walkman", "Radio", "Teléfono Móvil", "Portátil"]
beneficios <- [35, 85, 135, 10, 25, 2, 94]
pesos <- [8, 7, 8, 9, 7, 9, 9]
maxPeso <- 25

random_vector <- generar 700 números aleatorios entre 0 y 1
contador <- 0

# Definición de funciones
fncMax(x):
    beneficio <- calcular suma de beneficios para x
    peso <- calcular suma de pesos para x
    si peso <= maxPeso:
        retornar beneficio + (penalización si aplica)
    sino:
        retornar -penalización

fncSumaBeneficio(x):
    retornar suma( x[i] * beneficios[i] )

fncSumaPeso(x, penalizacion):
    peso <- suma( x[i] * pesos[i] )
    si peso <= maxPeso:
        si peso <= penalizacion:
            retornar penalizacion - peso
        sino:
            retornar 0
    sino:
        retornar -penalizacion

# Clase Particula
Clase Particula:
    inicializar():
        posicion <- vector binario inicial
        velocidad <- generar velocidades aleatorias
        pBest <- posicion inicial
        pBestAproximacion <- -1
        aproximacion <- -1

    calcular(funcion):
        aproximacion <- funcion(posicion)
        si aproximacion > pBestAproximacion:
            pBest <- posicion
            pBestAproximacion <- aproximacion

    actualizar_velocidad(mejorPosicionGrupo, random_vector):
        para cada variable i:
            r1 <- random_vector[contador++]
            r2 <- random_vector[contador++]
            velocidadCognitiva <- alpha * r1 * (pBest[i] - posicion[i])
            velocidadSocial <- beta * r2 * (mejorPosicionGrupo[i] - posicion[i])
            velocidad[i] <- w * velocidad[i] + velocidadCognitiva + velocidadSocial

    actualizar_posicion(limites):
        para cada variable i:
            probabilidad <- sigmoid(velocidad[i])
            posicion[i] <- 1 si random_vector[contador++] < probabilidad sino 0

# Clase PSO
Clase PSO:
    inicializar(funcion, valoresIniciales, limites, tamañoGrupo, maxIter, random_vector):
        mejorAproximacionGrupo <- -1
        mejorPosicionGrupo <- vector vacío
        enjambre <- lista de partículas inicializadas

        para iteracion en 1 hasta maxIter:
            para cada particula en enjambre:
                particula.calcular(funcion)
                si particula.aproximacion > mejorAproximacionGrupo:
                    mejorPosicionGrupo <- particula.posicion
                    mejorAproximacionGrupo <- particula.aproximacion

            para cada particula en enjambre:
                particula.actualizar_velocidad(mejorPosicionGrupo, random_vector)
                particula.actualizar_posicion(limites)

            registrar beneficios y pesos del mejor grupo

    imprimir_resultados():
        mostrar beneficios y pesos totales
        mostrar objetos seleccionados

    graficar_resultados(nombreArchivo):
        graficar historial de beneficios vs pesos

# Ejecución
valoresIniciales <- vector de ceros (sin objetos seleccionados)
limites <- [(0, 1) para cada objeto]

pso <- nuevo PSO(
    funcion=fncMax,
    valoresIniciales=valoresIniciales,
    limites=limites,
    tamañoGrupo=5,
    maxIter=5,
    random_vector=random_vector
)

pso.imprimir_resultados()
pso.graficar_resultados("resultado")

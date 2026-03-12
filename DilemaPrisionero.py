

import random

"""
Nmero de jugadas anteriores
"""
MEMORIA = 5

"""
Cantidad de veces que se juega
"""
ITERACIONES_PARTIDA = 30

"""
Tabla de puntos:
    C (cooperate) = 3
    L (low) = 0
    H (high) = 5
    D (defect) = 1

L < D < C < H
H + L <= 2*C
"""
C = 3
L = 0
H = 5
D = 1

"""
Parametros del algoritmo genético
"""
TAM_POBLACION = 100
GENERACIONES = 500
PC = 0.7
PM = 0.01
TAM_TORNEO = 3
K_RIVALES = 20
SEED = 1
ELITISMO = True

"""
Nombres de movimientos
    C = Cooperar
    A = Abandonar
"""
nombres_movimientos = {"C": "C", "A": "A"}


# LOGICA

def calcular_puntaje(mov_propio, mov_oponente):
    """
    Devuelve los puntos del jugador.
        C = Cooperar
        A = Abandonar
    """
    if mov_propio == "C" and mov_oponente == "C": # CC = C 
        return C
    elif mov_propio == "C" and mov_oponente == "A": # CA = L 
        return L
    elif mov_propio == "A" and mov_oponente == "C": # AC = H 
        return H
    else: # AA = D 
        return D


LONGITUD_CROMOSOMA = 2 * MEMORIA + (4 ** MEMORIA)


def bit_a_accion(bit):
    """
    Convierte un bit a movimiento.
        '0' -> 'A'
        '1' -> 'C'
    """
    return "C" if bit == "1" else "A"


def historia_a_indice(historia):

    indice = 0
    for k, (propia, oponente) in enumerate(historia):
        if   propia == "A" and oponente == "A": valor = 0
        elif propia == "A" and oponente == "C": valor = 1
        elif propia == "C" and oponente == "A": valor = 2
        else:                                    valor = 3   # CC
        indice += valor * (4 ** k)
    return indice


def decidir(individuo, historia):

    if len(historia) < MEMORIA:
        bit_pos = len(historia) * 2
        return bit_a_accion(individuo[bit_pos])
    else:
        offset = 2 * MEMORIA
        idx    = historia_a_indice(historia[-MEMORIA:])
        return bit_a_accion(individuo[offset + idx])


# CREAR POBLACION

def crear_individuo():
    """
    Genera un individuo
    """
    return "".join(str(random.randint(0, 1)) for _ in range(LONGITUD_CROMOSOMA))


def generar_poblacion(tam=TAM_POBLACION):
    """
    Genera una poblacion
    """
    return [crear_individuo() for _ in range(tam)]


# JUGAR

def jugar_partida(individuo_1, individuo_2, rondas=ITERACIONES_PARTIDA, verbose=False):

    historia_1 = []
    historia_2 = []

    """
    Puntuaciones
    """
    puntuacion_1 = 0
    puntuacion_2 = 0

    """
    Historial de movimientos
    """
    historial_1 = []
    historial_2 = []

    if verbose:
        print(f"\n{'Ronda':<8} {'J1':^6} {'J2':^6} {'Pts J1':^8} {'Pts J2':^8} {'Tot J1':^8} {'Tot J2':^8}")
        print("----------------------------------------------------------")

    for ronda in range(1, rondas + 1):

        """
        Decidir movimientos
        """
        mov_1 = decidir(individuo_1, historia_1)
        mov_2 = decidir(individuo_2, historia_2)

        """
        Calcular puntos de esta ronda
        """
        pts_1 = calcular_puntaje(mov_1, mov_2)
        pts_2 = calcular_puntaje(mov_2, mov_1)

        """
        Sumar puntajes
        """
        puntuacion_1 += pts_1
        puntuacion_2 += pts_2

        """
        Guardar historial
        """
        historial_1.append(mov_1)
        historial_2.append(mov_2)

        historia_1.append((mov_1, mov_2))
        historia_2.append((mov_2, mov_1))

        if verbose:
            print(f"{ronda:<6} {mov_1:^6} {mov_2:^6} {pts_1:^8} {pts_2:^8} "
                  f"{puntuacion_1:^8} {puntuacion_2:^8}")

    if verbose:
        print("----------------------------------------------------------")
        print(f"\nHistorial J1: {' '.join(historial_1)}")
        print(f"Historial J2: {' '.join(historial_2)}")
        print(f"\nPuntuacion final  -  J1: {puntuacion_1}  |  J2: {puntuacion_2}")

    return puntuacion_1, puntuacion_2


# FITNESS

def calcular_fitness(individuo, poblacion, k_rivales=K_RIVALES):

    indices = random.sample(range(len(poblacion)), min(k_rivales, len(poblacion)))

    total = 0.0
    for idx in indices:
        rival = poblacion[idx]
        pts, _ = jugar_partida(individuo, rival)
        total += pts

    return total / len(indices)


# TORNEO

def seleccion_torneo(poblacion, fits, tam_torneo=TAM_TORNEO):

    seleccionados = []

    for _ in range(len(poblacion)):

        """
        Elegir participantes
        """
        participantes = random.sample(list(zip(poblacion, fits)), tam_torneo)

        """
        Seleccionar el mejor
        """
        ganador = max(participantes, key=lambda x: x[1])
        seleccionados.append(ganador[0])

    return seleccionados


# CROSSOVER

def crossover(padre_1, padre_2, pc=PC):

    if random.random() > pc:
        return padre_1, padre_2

    punto = random.randint(1, LONGITUD_CROMOSOMA - 1)

    hijo_1 = padre_1[:punto] + padre_2[punto:]
    hijo_2 = padre_2[:punto] + padre_1[punto:]

    return hijo_1, hijo_2


# MUTACION

def mutar(individuo, pm=PM):

    resultado = []

    for bit in individuo:
        if random.random() < pm:
            resultado.append("0" if bit == "1" else "1")
        else:
            resultado.append(bit)
    return "".join(resultado)


# EVOLUCION

def evolucionar(
    tam_poblacion = TAM_POBLACION,
    generaciones  = GENERACIONES,
    pc            = PC,
    pm            = PM,
    k_rivales     = K_RIVALES,
    tam_torneo    = TAM_TORNEO,
    seed          = SEED,
    elitismo      = ELITISMO,
):

    random.seed(seed)

    """
    Generar poblacion
    """
    poblacion = generar_poblacion(tam_poblacion)

    print(f"\n{'Gen':^6} {'Media':^10} {'Mejor fit':^12}")
    print("--------------------------------")

    for generacion in range(generaciones):

        """
        Calcular fitness
        """
        fits = [calcular_fitness(ind, poblacion, k_rivales) for ind in poblacion]

        idx_mejor = max(range(len(poblacion)), key=lambda i: fits[i])
        mejor     = poblacion[idx_mejor]
        mejor_fit = fits[idx_mejor]
        media_fit = sum(fits) / len(fits)

        if generacion % 10 == 0 or generacion == generaciones - 1:
            print(f"{generacion:^6} {media_fit:^10.2f} {mejor_fit:^12.2f}")

        """
        Selección por torneo
        """
        seleccionados = seleccion_torneo(poblacion, fits, tam_torneo)

        """
        Crear nueva generación
        """
        nueva_poblacion = []

        """
        Elitismo
        """
        if elitismo:
            nueva_poblacion.append(mejor)

        while len(nueva_poblacion) < tam_poblacion:

            padre_1 = random.choice(seleccionados)
            padre_2 = random.choice(seleccionados)

            """
            Crossover
            """
            hijo_1, hijo_2 = crossover(padre_1, padre_2, pc)

            """
            Mutación
            """
            hijo_1 = mutar(hijo_1, pm)
            hijo_2 = mutar(hijo_2, pm)

            nueva_poblacion.append(hijo_1)
            if len(nueva_poblacion) < tam_poblacion:
                nueva_poblacion.append(hijo_2)

        poblacion = nueva_poblacion

    print("--------------------------------")

    """
    Evaluar y devolver el mejor individuo
    """
    fits     = [calcular_fitness(ind, poblacion, k_rivales) for ind in poblacion]
    idx_mejor = max(range(len(poblacion)), key=lambda i: fits[i])

    return poblacion[idx_mejor], fits[idx_mejor]


# ESTRATEGIAS

def crear_siempre_cooperar():
    return "1" * LONGITUD_CROMOSOMA

def crear_siempre_abandonar():
    return "0" * LONGITUD_CROMOSOMA

def crear_tit_for_tat():

    cromosoma = ["0"] * LONGITUD_CROMOSOMA

    for i in range(MEMORIA):
        cromosoma[i * 2] = "1"

    offset = 2 * MEMORIA
    for i in range(4 ** MEMORIA):
        ultima_oponente = (i % 4) // 2   # 0 si oponente jugó A, 1 si jugó C
        cromosoma[offset + i] = "1" if ultima_oponente == 1 else "0"

    return "".join(cromosoma)

"""
FALTA EP
"""

# MAIN

if __name__ == "__main__":

    print("\nDILEMA DEL PRISIONERO")

    mejor_individuo, mejor_fitness = evolucionar()

    print(f"\nMEJOR INDIVIDUO: {round(mejor_fitness, 2)}")
    print(f"Cromosoma: {mejor_individuo}")

    estrategias = {
        "Mejor AG"         : mejor_individuo,
        "Siempre Cooperar" : crear_siempre_cooperar(),
        "Siempre Abandonar": crear_siempre_abandonar(),
        "Tit-For-Tat"      : crear_tit_for_tat(),
    }

    puntuaciones_totales = {nombre: 0 for nombre in estrategias}

    print("\n")

    for nombre_1, est_1 in estrategias.items():
        for nombre_2, est_2 in estrategias.items():
            if nombre_1 == nombre_2:
                continue
            pts_1, pts_2 = jugar_partida(est_1, est_2)
            puntuaciones_totales[nombre_1] += pts_1
            print(f"{nombre_1:<20} vs {nombre_2:<20}  ->  {pts_1} - {pts_2}")

    print("\n")
    
    for nombre, total in sorted(puntuaciones_totales.items(), key=lambda x: x[1], reverse=True):
        print(f"  {nombre:<22} {total} puntos")
        
    puntuaciones_totales = {nombre: 0 for nombre in estrategias}

    jugar_partida(mejor_individuo, crear_siempre_abandonar(), rondas=10, verbose=True)
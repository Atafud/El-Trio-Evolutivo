
import numpy as np
import matplotlib.pyplot as plt
import random

class AG_MaximizarUnos:
    def __init__(self, tam_pob=100, long_crom=100, generaciones=100, pc=0.7, pm=0.01, elites=2):
        self.tam_pob = tam_pob
        self.long_crom = long_crom
        self.generaciones = generaciones
        self.pc = pc
        self.pm = pm
        self.elites = elites
        self.historial = {'media': [], 'mejor': [], 'peor': []}
    
    # Crea una matriz aleatoria de 0s y 1s (poblacion*genes)
    def generar_poblacion(self):
        return np.random.randint(0, 2, (self.tam_pob, self.long_crom))
    
    # Calcular cuantos 1s tiene un cromosoma
    def aptitud(self, cromosoma):
        return np.sum(cromosoma)
    
    # Suma todas las aptitudes
    # Calcula probabilidad de cada individuo: 
    # Elige aleatoriamente según esas probabilidades
    def seleccion_ruleta(self, poblacion, aptitudes):
        total = aptitudes.sum()
        prob = aptitudes / total
        idx = np.random.choice(len(poblacion), p=prob)
        return poblacion[idx].copy()
    
    def crossover(self, p1, p2):
        if random.random() < self.pc:
            punto = random.randint(1, self.long_crom - 1)
            h1 = np.concatenate([p1[:punto], p2[punto:]])
            h2 = np.concatenate([p2[:punto], p1[punto:]])
            return h1, h2
        return p1.copy(), p2.copy()
    
    def mutacion(self, cromosoma):
        for i in range(len(cromosoma)):
            if random.random() < self.pm:
                cromosoma[i] = 1 - cromosoma[i]
        return cromosoma
    
    def ejecutar(self):
        poblacion = self.generar_poblacion()
        
        for gen in range(self.generaciones):
            # Evaluar
            aptitudes = np.array([self.aptitud(ind) for ind in poblacion])
            
            # Estadísticas
            self.historial['media'].append(aptitudes.mean())
            self.historial['mejor'].append(aptitudes.max())
            self.historial['peor'].append(aptitudes.min())
            
            if gen % 20 == 0:
                print(f"Gen {gen}: Media={aptitudes.mean():.1f}, Mejor={aptitudes.max()}")
            
            # Nueva generación
            nueva_pob = []
            
            # Elitismo
            mejores_idx = np.argsort(aptitudes)[-self.elites:]
            for idx in mejores_idx:
                nueva_pob.append(poblacion[idx].copy())
            
            # Resto de la población
            while len(nueva_pob) < self.tam_pob:
                p1 = self.seleccion_ruleta(poblacion, aptitudes)
                p2 = self.seleccion_ruleta(poblacion, aptitudes)
                h1, h2 = self.crossover(p1, p2)
                h1 = self.mutacion(h1)
                h2 = self.mutacion(h2)
                nueva_pob.extend([h1, h2])
            
            poblacion = np.array(nueva_pob[:self.tam_pob])
        
        # Resultado final
        aptitudes = np.array([self.aptitud(ind) for ind in poblacion])
        mejor_idx = np.argmax(aptitudes)
        print(f"\nMejor: {aptitudes[mejor_idx]} unos de {self.long_crom}")
        
        return poblacion[mejor_idx], aptitudes[mejor_idx]
    
    def graficar(self):
        plt.figure(figsize=(10, 5))
        plt.plot(self.historial['media'], label='Media', linewidth=2)
        plt.plot(self.historial['mejor'], label='Mejor', linewidth=2)
        plt.plot(self.historial['peor'], label='Peor', alpha=0.5)
        plt.xlabel('Generación')
        plt.ylabel('Aptitud (número de 1s)')
        plt.title('Evolución del AG')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()


# ========== USO ==========

print("1. SIN CROSSOVER NI MUTACIÓN")
ag1 = AG_MaximizarUnos(pc=0, pm=0)
ag1.ejecutar()
ag1.graficar()

print("\n\n2. SOLO MUTACIÓN (pm=1)")
ag2 = AG_MaximizarUnos(pc=0, pm=1)
ag2.ejecutar()
ag2.graficar()

print("\n\n3. SOLO CROSSOVER (pc=1)")
ag3 = AG_MaximizarUnos(pc=1, pm=0)
ag3.ejecutar()
ag3.graficar()

print("\n\n4. CROSSOVER + MUTACIÓN")
ag4 = AG_MaximizarUnos(pc=0.7, pm=0.01)
ag4.ejecutar()
ag4.graficar()



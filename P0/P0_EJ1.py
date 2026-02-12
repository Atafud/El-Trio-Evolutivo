import numpy as np
import matplotlib.pyplot as plt
import random

class AG_Maximizar3s:
    def __init__(self, tam_pob=100, long_crom=20, generaciones=150, pc=0.8, pm=0.05, elites=5):
        self.tam_pob = tam_pob
        self.long_crom = long_crom
        self.generaciones = generaciones
        self.pc = pc
        self.pm = pm
        self.elites = elites
        self.alfabeto = list(range(10))
        self.historial = {'media': [], 'mejor': [], 'peor': []}
    
    def generar_poblacion(self):
        return np.random.choice(self.alfabeto, (self.tam_pob, self.long_crom))
    
    def aptitud(self, cromosoma):
        """Cuenta cuántos 3s hay en el cromosoma"""
        return np.sum(cromosoma == 3)
    
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
                cromosoma[i] = random.choice(self.alfabeto)
        return cromosoma
    
    def ejecutar(self):
        poblacion = self.generar_poblacion()
        
        for gen in range(self.generaciones):
            aptitudes = np.array([self.aptitud(ind) for ind in poblacion])
            
            self.historial['media'].append(aptitudes.mean())
            self.historial['mejor'].append(aptitudes.max())
            self.historial['peor'].append(aptitudes.min())
            
            if gen % 20 == 0:
                print(f"Gen {gen}: Media={aptitudes.mean():.1f}, Mejor={aptitudes.max()}")
            
            nueva_pob = []
            
            # Elitismo
            mejores_idx = np.argsort(aptitudes)[-self.elites:]
            for idx in mejores_idx:
                nueva_pob.append(poblacion[idx].copy())
            
            # Resto
            while len(nueva_pob) < self.tam_pob:
                p1 = self.seleccion_ruleta(poblacion, aptitudes)
                p2 = self.seleccion_ruleta(poblacion, aptitudes)
                h1, h2 = self.crossover(p1, p2)
                h1 = self.mutacion(h1)
                h2 = self.mutacion(h2)
                nueva_pob.extend([h1, h2])
            
            poblacion = np.array(nueva_pob[:self.tam_pob])
        
        aptitudes = np.array([self.aptitud(ind) for ind in poblacion])
        mejor_idx = np.argmax(aptitudes)
        print(f"\nMejor: {aptitudes[mejor_idx]} treses de 20")
        return poblacion[mejor_idx], aptitudes[mejor_idx]
    
    def graficar(self):
        plt.figure(figsize=(10, 5))
        plt.plot(self.historial['media'], label='Media', linewidth=2)
        plt.plot(self.historial['mejor'], label='Mejor', linewidth=2)
        plt.plot(self.historial['peor'], label='Peor', alpha=0.5)
        plt.xlabel('Generación')
        plt.ylabel('Cantidad de 3s')
        plt.title('EJERCICIO 1: Maximizar 3s')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()


# USO
print("EJERCICIO 1: Maximizar 3s")
print("Alfabeto: 0-9, Longitud: 20")
print("Óptimo: [3,3,3,3,...,3,3] = 20 treses")

ag = AG_Maximizar3s()
mejor, aptitud = ag.ejecutar()
print(f"Resultado: {mejor}")
ag.graficar()
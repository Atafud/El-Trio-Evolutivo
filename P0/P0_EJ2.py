import numpy as np
import matplotlib.pyplot as plt
import random

class AG_Subcadenas25:
    def __init__(self, tam_pob=200, long_crom=15, generaciones=1000, pc=0.3, pm=0.1, elites=3):
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
        contador = 0
        for i in range(len(cromosoma) - 1):
            if cromosoma[i] == 2 and cromosoma[i + 1] == 5:
                contador += 1
        return contador
    
    def seleccion_ruleta(self, poblacion, aptitudes):
        # Si todas las aptitudes son 0, selección aleatoria
        if aptitudes.sum() == 0:
            idx = np.random.randint(0, len(poblacion))
            return poblacion[idx].copy()
        
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
                print(f"Gen {gen}: Media={aptitudes.mean():.2f}, Mejor={aptitudes.max()}")
            
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
        print(f"\nMejor: {aptitudes[mejor_idx]} subcadenas '25' de 7 posibles")
        return poblacion[mejor_idx], aptitudes[mejor_idx]
    
    def graficar(self):
        plt.figure(figsize=(10, 5))
        plt.plot(self.historial['media'], label='Media', linewidth=2)
        plt.plot(self.historial['mejor'], label='Mejor', linewidth=2)
        plt.plot(self.historial['peor'], label='Peor', alpha=0.5)
        plt.axhline(y=7, color='red', linestyle='--', label='Óptimo (7)', linewidth=2)
        plt.xlabel('Generación')
        plt.ylabel('Subcadenas "25"')
        plt.title('EJERCICIO 2: Maximizar subcadenas "25"')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()


# USO
print("EJERCICIO 2: Maximizar subcadenas '25'")
print("Alfabeto: 0-9, Longitud: 15")
print("Óptimo: [2,5,2,5,2,5,2,5,2,5,2,5,2,5,2] = 7 subcadenas")

ag = AG_Subcadenas25()
mejor, aptitud = ag.ejecutar()
print(f"\nResultado: {mejor}")

# Mostrar las subcadenas encontradas
print("\nSubcadenas '25' encontradas:")
for i in range(len(mejor) - 1):
    if mejor[i] == 2 and mejor[i + 1] == 5:
        print(f"  Posición {i}-{i+1}: [{mejor[i]}, {mejor[i+1]}]")

ag.graficar()
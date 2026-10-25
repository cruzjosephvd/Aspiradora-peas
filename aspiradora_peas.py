import matplotlib.pyplot as plt
import numpy as np
import random
import time

class VisualEnvironment2x2:
    def __init__(self):
        # Cuadrícula 3x3: 0 = Limpio, 1 = Sucio
        self.grid = np.random.choice([0, 1], size=(3, 3))
        # Posición inicial aleatoria (fila, columna)
        self.agent_pos = [random.randint(0, 2), random.randint(0, 2)]

        # Configuración del gráfico interactivo
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(5, 5))

    def render(self, step, action, score=0):
        self.ax.clear()
        # Dibujar la cuadrícula (colores cambian según limpieza)
        self.ax.matshow(self.grid, cmap='Blues', vmin=0, vmax=1.5)

        # Dibujar al agente como un punto rojo grande
        self.ax.plot(self.agent_pos[1], self.agent_pos[0], 'ro', markersize=40)

        # Etiquetas de estado
        for i in range(3):
            for j in range(3):
                estado = "SUCIO" if self.grid[i, j] == 1 else "LIMPIO"
                self.ax.text(j, i, estado, ha='center', va='center',
                             color='black', weight='bold', fontsize=12)

        self.ax.set_title(f"Paso: {step} | Acción: {action} | PEAS: {score} pts", pad=20)
        self.ax.set_xticks([0, 1, 2])
        self.ax.set_yticks([0, 1, 2])
        self.ax.grid(which='minor', color='black', linestyle='-', linewidth=2)

        plt.draw()
        plt.pause(1.2)  # Pausa para visualizar la animación

    def get_percept(self):
        return self.agent_pos.copy(), self.grid[self.agent_pos[0], self.agent_pos[1]]

    def execute_action(self, action):
        if action == 'Suck':
            self.grid[self.agent_pos[0], self.agent_pos[1]] = 0
        elif action == 'Up' and self.agent_pos[0] > 0:
            self.agent_pos[0] -= 1
        elif action == 'Down' and self.agent_pos[0] < 2:
            self.agent_pos[0] += 1
        elif action == 'Left' and self.agent_pos[1] > 0:
            self.agent_pos[1] -= 1
        elif action == 'Right' and self.agent_pos[1] < 2:
            self.agent_pos[1] += 1

    def is_completely_clean(self):
        return np.sum(self.grid) == 0

class RandomVacuumAgent:
    def __init__(self):
        # Creamos un mapa mental de 3x3 lleno de ceros (0 = No visto, 1 = Visto)
        self.mapa_mental = np.zeros((3, 3))

    def act(self, percept):
        pos, status = percept

        # Registramos que ya vimos la casilla actual
        self.mapa_mental[pos[0], pos[1]] = 1

        # Regla principal: Si está sucio, limpia.
        if status == 1:
            return 'Suck'

        # Movimientos válidos según límites del tablero 3x3
        movimientos_posibles = []
        if pos[0] > 0: movimientos_posibles.append('Up')
        if pos[0] < 2: movimientos_posibles.append('Down')
        if pos[1] > 0: movimientos_posibles.append('Left')
        if pos[1] < 2: movimientos_posibles.append('Right')

        mov_decision = []

        # Analizar hacia dónde moverse priorizando casillas no vistas (con valor 0)
        for mov in movimientos_posibles:
            if mov == 'Up':
                if self.mapa_mental[pos[0] - 1, pos[1]] == 0:
                    mov_decision.append('Up')
            elif mov == 'Down':
                if self.mapa_mental[pos[0] + 1, pos[1]] == 0:
                    mov_decision.append('Down')
            elif mov == 'Left':
                if self.mapa_mental[pos[0], pos[1] - 1] == 0:
                    mov_decision.append('Left')
            elif mov == 'Right':
                if self.mapa_mental[pos[0], pos[1] + 1] == 0:
                    mov_decision.append('Right')

        # Si hay casillas sin explorar a los lados, toma una. Si no, camina por donde ya conoce.
        if len(mov_decision) > 0:
            return random.choice(mov_decision)
        else:
            return random.choice(movimientos_posibles)


if __name__ == "__main__":
    env = VisualEnvironment2x2()
    agent = RandomVacuumAgent()

    # Métrica inicial PEAS
    puntuacion_peas = 0
    env.render(step=0, action="Inicio", score=puntuacion_peas)

    for paso in range(1, 26):
        # Tomamos percepción previa para evaluar PEAS con precisión
        pos, esta_sucio = env.get_percept()

        action = agent.act((pos, esta_sucio))

        if action == 'Suck':
            if esta_sucio == 1:
                puntuacion_peas += 10
            else:
                puntuacion_peas -= 2
        elif action in ['Up', 'Down', 'Left', 'Right']:
            puntuacion_peas -= 1

        # Ejecutar acción en el entorno
        env.execute_action(action)

        # Renderizar la interfaz con los datos actualizados
        env.render(step=paso, action=action, score=puntuacion_peas)

        # Si todo está completamente limpio y la última acción no fue aspirar, se detiene inmediatamente
        if env.is_completely_clean() and action != 'Suck':
            print(f"¡Entorno completamente limpio!")
            print(f"Rendimiento PEAS final del agente: {puntuacion_peas} puntos.")
            break

    plt.ioff()
    plt.show()
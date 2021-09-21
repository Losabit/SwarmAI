import numpy as np
import time
from DrawerHelper import *


class Functions2D:
    @staticmethod
    def borned_linear(x):
        if x[0] >= 20:
            return 15
        else:
            return x[0]

    @staticmethod
    def draw_function(function):
        dHelper = DrawerHelper("Draw Function", 500, 500)
        while True:
            for x in range(-100, 200):
                y = function([x])
                dHelper.draw_point(dHelper.BLUE, (x + 150, -y + 100))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()


def particle_swarm_optimization(X, V, f, it_max=100, omega=1.0,
                                acceleration_coeff1=1.0, acceleration_coeff2=1.0):
    P = np.copy(X)
    Pg = np.copy(P[np.argmax([f(x) for x in P])])
    it = 0
    while it < it_max:
        for i in range(len(X)):
            r1 = np.random.random_sample()
            r2 = np.random.random_sample()
            V[i] = omega * V[i] + acceleration_coeff1 * r1 * (P[i] - X[i]) + acceleration_coeff2 * r2 * (Pg - X[i])
            X[i] = V[i] * X[i]
            if f(X[i]) > f(P[i]):
                P[i] = np.copy(X[i])
                if f(X[i]) > f(Pg):
                    Pg = np.copy(X[i])
        it += 1
    return Pg


function_to_execute = Functions2D.borned_linear
# Functions2D.draw_function(function_to_execute)

number_of_particules = 3
number_of_dimensions = 1

# Init X en fonction des dimensions et taille + random ou equidistants + borné / non borné
# Créer des fonctions de test / afficher des fonctions 3D
# Changer le critere d'arret
X = np.array([[2], [3], [1]])
v_min = -1
v_max = 1
V = (v_max - v_min) * np.random.random_sample((number_of_particules, number_of_dimensions)) + v_min  #[v_min, v_max]

start = time.time()
best_position = particle_swarm_optimization(X, V, function_to_execute, it_max=100)
end = time.time()
elapsed = end - start
print(f'Temps d\'exécution : {elapsed:.5}ms')
# https://www.ukonline.be/cours/python/opti/chapitre3-1#:~:text=Une%20autre%20possibilit%C3%A9%20pour%20mesurer,fonction%20time%20du%20module%20time%20.

print(best_position)
print(function_to_execute(best_position))


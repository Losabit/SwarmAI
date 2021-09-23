import numpy as np
import time
from DrawerHelper import *
from FunctionsSample import *


class PSO:
    def __init__(self, X, V, f):
        self.X = X
        self.V = V
        self.f = f
        self.P = np.copy(self.X)
        self.Pg = np.copy(self.P[np.argmax([self.f(x) for x in self.P])])

    def execute(self, it_max=100, omega=1.0, acceleration_coeff1=1.0, acceleration_coeff2=1.0):
        it = 0
        while it < it_max:
            self.update_all_particule(omega, acceleration_coeff1, acceleration_coeff2)
            it += 1
        return self.Pg

    def update_all_particule(self, omega=1.0, acceleration_coeff1=1.0, acceleration_coeff2=1.0):
        for i in range(len(self.X)):
            r1 = np.random.random_sample()
            r2 = np.random.random_sample()
            self.V[i] = omega * self.V[i] + acceleration_coeff1 * r1 * (self.P[i] - self.X[i]) \
                        + acceleration_coeff2 * r2 * (self.Pg - self.X[i])
            self.X[i] = self.V[i] + self.X[i]
            if self.f(self.X[i]) > self.f(self.P[i]):
                self.P[i] = np.copy(self.X[i])
                if self.f(self.X[i]) > self.f(self.Pg):
                    self.Pg = np.copy(self.X[i])


# random ou equidistants + borné / non borné
# Changer le critere d'arret

function_to_execute = Functions2D.up_and_down
# Functions2D.draw_function(function_to_execute)

function_to_execute_2 = Functions3D.center
Functions3D.draw_function(function_to_execute_2)

number_of_particules = 20
number_of_dimensions = 1

x_min = -100
x_max = 100
X = (x_max - x_min) * np.random.random_sample((number_of_particules, number_of_dimensions)) + x_min
v_min = -1
v_max = 1
V = (v_max - v_min) * np.random.random_sample((number_of_particules, number_of_dimensions)) + v_min  #[v_min, v_max]
model = PSO(X, V, function_to_execute)

dHelper = DrawerHelper("Draw Function", 500, 500)
x_func, y_func = Functions2D.get_function_points(function_to_execute)
xLag = 150
yLag = 100
while True:
    time.sleep(0.25)
    dHelper.draw_background(dHelper.WHITE)
    for particule in model.X:
        dHelper.draw_point(dHelper.GREEN, (particule[0] + xLag, -function_to_execute(particule) + yLag), width=10)
    for i in range(len(x_func)):
        dHelper.draw_point(dHelper.BLUE, (x_func[i] + xLag, -y_func[i] + yLag))

    pygame.display.update()
    model.update_all_particule()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

'''
start = time.time()
best_position = model.execute(X, V, function_to_execute)
end = time.time()
elapsed = end - start
print(f'Temps d\'exécution : {elapsed:.5}ms')
# https://www.ukonline.be/cours/python/opti/chapitre3-1#:~:text=Une%20autre%20possibilit%C3%A9%20pour%20mesurer,fonction%20time%20du%20module%20time%20.

print(best_position)
print(function_to_execute(best_position))
'''

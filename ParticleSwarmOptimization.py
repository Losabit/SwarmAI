import numpy as np


def borned_linear(x):
    if x[0] >= 20 or x[1] >= 30:
        return 20
    else:
        return x[0] + x[1]


omega = 1.0
acceleration_coeff1 = 1.0
acceleration_coeff2 = 1.0
function_to_execute = borned_linear
number_of_particules = 2
number_of_dimensions = 2


def particle_swarm_optimization(X, f, it_max=100):
    P = np.copy(X)
    Pg = P[np.argmax([f(x) for x in P])]
    it = 0
    while it < it_max:
        for i in range(len(X)):
            r1 = np.random.random_sample()
            r2 = np.random.random_sample()
            V[i] = omega * V[i] + acceleration_coeff1 * r1 * (P[i] - X[i]) + acceleration_coeff2 * r2 * (Pg - X[i])
            X[i] = V[i] * X[i]
            if f(X[i]) > f(P[i]):
                P[i] = X[i]
                if f(X[i]) > f(Pg):
                    Pg = X[i]
        it += 1
    return Pg


# Init X en fonction des dimensions et taille + random ou equidistants + borné / non borné
# Changer a fonction de test
# Changer le critere d'arret
X = np.array([[1, 2], [2, 3]])
v_min = -1
v_max = 1
V = (v_max - v_min) * np.random.random_sample((number_of_particules, number_of_dimensions)) + v_min  #[v_min, v_max]

# [          0 -2147483648] Résultat obtenu comment ?
# -2147483648
best_position = particle_swarm_optimization(X, function_to_execute)
print(best_position)
print(function_to_execute(best_position))


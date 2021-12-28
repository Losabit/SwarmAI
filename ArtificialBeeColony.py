import imageio
import  random
Workers = 30
Scouts = 5
All_bees = Workers + Scouts
iter = 50
pos_list = []
fitness_list = []
limit_list = []
opt_fitness = []

for i in range (All_bees) :
    pos_x = random.random()
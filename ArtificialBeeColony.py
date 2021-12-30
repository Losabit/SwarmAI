import imageio
import random
import matplotlib.pyplot as plt

Workers = 50
Scouts = 10
All_bees = Workers + Scouts
limit = 10
iter = 30
pos_list = []
fitness_list = []
limit_list = []
opt_fitness = []
filenames = []
nbf = 0


def max_value_index(l):
    max = l[0]
    index = 0
    for i in range(len(l)):
        if l[i] > max:
            max = l[i]
            index = i
    return index


for i in range(All_bees):
    pos_x = 500 * (random.random() - 0.5)
    pos_y = 500 * (random.random() - 0.5)
    pos_list.append({"x": pos_x, "y": pos_y})
    fitness = pos_y - pos_x ** 2
    fitness_list.append(fitness)
    limit_list.append(0)

index_sol = max_value_index(fitness_list)
best_pos = pos_list[index_sol]
best_fitness = fitness_list[i]
print(best_fitness)

for it in range(iter):
    for i in range(Workers):
        nindex = random.randint(0, All_bees - 1)
        while nindex == i:
            nindex = random.randint(0, All_bees - 1)
        tmp_x = pos_list[i]["x"] + 2 * (random.random() - 0.5) * (pos_list[nindex]["x"] - pos_list[i]["x"])
        tmp_y = pos_list[i]["y"] + 2 * (random.random() - 0.5) * (pos_list[nindex]["y"] - pos_list[i]["y"])
        if tmp_x > 250:
            tmp_x = 250
        if tmp_x < -250:
            tmp_x = -250
        if tmp_y > 250:
            tmp_y = 250
        if tmp_y < -250:
            tmp_y = -250
        tmp_fit = tmp_y - tmp_x ** 2

        if tmp_fit > fitness_list[i]:
            fitness_list[i] = tmp_fit
            pos_list[i] = {"x": tmp_x, "y": tmp_y}
            limit_list[i] = 0
        else:

            limit_list[i] = limit_list[i] + 1
        if limit_list[i] > limit:
            # New pos
            tmp_pos_x = 500 * (random.random() - 0.5)
            tmp_pos_y = 500 * (random.random() - 0.5)
            pos_list[i] = {"x": tmp_x, "y": tmp_y}
        # Print ici

        for i in range(Workers, All_bees):
            pos_x = 500 * (random.random() - 0.5)
            pos_y = 500 * (random.random() - 0.5)
            pos_list[i] = {"x": pos_x, "y": pos_y}

            fitness_list[i] = pos_y - pos_x ** 2
            plt.xlim(-260, 260)
            plt.ylim(-260, 260)


        index = max_value_index(fitness_list)
        if fitness_list[index] > best_fitness:
            best_pos = pos_list[index]
            best_fitness = fitness_list[index]
            print("cc")

        opt_fitness.append(best_fitness)
    workers_x = []
    workers_y = []
    scoot_x = []
    scoot_y = []
    for j in range(0, Workers):
        workers_x.append(pos_list[j]["x"])
        workers_y.append(pos_list[j]["y"])
    for k in range(Workers, All_bees):
        scoot_x.append(pos_list[k]["x"])
        scoot_y.append(pos_list[k]["y"])

    plt.scatter(workers_x, workers_y,c="red")
    plt.scatter(scoot_x, scoot_y,c="aqua")
    plt.show()
    plt.savefig('resources/abc/plot/' + str(i) + '_' + str(nbf) + '.png')
    plt.close()
    filenames.append('resources/abc/plot/' + str(i) + '_' + str(nbf) + '.png')
    nbf += 1
print("la")
print(best_fitness)
# x = range(iter*30)
# print(x)
# print(opt_fitness)
# plt.plot(x, opt_fitness)
# plt.show()
print("ici")

with imageio.get_writer('resources/abc/gif/movie.gif', mode='I') as writer:
    for filename in filenames:
        image = imageio.imread(filename)
        writer.append_data(image)

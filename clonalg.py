import matplotlib.pyplot as plt
import numpy as np
import math


class Clonalg:
    def __init__(self, max_it, n1, n2, p, beta, limits, evaluation):
        self.max_it = max_it
        self.N = n1
        self.n1 = n1
        self.n2 = n2
        self.beta = beta
        self.p = p
        self.nc = int(beta * self.N)  # Number of clones to be generate for each antibody
        self.evaluation = evaluation
        self.limits = limits

        self.results = np.zeros((3, self.max_it))  # 3: max, min and average
        self.population = np.random.randint(limits[0], limits[1], size=(self.N, 2))

    def select(self, population, fitness):
        # if n1 is equal N, then no selection is required
        if self.N == self.n1:
            return population, fitness

        indexes = fitness.argsort()[-self.n1::][::-1]
        # select the n1 highest fitness
        return population[indexes], fitness[indexes]

    def select_clones(self, population, fitness):
        # multimodal: select the best clone for each antibody and generate new population
        for i in range(0, self.N, self.nc):
            best = np.argmax(fitness[i * self.nc: i * self.nc + self.nc])
            self.population[i] = population[best]

    def clone(self, antibodies, fitness):
        fitness_clones = np.zeros(len(antibodies) * self.nc)
        clones = []
        for i, antibody in enumerate(antibodies):
            for j in range(i * self.nc, i * self.nc + self.nc):
                clones.append(antibody)
                fitness_clones[j] = fitness[i]
            i += self.nc

        return clones, fitness_clones

    def normalize(self, d):
        dmax = np.amax(d)
        return np.apply_along_axis(lambda di: di / dmax, 0, d)

    def mutation(self, clones, fitness):
        for (i, clone) in enumerate(clones):
            alpha = np.exp(-self.p * fitness[i])
            pb = np.random.uniform(0, 1)
            if (pb > alpha):
                continue

            delta = clones[i][0] * alpha * np.random.choice([0.01, 1])
            clones[i][0] = math.fmod(clones[i][0] + delta, self.limits[1])
            delta = clones[i][1] * alpha * np.random.choice([0.01, 1])
            clones[i][1] = math.fmod(clones[i][1] + delta, self.limits[1])
        return clones

    def replace(self):
        if self.n2 == 0:
            return self.population

    def clonalg_opt(self):
        t = 1
        while t < self.max_it:
            self.fitness = np.apply_along_axis(self.evaluation, 1, self.population)

            self.results[0][t] = np.amax(self.fitness)
            self.results[1][t] = np.amin(self.fitness)
            self.results[2][t] = np.average(self.fitness)

            population_select, fitness_select = self.select(self.population, self.fitness)
            clones, fitness_clones = self.clone(population_select, fitness_select)
            fitness_clones_normalized = self.normalize(fitness_clones)
            clones_mutated = self.mutation(clones, fitness_clones_normalized)
            fitness_clones = np.apply_along_axis(self.evaluation, 1, clones_mutated)
            self.select_clones(clones_mutated, fitness_clones)
            self.replace()
            t = t + 1

    def graph(self):
        plt.plot(self.results[0], label="Best evaluation")
        plt.plot(self.results[1], label="Worst evaluation")
        plt.plot(self.results[2], label="Average")
        plt.legend(loc='best')
        plt.show()

    def result(self):
        b = self.fitness.argmax(axis=0)
        return (self.population[b], self.fitness[b] * (-1))


def eggholder(args):
    x1 = args[0]
    x2 = args[1]
    y = -(x2 + 47) * math.sin(math.sqrt(abs(x2 + x1 / 2 + 47))) - x1 * math.sin(math.sqrt(abs(x1 - (x2 + 47))))
    return y * (-1)





def main():
    np.random.seed(123)
    clonalg = Clonalg(max_it=50, n1=50, n2=0, p=5, beta=0.1, limits=(-512, 512), evaluation=eggholder)
    clonalg.clonalg_opt()
    print(clonalg.result())
    clonalg.graph()


if __name__ == '__main__':
    main()

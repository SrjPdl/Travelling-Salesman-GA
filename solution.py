from pickle import NONE
from statistics import mode
from tsp import TSP
from deap import base, creator, tools
import os
import random
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from eaElitismCallback import eaElitismCallback
import imageio.v2 as iio
from pygifsicle import optimize

RANDOM_SEED = 10
random.seed(RANDOM_SEED)

TSP_NAME = 'bayg29'
tsp = TSP(TSP_NAME)

POPULATION_SIZE = 300
MAX_GENERATIONS = 200
HOF_SIZE = 30
P_CROSSOVER = 0.9
P_MUTAION = 0.1

toolbox = base.Toolbox()

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox.register("radomGen",random.sample,range(len(tsp)),len(tsp))

toolbox.register("individualCreator", tools.initIterate, creator.Individual, toolbox.radomGen)

toolbox.register("populationCreator",tools.initRepeat,list,toolbox.individualCreator,POPULATION_SIZE)

def fitness(individual):
    return tsp.get_distance(individual),

toolbox.register("evaluate", fitness)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", tools.cxOrdered)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb= 1/len(tsp))

def save_best(gen, best, max_gen):
    '''
    Callback function that can be used for saving the best individual of each generation as gif. Note it may slow down the genetic algorithm.
    '''

    plot = tsp.plot_tsp(best)
    if not os.path.exists('sol'):
        os.makedirs('sol')
    plot.title(f"Generation #{gen}\nDistance: {round(best.fitness.values[0],3)}")
    plot.savefig(f"sol/best_{gen}.png", dpi=200)
    plot.clf()
    if gen == max_gen:
        with iio.get_writer("sol/best.gif", mode='I') as writer:
            for i in range(1,max_gen+1):
                image = iio.imread(f"sol/best_{i}.png")
                writer.append_data(image)

                if os.path.exists(f"sol/best_{i}.png"):
                    os.remove(f"sol/best_{i}.png")
        
        optimize("sol/best.gif")


def main():
    population = toolbox.populationCreator()
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)

    hof = tools.HallOfFame(HOF_SIZE)

    #use save_best callback function to save the best individual of each generation as gif

    population, logbook = eaElitismCallback(population,toolbox,cxpb=P_CROSSOVER,mutpb=P_MUTAION,ngen=MAX_GENERATIONS,stats=stats,halloffame=hof,verbose=True, callback=None)

    best = hof[0]
    print("Best individual is %s, %s" % (best, best.fitness.values))
    plot = tsp.plot_tsp(best)
    plot.show()

    minFitness, avgFitness, maxFitness = logbook.select("min", "avg", "max")

    sns.set_style("whitegrid")
    plt.plot(minFitness, label="Minimum")
    plt.plot(avgFitness, label="Average")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend(loc="upper right")
    plt.show()
    sns.set_style("white")

if __name__=="__main__":
    main()



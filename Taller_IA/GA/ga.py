import numpy

def cal_pop_fitness(equation_inputs, pop):
     # Calcular el valor de fitness de cada individuo (solución) en la población.
     # La función fitness es igual a la suma de los productos ponderados con los pesos en el individuo.
     fitness = numpy.sum(pop*equation_inputs, axis=1)
     return fitness

def select_mating_pool(pop, fitness, num_parents):

    # Seleccionar los individuos más aptos en la población como padres para producir descendencia

    parents = numpy.empty((num_parents, pop.shape[1]))

    for parent_num in range(num_parents):
        max_fitness_idx = numpy.where(fitness == numpy.max(fitness))
        max_fitness_idx = max_fitness_idx[0][0]
        parents[parent_num, :] = pop[max_fitness_idx, :]
        fitness[max_fitness_idx] = -99999999999

    return parents

def crossover(parents, offspring_size):
     offspring = numpy.empty(offspring_size)
     # Punto de cruce
     crossover_point = numpy.uint8(offspring_size[1]/2)
 
     for k in range(offspring_size[0]):
         # Indice del primer padre
         parent1_idx = k%parents.shape[0]
         # Indice del segundo padre
         parent2_idx = (k+1)%parents.shape[0]
         # Primer descendiente
         offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
         # Segundo descendiente
         offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]

     return offspring

def mutation(offspring_crossover):

    # La mutacion cambia aleatoriamente un gen en cada descendiente.

    for idx in range(offspring_crossover.shape[0]):

        # The random value to be added to the gene.
        random_value = numpy.random.uniform(-1.0, 1.0, 1)
        offspring_crossover[idx, 4] = offspring_crossover[idx, 4] + random_value

    return offspring_crossover
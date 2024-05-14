import numpy
import ga

# Inputs of the equation.
equation_inputs = [4,-2,3.5,5,-11,-4.7]
# Numero de pesos que estámos que maximicen el valor de la función.
num_weights = 6

# Definir el tamaño de la población
sol_per_pop = 8
# La población tendrá sol_per_pop individuo donde cada individuo tiene num_weights genes.
pop_size = (sol_per_pop,num_weights)

# Crear la población inicial
new_population = numpy.random.uniform(low=-4.0, high=4.0, size=pop_size)

# Imprimir población inicial
print("\n Población inicial: \n",new_population)

num_generations = 5
num_parents_mating = 4

for generation in range(num_generations):
     # Evaluación del fitness de cada individuos en la población.
     fitness = ga.cal_pop_fitness(equation_inputs, new_population)
     print("\n Valores de fitness: \n", fitness)
     # Seleccionar los individuos más aptos en la población para apareamiento (padres).
     parents = ga.select_mating_pool(new_population, fitness, num_parents_mating)
     print("\n Padres seleccionados: \n", parents)
     # Generar una nueva población usando los operadores genéticos.
     # Cruzamiento
     offspring_crossover = ga.crossover(parents, offspring_size=(pop_size[0]-parents.shape[0], num_weights))
     print("\n Descendencia por cruzamiento: \n", offspring_crossover)
     # Mutación
     offspring_mutation = ga.mutation(offspring_crossover)
     print("\n Descendencia por mutación: \n", offspring_mutation)

     print("\n Generación: ", generation)
     # Reemplazar población anterior por la nueva
     new_population[0:parents.shape[0], :] = parents
     new_population[parents.shape[0]:, :] = offspring_mutation
     print("\n Nueva población: \n", new_population)

# Evaluación del fitness de cada individuos en la población.
fitness = ga.cal_pop_fitness(equation_inputs, new_population)
print("\n Valores de fitness: \n", fitness)
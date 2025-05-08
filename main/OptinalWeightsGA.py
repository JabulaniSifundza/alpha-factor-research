# the imports
import pickle as pk
# import pandas as pd
import numpy as np
from   scipy import stats
import UtilityFunctions as ut
import ManageData  as md  #loads and saves data
import random
from deap import base
from deap import creator
from deap import tools

TD          = md.loadsavedfile('TDDataALLCap.pkl')
F1_AP       = TD['Price_Book_AP']
F2_AP       = TD['SurpriseMomentum_AP']
F3_AP       = TD['Month12ChangeF12MEarningsEstimate_AP']
Returns_AP  = TD['ForwardReturns_AP']

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)
toolbox = base.Toolbox()

# Attribute generator 
#define 'gene' to be an attribute ('gene')
#which corresponds to integers sampled uniformly
#from the range [0,1] (i.e. 0 or 1 with equal probability)
toolbox.register("gene", random.randint, 0, 1)

#define 'individual' to be an individual
#consisting of 15 'gene' elements ('genes')
toolbox.register("individual", tools.initRepeat, creator.Individual, 
    toolbox.gene, 45)

# define the population to be a list of individuals
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# the goal ('fitness') function to be maximized
def evalFunction(individual):
    global F1_AP,F2_AP,F3_AP,Returns_AP
    x1,x2,x3  = DecodeBitsTo_x1_x2_x3(individual)
    Fitness   = Function(x1,x2,x3,F1_AP,F2_AP,F3_AP,Returns_AP)
    return Fitness,

def Function(x1,x2,x3,F1_AP,F2_AP,F3_AP,Returns_AP):
        Signal_AP          = x1*F1_AP + x2*F2_AP + x3*F3_AP
        ICByPeriod_p,ICByPeriodPval_p,GrandMeanIC,GrandStdIC,ICitp1 = CalcICByPeriod(Signal_AP,Returns_AP)
        Pen     = Penalty(x1,x2,x3)
        ICitp2  = 5 + 10*ICitp1 - Pen
        # print('ICitp1 ' + str(ICitp1) + ' Penalty ' + str(Pen))
        # print('Sum weights ' + str(x1+x2+x3))
        # print('ICitp2 ' + str(ICitp2))
        return ICitp2
def Function2(x1,x2,x3,F1_AP,F2_AP,F3_AP,Returns_AP):
        Signal_AP          = x1*F1_AP + x2*F2_AP + x3*F3_AP
        ICByPeriod_p,ICByPeriodPval_p,GrandMeanIC,GrandStdIC,ICitp1 = CalcICByPeriod(Signal_AP,Returns_AP)
        Pen     = Penalty(x1,x2,x3)
        ICitp2  = 5 + 10*ICitp1 - Pen
        print('ICitp1 ' + str(ICitp1) + ' Penalty ' + str(Pen))
        print('Sum weights ' + str(x1+x2+x3))
        print('Weights ' + str(x1) + ' ' + str(x2) + ' ' + str(x3))
        return ICitp1
def Penalty(x1,x2,x3):
    Sum     = x1+x2+x3
    Value   = np.abs(1-Sum**2)
    return Value
def DecodeBitsTo_x1_x2_x3(individual):
    NumBits    = 15   
    x1_bits    = individual[0:NumBits]
    x2_bits    = individual[NumBits:NumBits*2]
    x3_bits    = individual[NumBits*2:NumBits*3]
    x1_decimal = ConvertToDecimal(x1_bits)
    x2_decimal = ConvertToDecimal(x2_bits)
    x3_decimal = ConvertToDecimal(x3_bits)
    a  = 0.0
    b  = 1.0
    x1 = a + x1_decimal*((b-a)/(2**(NumBits)-1))
    x2 = a + x2_decimal*((b-a)/(2**(NumBits)-1))
    x3 = a + x3_decimal*((b-a)/(2**(NumBits)-1))
    return x1,x2,x3
def ConvertToDecimal(Bits):
    Decimal = 0
    ctr = -1
    for b in Bits:
        ctr     = ctr+1
        Value   = b*(2**ctr)
        Decimal = Decimal + Value
    return Decimal
#----------
# Operator registration
#----------
# register the goal / fitness function
toolbox.register("evaluate", evalFunction)

# register the crossover operator
toolbox.register("mate", tools.cxTwoPoint)

# register a mutation operator with a probability to
# flip each attribute/gene of 0.05
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)

# operator for selecting individuals for breeding the next
# generation: each individual of the current generation
# is replaced by the 'fittest' (best) of three individuals
# drawn randomly from the current generation.
toolbox.register("select", tools.selTournament, tournsize=3)

#----------
def ProcessGA():
    NumberInPopulation      = 100
    MaxGenerations          = 10
    CrossoverProbability    = .5
    MutationrProbability    = .2
    Trace                   = 1
    R       = GeneticAlgo(NumberInPopulation,MaxGenerations,CrossoverProbability,MutationrProbability,Trace)
    return R

def GeneticAlgo(NumberInPopulation,MaxGenerations,CrossoverProbability,MutationrProbability,Trace):   
    global F1_AP,F2_AP,F3_AP,Returns_AP
    # CrossoverProbability  is probability two individuals are crossed
    # MutationrProbability is the probability for mutating an individualrandom.seed(64)
    
    # create an initial population of n individuals (where
    # each individual is a list of integers)
    pop = toolbox.population(n=NumberInPopulation)
    if Trace == 1:
        print("Start of evolution")
    
    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    if Trace == 1:
        print("  Evaluated %i individuals" % len(pop))

    # Extracting all the fitnesses of 
    fits = [ind.fitness.values[0] for ind in pop]

    # Variable keeping track of the number of generations
    g = 0
    # Begin the evolution
    while g < MaxGenerations:
        # A new generation
        g = g + 1
        if g%500 ==0:
            print("         -- Generation %i --" % g)
        if Trace == 1:
            print("   Generation %i" % g)
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))
        if CrossoverProbability > 0: # Apply crossover to the offspring
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                # cross two individuals with probability CrossoverProbability
                if random.random() < CrossoverProbability:
                    toolbox.mate(child1, child2)
                    # fitness of children recalculated later
                    del child1.fitness.values
                    del child2.fitness.values
        if MutationrProbability > 0: # Apply mutation to the offspring
            for mutant in offspring:
                # mutate an individual with probability MutationrProbability
                if random.random() < MutationrProbability:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values
    
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        if Trace == 1:
            print("  Evaluated %i individuals" % len(invalid_ind))
        
        # The population is entirely replaced by the offspring
        pop[:] = offspring
        
        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]
        if Trace == 1:
            print("  Max %s" % max(fits))

    if Trace == 1:
        print("-- End of (successful) evolution --")
    
    best_ind            = tools.selBest(pop, 1)[0]
    # best_ind_fitness    = best_ind.fitness.values
    [x1,x2,x3]          = DecodeBitsTo_x1_x2_x3(best_ind)
    Fitness             = Function2(x1,x2,x3,F1_AP,F2_AP,F3_AP,Returns_AP)

    R               = {}
    R['Weights']    = [x1,x2,x3]
    R['Fitness']    = Fitness
    return R


def SaveD(D,Filename):
    #start_time      = time.time()
    f = open(Filename,"wb")
    pk.dump(D,f)
    f.close()
    #elapsed_time = time.time() - start_time
    #print('Elapsed time = ' + str(elapsed_time))
    print('D saved as ' + Filename)
    return 1

def LoadD(Filename):
    #start_time  = time.time()
    f           = open(Filename,"rb")
    D           = pk.load(f) 
    f.close()
    #elapsed_time = time.time() - start_time
    #print('Elapsed time = ' + str(elapsed_time))
    print('D loaded from ' + Filename)
    return D
def CalcICByPeriod(Signal_AP,Returns_AP):
    MinNumForCorrelation    =   5
    NumPeriod               =   Returns_AP.shape[1]
    ICByPeriod_p            =   np.nan*np.zeros(NumPeriod)
    ICByPeriodPval_p        =   np.nan*np.zeros(NumPeriod)  
    #CumExcessRetBySignalTile        =   nan(NumTiles,NumPeriods);
    for p in range(0,NumPeriod):
        if p+1 <= NumPeriod-1:
            s       =   Signal_AP[:,p]
            f       =   Returns_AP[:,p+1]
            s,f,goodlist = ut.pairwise(s,f)
            if not ut.isempty(goodlist) and len(goodlist) >= MinNumForCorrelation:
                rho, pval           = stats.spearmanr(s,f)
                ICByPeriod_p[p]     = rho
                ICByPeriodPval_p[p] = pval
    GrandMeanIC =   np.nanmean(ICByPeriod_p)
    GrandStdIC  =   np.nanstd(ICByPeriod_p)
    ICitp       =   GrandMeanIC/GrandStdIC
    return ICByPeriod_p,ICByPeriodPval_p,GrandMeanIC,GrandStdIC,ICitp

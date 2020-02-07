import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time

# from process_allocation import process_allocation
from step_calculation import step_calc
from measures import statistics_measures
from measures import make_plot

from pymoo.performance_indicator.hv import Hypervolume
from pymoo.algorithms.nsga2 import NSGA2
from pymoo.factory import get_problem
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter
from pymoo.factory import get_algorithm, get_crossover, get_mutation, get_sampling

import autograd.numpy as anp
import numpy as np
from pymoo.util.misc import stack
from pymoo.model.problem import Problem

class MyProblem(Problem):
    def __init__(self):
        super().__init__(n_var=2,
                         n_obj=2,
                         n_constr=0,
                         xl=anp.array([1,1]),
                         xu=anp.array([500,5]))

    def _evaluate(self, x, out, *args, **kwargs):
        new_acts = []
        new_costs = []
        for i in x:
            pools = {}
            
            for j in range(len(i)):
                pools["Role " + str(j+1)] = i[j]

            res = step_calc(pools)
            new_act = float(res[0])
            new_acts.append(new_act)
            new_cost = float(res[2])
            new_costs.append(new_cost)

        out["F"] = anp.column_stack([new_acts, new_costs])

glob = {'suboptimals': [], 'max_act': 0, 'max_cost': 0, 'measures': []}
start = time.time()

for it in range(5):
    glob = {
                'times': [],
                'costs': [],
                'dominants': [],
                'best_dominants': [],
                'max_cost': 0,
                'max_act': 0,
                'suboptimals': [],
                'best_cost': 999999999,
                'best_act': 999999999,
                'best_alloc': '',
                'visited_pools': {},
                'pools_map': {},
                'stable': [],
                'moving': [],
                'neighbourhood': [],
                'measures': glob['measures']
            }

    problem = MyProblem()
    algorithm = get_algorithm("nsga2",
                        pop_size=10,
                        sampling=get_sampling("int_random"),
                        crossover=get_crossover("int_sbx"),
                        mutation=get_mutation("int_pm", eta=3.0),
                        eliminate_duplicates=True
                        )

    res = minimize(problem,
                algorithm,
                ('n_gen', 50),
                seed=1,
                pf=problem.pareto_front(use_cache=False),
                save_history=True,
                verbose=True)

    pop_each_gen = [a.pop for a in res.history]
    iter = 0
    for p in pop_each_gen:
        glob['suboptimals'] = []
        glob['max_act'] = 0
        glob['max_cost'] = 0
        for p1 in p:
            if(glob['max_act'] < p1.F[0]):
                glob['max_act'] = p1.F[0]
            if(glob['max_cost'] < p1.F[1]):
                glob['max_cost'] = p1.F[1]

            glob['suboptimals'].append({'act': p1.F[0], 'cost': p1.F[1]})
        statistics_measures(iter, "stats_nsga2.txt", glob, True, 0)
        iter += 1

    f1 = open("stats_nsga2.txt", "a")
    f1.write(str(glob['suboptimals']) + " \n")
    f1.close()

end = time.time()
make_plot(glob)

f2 = open("stats_nsga2.txt", "a")
f2.write("--------------------------------------------------- \n")
f2.write("Total time elapsed for 5 experiments (sec) = " + str(end - start) + " \n")
f2.write("--------------------------------------------------- \n")
f2.close()
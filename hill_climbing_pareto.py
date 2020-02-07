import sys
import subprocess
import configparser as cp
import csv
import time

import itertools
import copy
from shutil import copyfile

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from process_allocation import process_allocation
from step_calculation import step_calc
from pareto_pruner import prunePareto
from measures import statistics_measures
from measures import make_plot

def hill_pareto(max_iters, statistics_step, tabu=False, trace_file_name="trace.txt", stats_file_name="test_stats.txt"):
    f = open(trace_file_name, "a")
    start = time.time()

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
        'measures': []
    }

    for it in range(5):
        model_name = "./ConsultaDataMining201618.bpmn"
        copyfile(model_name, "./CopiedModel.bpmn")
        res = step_calc()
        act = res[0]
        pools = res[1]
        cost = res[2]
        utils = res[3]
        joined = '_'.join(str(v) for v in pools.values())
        
        tabu_list = []
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

        glob['moving'] = [{'id': joined, 'act': act, 'cost': cost, 'utils': utils}]
        glob['pools_map'][joined] = pools
        glob['visited_pools'][joined] = True

        glob['best_cost'] = res[2]
        glob['best_act'] = int(res[0])
        glob['best_alloc'] = joined

        glob['suboptimals'].append({'id': joined, 'cost': glob['best_cost'], 'act': glob['best_act'], 'utils': utils})
        f.write(joined + " = " + str(glob['best_act']) + " iter = 0 sub = " + str(glob['suboptimals']) + "\n")

        print("values = ", joined)

        iterations = 0
        while len(glob['moving']) > 0 and iterations < max_iters:
            iterations += 1
            suboptimals_changed = False
            # last_step_no_improve = False
            glob['neighbourhood'] = []

            for current in glob['moving']:
                utils = current['utils']
                print(glob['pools_map'][current['id']])

                # iterating all possible neighbours and selecting the best allocation
                for pair in itertools.product(glob['pools_map'][current['id']], repeat=2):
                    if(pair[0] != pair[1]):
                        cop = copy.deepcopy(glob['pools_map'][current['id']])
                        # moving
                        if(cop[pair[0]] > 1 and utils[pair[0]] < utils[pair[1]] and utils[pair[0]] < 90):
                            cop2 = copy.deepcopy(glob['pools_map'][current['id']])
                            cop2[pair[0]] -= 1
                            cop2[pair[1]] += 1
                            suboptimals_changed = process_allocation(glob, cop2, f, iterations, tabu_list, tabu) or suboptimals_changed

                        # removing
                        if(cop[pair[0]] > 15 and utils[pair[0]] < 90):
                            cop2 = copy.deepcopy(glob['pools_map'][current['id']])
                            cop2[pair[0]] -= 15
                            suboptimals_changed = process_allocation(glob, cop2, f, iterations, tabu_list, tabu) or suboptimals_changed

                        # removing
                        if(cop[pair[0]] > 1 and utils[pair[0]] < 90):
                            cop2 = copy.deepcopy(glob['pools_map'][current['id']])
                            cop2[pair[0]] -= 1
                            suboptimals_changed = process_allocation(glob, cop2, f, iterations, tabu_list, tabu) or suboptimals_changed

                        # adding
                        if(utils[pair[0]] > 50 or tabu):
                            cop2 = copy.deepcopy(glob['pools_map'][current['id']])
                            cop2[pair[0]] += 1
                            suboptimals_changed = process_allocation(glob, cop2, f, iterations, tabu_list, tabu) or suboptimals_changed
            
            # we keep only the solutions from the neighbourhood
            # that became suboptimal
            glob['moving'] = list(filter(lambda x: x in glob['suboptimals'], glob['neighbourhood']))

            # write statistics for current iteration
            if(iterations % statistics_step == 0 or len(glob['moving']) == 0):
                statistics_measures(iterations, stats_file_name, glob, suboptimals_changed, len(glob['neighbourhood']))

            # in tabu case we can add non-optimal points to keep expanding
            if(len(glob['moving']) < 5 and tabu):
                for q in range(int(len(glob['neighbourhood']))):
                    if(glob['neighbourhood'][q]['id'] not in tabu_list and len(glob['moving']) < 5):
                        glob['moving'].append(glob['neighbourhood'][q])
                        tabu_list.append(glob['neighbourhood'][q]['id'])

            # also for tabu case
            for q in range(int(len(glob['moving']))):
                if(glob['moving'][q]['id'] not in tabu_list):
                    tabu_list.append(glob['moving'][q]['id'])

            while(len(tabu_list) > 10):#150 for purchasing example, 20 for consulta
                # 500 - 250 - 200 - 175 - 160 - 150 - 140 - 130 - 120 - 100 - 50 - 25 - 10
                # or tabu 200 (212) - 140
                tabu_list.pop(0)
            # print('moving =', len(glob['moving']))
        f2 = open(stats_file_name, "a")
        f2.write(str(glob['suboptimals']) + " \n")
        f2.close()

    f.close()
    print("suboptimals = ", glob['suboptimals'])
    end = time.time()
    make_plot(glob)

    f2 = open(stats_file_name, "a")
    f2.write("--------------------------------------------------- \n")
    f2.write("Total time elapsed for 5 experiments (sec) = " + str(end - start) + " \n")
    f2.write("--------------------------------------------------- \n")
    f2.close()

    # print("times = ", times)
    # print("costs = ", costs)
    # plt.plot(times, costs, 'ro')

    return glob
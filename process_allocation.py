from step_calculation import step_calc
from pareto_pruner import prunePareto

def process_allocation(glob, pools, f, counter, tabu_list, tabu):
    joined2 = '_'.join(str(v) for v in pools.values())
    changed = False

    # we dont process the allocation that already visited
    if((glob['visited_pools'].get(joined2) == None and not tabu) or (tabu and joined2 not in tabu_list)):
        glob['visited_pools'][joined2] = True
        res = step_calc(pools)
        glob['pools_map'][joined2] = res[1]
        new_act = int(res[0])
        new_cost = res[2]
        new_utils = res[3]

        glob['times'].append(new_act)
        glob['costs'].append(new_cost)

        if(new_act > glob['max_act']):
            glob['max_act'] = new_act

        if(new_cost > glob['max_cost']):
            glob['max_cost'] = new_cost

        # for tabu we add everything, for hill climbing only the best
        if(tabu):
            glob['neighbourhood'].append({'id': joined2, 'cost': new_cost, 'act': new_act, 'utils': new_utils})
        else:
            pareto_res = prunePareto(glob['neighbourhood'], new_act, new_cost, joined2, new_utils)
            glob['neighbourhood'] = pareto_res[0]

        pareto_res = prunePareto(glob['suboptimals'], new_act, new_cost, joined2, new_utils)
        if(pareto_res[1]):
            changed = True
            glob['suboptimals'] = pareto_res[0]

            if(new_act < glob['best_act']):
                glob['best_act'] = new_act

            if(new_cost < glob['best_cost']):
                glob['best_cost'] = new_cost

            f.write(joined2 + " iter = " + str(counter) + " sub = " + str(glob['suboptimals']) + "\n")

    return changed
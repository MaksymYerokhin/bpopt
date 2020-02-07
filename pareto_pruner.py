def prunePareto(lst, act, cost, joined, utils):
    new_lst = list(
        filter(lambda obj: obj['cost'] < cost or obj['act'] < act, lst))
    changed = len(new_lst) < len(lst)
    # new point dominated some of the existing, so we insert it right away
    if(changed):
        new_lst.append({'id': joined, 'cost': cost, 'act': act, 'utils': utils})
    else:
        # if anybody is dominating new point, we skip it
        dominating = list(filter(lambda obj: obj['cost'] <= cost and obj['act'] <= act, lst))
        if(len(dominating) == 0):
            new_lst.append({'id': joined, 'cost': cost, 'act': act, 'utils': utils})
            changed = True

    return (new_lst, changed)
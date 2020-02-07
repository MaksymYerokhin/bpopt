import copy
import matplotlib.pyplot as plt

def statistics_measures(iterations, file_name, globalis, suboptimals_changed, len_neighbouthood):
    # violin plot (multiple experiments)
    # for different iteration, eg when it stps adding more points
    # interval plot
    # all measures on separate graphs

    # min max

    cop1 = copy.deepcopy(globalis['suboptimals'])
    cop2 = copy.deepcopy(globalis['suboptimals'])
    cop3 = copy.deepcopy(globalis['suboptimals'])
    cop4 = copy.deepcopy(globalis['suboptimals'])

    cop1.sort(key=lambda x: x['cost'])
    mincost = cop1[0]['cost']

    cop2.sort(key=lambda x: x['cost'], reverse=True)
    maxcost = cop2[0]['cost']

    cop3.sort(key=lambda x: x['act'])
    minact = cop3[0]['act']

    cop4.sort(key=lambda x: x['act'], reverse=True)
    maxact = cop4[0]['act']

    # print('mincost = ', mincost)
    # print('maxcost = ', maxcost)

    # print('minact = ', minact)
    # print('maxact = ', maxact)

    h1 = maxact - minact
    h2 = maxcost - mincost
    hh1 = globalis['max_act']
    hh2 = globalis['max_cost']

    # print('hh1 = ', hh1)
    # print('hh2 = ', hh2)

    # print('h1 = ', h1)
    # print('h2 = ', h2)

    print('Overall pareto spread = ', (h1 * h2)/(hh1 * hh2))
    print('Pareto spread over time = ', h1/hh1)
    print('Pareto spread over cost = ', h2/hh2)
    print('Points number = ', len(globalis['suboptimals']))

    area = 0
    for i in range(len(cop1) - 1):
        p1 = cop1[i]
        p2 = cop1[i + 1]
        ht = p2['cost'] - p1['cost']
        s = ((p1['act'] + p2['act']) / 2) * ht
        area += s

    print('Hyperarea difference = ', area)
    f = open(file_name, "a")
    f.write("iterations = " + str(iterations) + ", " + str(round((h1 * h2)/(hh1 * hh2), 3)) + ", " + str(round(h1/hh1, 3)) + ", " + str(round(h2/hh2, 3)) + ", " + str(len(globalis['suboptimals'])) +
                    ", " + str(area) + ", changed = " + str(suboptimals_changed) + ", neighbourhood = " + str(len_neighbouthood) + " \n")
    f.close()
    globalis['measures'].append({'iterations': iterations, 'points': len(globalis['suboptimals']), 'spread': round((h1 * h2)/(hh1 * hh2),3), 'spread_time': round(h1/hh1, 3), 'spread_cost': round(h2/hh2,3), 'area': area})

def make_plot(glob):
    plt.title("Subplot Area distribution")
    plt.xlabel("Iterations")
    plt.ylabel("Area")
    plt.autoscale()

    dtimes = [x['act'] for x in glob['suboptimals']]
    dcosts = [x['cost'] for x in glob['suboptimals']]
    areas = [x['area'] for x in glob['measures']]
    spreads = [x['spread'] for x in glob['measures']]
    spreads_time = [x['spread_time'] for x in glob['measures']]
    spreads_cost = [x['spread_cost'] for x in glob['measures']]
    iterations = [x['iterations'] for x in glob['measures']]
    points = [x['points'] for x in glob['measures']]

    plt.scatter(iterations, areas, color='red')
    fig, ax = plt.subplots()
    ax.set_xlabel("Average cycle time")
    ax.set_ylabel("Cost")
    ax.set_title("Pareto frontier")
    ax.scatter(dtimes, dcosts)
    
    # fig2, ax2 = plt.subplots()
    # ax2.set_xlabel("Iterations")
    # ax2.set_ylabel("Spread")
    # ax2.set_title("Spread distribution")
    # ax2.scatter(iterations, spreads)

    # fig3, ax3 = plt.subplots()
    # ax3.set_xlabel("Iterations")
    # ax3.set_ylabel("Number of points")
    # ax3.set_title("Number of points growth")
    # ax3.scatter(iterations, points)

    # fig4, ax4 = plt.subplots()
    # ax4.set_xlabel("Iterations")
    # ax4.set_ylabel("Time spread")
    # ax4.set_title("Time spread distribution")
    # ax4.scatter(iterations, spreads_time)

    # fig5, ax5 = plt.subplots()
    # ax5.set_xlabel("Iterations")
    # ax5.set_ylabel("Cost spread")
    # ax5.set_title("Cost spread distribution")
    # ax5.scatter(iterations, spreads_cost)

    plt.show()
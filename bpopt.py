import sys
import os

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from hill_climbing_pareto import hill_pareto

def main():
    hill_pareto(50, 2, tabu=True, trace_file_name="corrected_consulta_trace_tabu.txt", stats_file_name="corrected_consulta_stats_tabu.txt")

if __name__ == "__main__":
    main()
# Optimizing Resource Allocation in Business Processes (BPOPT)

BPOPT uses simulation process models to find the better resource allocations using three different algorithms.
We assume that you use XES logs as input for the Simod tool and get the simulation model from there.
Then you can run bpopt.py script or nsga2.py script to execute the analysis and get the benchmarks.
The output is always a set of solution in form of Pareto frontier and a set of corresponding metrics
assessing these frontiers. Due to the stochastic nature of BIMP simulator we run each experiment 5 times.

### Prerequisites

To execute this code you just need to install Python 3.7+ in your system.

### Data format
 
The application assumes the input is composed by a case identifier, an activity label, a resource attribute (indicating which resource performed the activity), and two timestamps: the start timestamp and the end timestamp. 
If you decide to start with BPMN, you have to ensure that it contains the available resource pools, their timetables, and the mapping between activities and resource pools.

### Execution steps

***Simulation model mining:*** 
Described in https://github.com/AdaptiveBProcess/Simod

***Hill Climbing and Tabu Search:***
To use these algorithms, you have to first setup bpopt.py.
Change the parameters of the following command:
`hill_pareto(50, 2, tabu=True, trace_file_name="corrected_consulta_trace_tabu.txt", stats_file_name="corrected_consulta_stats_tabu.txt")`
The first paraneters is the maximum number of iterations, second is the frequency of logging of the measures (from 1 to max. number of iterations),
then goes the name of statistics file and trace file (if you want to see more insight).
The input model is set in hill_climbing_pareto.py

***NSGA-2:***
To run NSGA-2 you have to execute nsga2.py script and have the simulation model as CopiedModel.bpmn in the same directory.
You have to edit MyProblem class and set the number of BPMN pools in `n_var`, number of outcomes in `n_obj` and resource bounds
in `xl` and `xu`.

### Results
Each script produces the statistics file and logging information in trace file.
Statistics measures include pareto spread, hyperarea difference and the number of points. 
Also the script builds a Pareto frontier with the biggest numb er of points for each experiment.

## Authors

* **Maksym Yerokhin**
* **Marlon Dumas**
* **Fabrizio Maria Maggi**

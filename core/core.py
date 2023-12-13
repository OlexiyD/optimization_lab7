import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.termination import get_termination
from pymoo.optimize import minimize
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.decomposition.asf import ASF

import matplotlib.pyplot as plt

from dataclasses import dataclass
from typing import Callable

from sympy import lambdify

# Documentation: https://pymoo.org/getting_started/part_2.html

# Inputs from GUI: 
# n_var, n_obj, n_ieq_constr, xl, xu, f1, f2, g1, g2
# NSGA2 + all params (there will be one more algo with other params)
# weights

# Output to GUI:
# X - length of n_var (simply few numbers)
# F - length of n_obj (simply few numbers)

# TODO: with lambdify string can be coverted to function. Order of variables matter!
# Ex.: f2 = lambdify(['z', 'x', 'y'], "x*2 +y*10 + z*40") # can take both strings and symbolic objects
# Note: should teke same numbers of inputs as length of first arg in lambdify (even if not all of them are used!)

# Configuration package for problem
@dataclass
class OptimizationConfiguration():
    """This class holds information about optimization configuration

    Attributes:
        termination_n_gen (int):          Number of generations for optimization termination.
        save_history (bool):              Flag which defines if history of operations has to be stored.
        verbose (bool):                   Flag which defines if verbose output has to be generated.
        weights (list[float]):            List of objectives weights (sum must be equal to 1).
    """

    termination_n_gen: int = None
    save_history: bool = False
    verbose: bool = False
    weights: list[float] = None

# Configuration package for problem
@dataclass
class ProblemConfiguration():
    """This class holds information about optimization problem

    Attributes:
        n_var (int):                      Number of independent variables.
        n_obj (int):                      Number of objective functions.
        n_ieq_constr (int):               Number of constrains.
        xl (np.array):                    Lower limits for independednt variables. Length of array is n_var
        xu (np.array):                    Upper limits for independednt variables. Length of array is n_var
        objective_fcn (list[function]):   List of objective functions
        constrains (list[function]):      List of constrains
    """

    n_var: int = 1
    n_obj: int = 1
    n_ieq_constr: int = 1
    xl: np.ndarray = None
    xu: np.ndarray = None
    objective_fcn: list[Callable] = None
    constrains: list[Callable] = None

# Configuration package for NSGA2 algorithm
@dataclass
class AlgorithmConfiguration():
    """This class holds information about solving algorithm

    Attributes:
        algo_type (str):                  Solver algorithm type. Supoorted values: NSGA2, U-NSGA-III, MOEA/D.
        n_obj (int):                      Number of objective functions. Dublicate from problem config!
        ref_dirs_type (str):              Type of reference dir's. Supported values: "energy", "uniform"
        n_partitions (int):               Number of partitions (required for "uniform" ref_dir).
        n_points (int):                   Number of ppoints (required for "energy" ref_dir).
        pop_size (int):                   Population size
        n_offsprings (int):               Number of offspring that are created through mating.
        crossover_prob (float):           Crossover operator will create a different number of offsprings dependent on the implementation.
        crossover_eta (int):              Crossover operator will create a different number of offsprings dependent on the implementation.
        mutation_en (bool):               Mutation enable
        mutation_eta (int):               Probability config for mutation
        eliminate_duplicates (bool):      Remove duplicates
    """

    algo_type: str = None
    n_obj: int = None
    ref_dirs_type: str = "uniform"
    n_partitions: int = None
    n_points: int = None
    pop_size: int = 40
    n_offsprings: int = 10
    crossover_prob: float = 0.9
    crossover_eta: int = 15
    mutation_en: bool = True
    mutation_eta: int = 20
    eliminate_duplicates: bool = True

# Creating problem calss for optimization
class Problem(ElementwiseProblem):
    """General class to solve problem

    Inherited from base class for optimization problems

    Attributes (additional):
        _obj_fcn (list[lambda fcn]):    List of objective functions
        _constrains (list[lambda fcn]): List of constrains
    """

    def __init__(self, configuration):
        super().__init__(n_var=configuration.n_var,
                         n_obj=configuration.n_obj,
                         n_ieq_constr=configuration.n_ieq_constr,
                         xl=configuration.xl,
                         xu=configuration.xu)
        
        # Objective functions and constrains for problem
        self._obj_fcn = configuration.objective_fcn
        self._constrains = configuration.constrains

    def _evaluate(self, x, out, *args, **kwargs):
        # Calculate funtion results
        out["F"] = [fun(*x) for fun in self._obj_fcn]
        out["G"] = [fun(*x) for fun in self._constrains]

def visualize(problem: Problem, X: np.ndarray, F: np.ndarray, solution_idx: int):
    """Function to perform reults visualization

    Plots design space and objective space

    Parameters:
        problem (class Problem):    Problem for optimization
        X (np.ndarray):             Variables values
        Y (np.ndarray):             Objective functions values
        solution_idx (int):         Index of solution
    """

    # Visualizing
    # TODO: multiprocessing seems not required
    # TODO: consider 1, 2, 3 objectives

    plt.figure(figsize=(7, 5))

    xl, xu = problem.bounds()
    num_vars = len(X[0])
    num_obj = len(F[0])
    match num_vars:
        case 1:
            # Plot option for single objective optimization
            plt.scatter(X, F, marker="x", color="green", s=200)
            plt.title("Single solution")
        case 2:
            # Plot option for two objective optimization
            plt.scatter(X[:, 0], X[:, 1], s=30, facecolors='none', edgecolors='r')
            plt.scatter(X[solution_idx, 0], X[solution_idx, 1], marker="x", color="green", s=200)
            plt.xlim(xl[0], xu[0])
            plt.ylim(xl[1], xu[1])
            plt.xlabel("x0")
            plt.ylabel("x1")
            plt.title("Design Space")
            plt.grid(visible=True)
        case 3:
            # TODO: unoperational
            plt.scatter(X[:, 0], X[:, 1], X[:, 1], s=30, facecolors='none', edgecolors='r')
            plt.scatter(X[solution_idx, 0], X[solution_idx, 1], X[solution_idx, 1], marker="x", color="green", s=200)
            plt.xlim(xl[0], xu[0])
            plt.ylim(xl[1], xu[1])
            plt.xlabel("x0")
            plt.ylabel("x1")
            plt.title("Design Space")
            plt.grid(visible=True)
            pass
        case default:
            #
            pass

    plt.ion()
    plt.show() 

    plt.figure(figsize=(7, 5))

    match num_obj:
        case 1:
            # How handle?
            pass
        case 2:
            # Plot option for two objective optimization
            plt.scatter(F[:, 0], F[:, 1], s=30, facecolors='none', edgecolors='blue')
            plt.scatter(F[solution_idx, 0], F[solution_idx, 1], marker="x", color="red", s=200)
            plt.xlabel("f0")
            plt.ylabel("f1")
            plt.title("Objective Space")
            plt.grid(visible=True)
        case 3:
            # TODO: unoperational
            plt.scatter(F[:, 0], F[:, 1], s=30, facecolors='none', edgecolors='blue')
            plt.scatter(F[solution_idx, 0], F[solution_idx, 1], marker="x", color="red", s=200)
            plt.xlabel("f0")
            plt.ylabel("f1")
            plt.title("Objective Space")
            plt.grid(visible=True)
            pass
        case default:
            #
            pass

    plt.ion()
    plt.show()

    # Option for single criteria

def init_algo(config: AlgorithmConfiguration):
    """Function to intialize solver algorithm

    Parameters:
        config (class AlgorithmConfiguration):      Algorithm configuration
    """
    
    match config.algo_type:
        case "NSGA2":
            # NSGA 2 algorithm
            algorithm = NSGA2(
                            pop_size=config.pop_size,
                            n_offsprings=config.n_offsprings,
                            sampling=FloatRandomSampling(),
                            crossover=SBX(prob=config.crossover_prob, eta=config.crossover_eta),
                            mutation=(PM(eta=config.mutation_eta) if config.mutation_en else None),
                            eliminate_duplicates=config.eliminate_duplicates
                        )
        case "U-NSGA-III":
            # U-NSGA-III algorithm
            ref_dirs = get_reference_directions(config.ref_dirs_type, config.n_obj, n_partitions=config.n_partitions)
            pass
        case "MOEA/D":
            # MOEA-D algorithm
            ref_dirs = get_reference_directions(config.ref_dirs_type, config.n_obj, config.n_points, seed=1)
            pass
        case _:
            # unsupported algorithm value
            raise ValueError("Incorrect algorithm option supplied!")
        
    return algorithm


# test code - this will be at GUI or at GUI communication
if __name__ == "__main__":

    # Inputs (from GUI)
    # Problem configuration
    problem_config = ProblemConfiguration()
    problem_config.n_var = 2
    problem_config.n_obj = 2
    problem_config.n_ieq_constr = 2
    problem_config.xl = np.array([-2, -2])
    problem_config.xu = np.array([2, 2])

    # TODO: here some parsing may be required
    # TODO: wrap in try catch and send error message to GUI at catch (maybe all core)
    # f1 = 100 * (x[0]**2 + x[1]**2)
    f1 = lambdify(['x0', 'x1'], "100 * (x0**2 + x1**2)")
    # f2 = (x[0]-1)**2 + x[1]**2
    f2 = lambdify(['x0', 'x1'], "(x0-1)**2 + x1**2")

    # g1 = 2*(x[0]-0.1) * (x[0]-0.9) / 0.18
    g1 = lambdify(['x0', 'x1'], "2*(x0-0.1) * (x0-0.9) / 0.18")
    # g2 = - 20*(x[0]-0.4) * (x[0]-0.6) / 4.8
    g2 = lambdify(['x0', 'x1'], "- 20*(x0-0.4) * (x0-0.6) / 4.8")

    problem_config.objective_fcn = [f1, f2]
    problem_config.constrains = [g1, g2]

    # Algorithm configuration
    # TODO: expect here branching based on algorithm
    algo_config = AlgorithmConfiguration()
    algo_config.algo_type = "NSGA2"
    algo_config.n_obj = problem_config.n_obj
    algo_config.n_partitions = 12
    algo_config.n_points = 90
    algo_config.ref_dirs_type = "uniform"
    algo_config.pop_size = 40
    # + other params (currently set to some default values)

    # Optimization configuration
    opt_config = OptimizationConfiguration()
    opt_config.termination_n_gen = 40
    opt_config.save_history = False
    opt_config.verbose = True
    opt_config.weights = np.array([0.2, 0.8])

    # Instanciating object of problem class
    problem = Problem(problem_config)

    # Creating algorithm for optimization
    algorithm = init_algo(algo_config)

    # Creating termination criteria
    termination = get_termination("n_gen", opt_config.termination_n_gen)

    # Applying optimization (produces set of solutions)
    res = minimize(problem,
                   algorithm,
                   termination,
                   seed=1,
                   save_history=opt_config.save_history,
                   verbose=opt_config.verbose)

    # Storing solutions to variables
    X = res.X
    F = res.F

    # Normalization
    approx_ideal = F.min(axis=0)
    approx_nadir = F.max(axis=0)
    nF = (F - approx_ideal) / (approx_nadir - approx_ideal)

    # Selecting single solution based on weights
    weights = opt_config.weights
    decomp = ASF()
    idx = decomp.do(nF, 1/weights).argmin()       # index of selected solution
    print("Best regarding ASF: Point \ni = %s\nF = %s" % (idx, F[idx]))

    # Visualizing
    visualize(problem, X, F, idx)
    input("Press [enter] to continue.")
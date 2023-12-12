import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.termination import get_termination
from pymoo.optimize import minimize

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
        weights (list[float]):            List of constrains
    """

    n_var: int = 1
    n_obj: int = 1
    n_ieq_constr: int = 1
    xl: np.ndarray = None
    xu: np.ndarray = None
    objective_fcn: list[Callable] = None
    constrains: list[Callable] = None
    weights: list[float] = None

# Configuration package for NSGA2 algorithm
@dataclass
class AlgorithmConfigurationNSGA2():
    """This class holds information about optimization problem

    Attributes:
        pop_size (int):                   Population size
        n_offsprings (int):               Number of offspring that are created through mating.
        crossover_prob (float):           Crossover operator will create a different number of offsprings dependent on the implementation.
        crossover_eta (int):              N
        mutation_eta (int):               N
        eliminate_duplicates (bool):      N

    """

    pop_size: int = 40
    n_offsprings: int = 10
    crossover_prob: float = 0.9
    crossover_eta: int = 15
    mutation_eta: int = 20
    eliminate_duplicates: bool = True

# Creating problem calss for optimization
class Problem(ElementwiseProblem):
    """General class to solve problem

    Inherited from base class for optimization problems-

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

# # Multiprocessing visualization
# def visualization(F, i):
#     plt.figure(figsize=(7, 5))
#     plt.scatter(F[:, 0], F[:, 1], s=30, facecolors='none', edgecolors='blue')
#     plt.scatter(F[i, 0], F[i, 1], marker="x", color="red", s=200)       # solution
#     plt.title("Objective Space")
#     plt.show()


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
    # TODO: wrap in try catch and send erro message to GUI at catch (maybe all core)
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
    problem_config.weights = np.array([0.2, 0.8])

    # Algorithm configuration
    # TODO: expect here branching based on algorithm
    algo_config = AlgorithmConfigurationNSGA2()
    algo_config.pop_size = 40
    # + other params (currently set to some default values)

    # Instanciating object of problem class
    problem = Problem(problem_config)

    # Creating algorithm for optimization
    algorithm = NSGA2(
        pop_size=algo_config.pop_size,
        n_offsprings=algo_config.n_offsprings,
        sampling=FloatRandomSampling(),
        crossover=SBX(prob=algo_config.crossover_prob, eta=algo_config.crossover_eta),
        mutation=PM(eta=algo_config.mutation_eta),
        eliminate_duplicates=algo_config.eliminate_duplicates
    )

    # Creating termination criteria
    # TODO: also as input?
    termination = get_termination("n_gen", 40)

    # Applying optimization (produces set of solutions)
    res = minimize(problem,
                   algorithm,
                   termination,
                   seed=1,
                   save_history=True,
                   verbose=True)

    # Storing solutions to variables
    X = res.X
    F = res.F

    # Normalization
    approx_ideal = F.min(axis=0)
    approx_nadir = F.max(axis=0)
    nF = (F - approx_ideal) / (approx_nadir - approx_ideal)

    # Selecting single solution based on weights
    weights = problem_config.weights
    decomp = ASF()
    i = decomp.do(nF, 1/weights).argmin()       # index of selected solution
    print("Best regarding ASF: Point \ni = %s\nF = %s" % (i, F[i]))

    # Visualizing
    # TODO: multiprocessing seems not required
    # TODO: consider 1, 2, 3 objectives
    xl, xu = problem.bounds()
    plt.figure(figsize=(7, 5))
    plt.scatter(X[:, 0], X[:, 1], s=30, facecolors='none', edgecolors='r')
    plt.scatter(X[i, 0], X[i, 1], marker="x", color="green", s=200)       # solution
    plt.xlim(xl[0], xu[0])
    plt.ylim(xl[1], xu[1])
    plt.title("Design Space")
    plt.ion()
    plt.show()

    plt.figure(figsize=(7, 5))
    plt.scatter(F[:, 0], F[:, 1], s=30, facecolors='none', edgecolors='blue')
    plt.scatter(F[i, 0], F[i, 1], marker="x", color="red", s=200)       # solution
    plt.title("Objective Space")
    plt.ion()
    plt.show()
    input("Press [enter] to continue.")
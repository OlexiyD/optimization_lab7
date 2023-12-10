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

# Inputs from GUI: 
# n_var, n_obj, n_ieq_constr, xl, xu, f1, f2, g1, g2
# NSGA2 + all params (there will be one more algo with other params)
# weights

# Output to GUI:
# X - length of n_var (simply few numbers)
# F - length of n_obj (simply few numbers)

# Creating problem calss for optimization
# TODO: modify to make f, g - variable length input params, other also as input
class MyProblem(ElementwiseProblem):

    def __init__(self):
        super().__init__(n_var=2,
                         n_obj=2,
                         n_ieq_constr=2,
                         xl=np.array([-2,-2]),
                         xu=np.array([2,2]))

    def _evaluate(self, x, out, *args, **kwargs):
        f1 = 100 * (x[0]**2 + x[1]**2)
        f2 = (x[0]-1)**2 + x[1]**2

        g1 = 2*(x[0]-0.1) * (x[0]-0.9) / 0.18
        g2 = - 20*(x[0]-0.4) * (x[0]-0.6) / 4.8

        out["F"] = [f1, f2]
        out["G"] = [g1, g2]

# Instanciating object of problem class
problem = MyProblem()

# Creating algorithm for optimization
algorithm = NSGA2(
    pop_size=40,
    n_offsprings=10,
    sampling=FloatRandomSampling(),
    crossover=SBX(prob=0.9, eta=15),
    mutation=PM(eta=20),
    eliminate_duplicates=True
)

# Creating termination criteria
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
weights = np.array([0.2, 0.8])
decomp = ASF()
i = decomp.do(nF, 1/weights).argmin()       # index of selected solution
print("Best regarding ASF: Point \ni = %s\nF = %s" % (i, F[i]))

# Visualizing
xl, xu = problem.bounds()
plt.figure(figsize=(7, 5))
plt.scatter(X[:, 0], X[:, 1], s=30, facecolors='none', edgecolors='r')
plt.scatter(X[i, 0], X[i, 1], marker="x", color="green", s=200)       # solution
plt.xlim(xl[0], xu[0])
plt.ylim(xl[1], xu[1])
plt.title("Design Space")
plt.show()

plt.figure(figsize=(7, 5))
plt.scatter(F[:, 0], F[:, 1], s=30, facecolors='none', edgecolors='blue')
plt.scatter(F[i, 0], F[i, 1], marker="x", color="red", s=200)       # solution
plt.title("Objective Space")
plt.show()
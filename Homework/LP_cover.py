from pyomo.environ import *
infinity = float('inf')

model = AbstractModel(sense=pyo.maximize)
# Covers
model.F = Set()

# Storage
model.N = Set()

# Revenue of each cover
model.c = Param(model.F, within=PositiveReals)
# Size of each cover
model.a = Param(model.F, model.N, within=NonNegativeReals)

# Lower and upper bound on each cover
model.Nmin = Param(model.N, within=NonNegativeReals, default =0.0)
model.Nmax = Param(model.N, within=NonNegativeReals, default=infinity)

# Maximum producing per each cover
model.V = Param(model.F, within=PositiveReals)

# Maximum producing of cover consumed
model.Vmax = Param(within=PositiveReals)

# Number of cover
model.x = Var(model.F, within=NonNegativeIntegers)

# Maximize the revenue of covered
def cost_rule(model):
    return sum(model.c[i] * model.x[i] for i in model.F) + 58500

# Limit for volume of covers
def volume_rule(model, j):
    value = sum(model.a[i, j] * model.x[i] for i in model.F)
    return inequality(model.Nmin[j], value, model.Nmax[j])

model.volume_limit = Constraint(model.N, rule=volume_rule)

def producing_rule(model):
    return sum(model.V[i]*model.x[i] for i in model.F) <= model.Vmax

model.producing = Constraint(rule=producing_rule)
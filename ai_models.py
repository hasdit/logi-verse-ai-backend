import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

# Load demo data
df = pd.read_csv("demo_data.csv")

# Demand prediction model
def predict_demand(product, days=7):
    np.random.seed(42)
    base_demand = df[df['product']==product]['quantity'].mean()
    forecast = base_demand + np.random.randint(-5, 10, size=days)
    return forecast.tolist()

# Route optimization (simplified demo)
def optimize_route(locations):
    # locations: list of (lat, lon)
    n = len(locations)
    distance_matrix = [[np.linalg.norm(np.array(locations[i])-np.array(locations[j])) for j in range(n)] for i in range(n)]
    manager = pywrapcp.RoutingIndexManager(n, 1, 0)
    routing = pywrapcp.RoutingModel(manager)
    def distance_callback(i, j):
        return int(distance_matrix[i][j]*1000)
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    solution = routing.SolveWithParameters(search_parameters)
    if solution:
        index = routing.Start(0)
        route = []
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))
        return route
    return list(range(n))

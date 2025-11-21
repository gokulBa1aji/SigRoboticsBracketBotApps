from graphslam.graph import Graph

g = Graph.from_g2o("trajectory.g2o")

g.plot()


g.optimize()


g.plot()
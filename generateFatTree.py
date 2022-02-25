import sys
from util.snakeCase import snake_case
import argparse
import os


class NetworkGenerator:
    def __init__(self, directory: str, r: int):
        self.r = r
        self.directory = directory

    def generate_tor_router(self):
        for pod in range(1, self.r * 2 + 1):
            for tor in range(1, self.r + 1):
                routerName = "TorP%dT%d" % (pod, tor)
                with open(os.path.join(self.directory, "%s.fib" % routerName), 'w') as fib:
                    for server in range(self.r):
                        fib.write("10.%d.%d.%d/32, %d\n" % (pod, tor, server, server))
                    fib.write("0.0.0.0/0," + ",".join(map(str, range(self.r, self.r * 2))) + "\n")
    
    def generate_leaf_router(self):
        for pod in range(1, self.r * 2 + 1):
            for set in range(1, self.r + 1):
                routerName = "LeafP%dS%d" % (pod, set)
                with open(os.path.join(self.directory, "%s.fib" % routerName), 'w') as fib:
                    for tor in range(self.r):
                        fib.write("10.%d.%d.0/24, %d\n" % (pod, tor, tor))
                    fib.write("0.0.0.0/0," + ",".join(map(str, range(self.r, self.r * 2))) + "\n")
    
    def generate_core_router(self):
        for set in range(1, self.r + 1):
            for redendency in range(1, self.r + 1):
                routerName = "CoreS%dR%d" % (set, redendency)
                with open(os.path.join(self.directory, "%s.fib" % routerName), 'w') as fib:
                    for pod in range(self.r * 2):
                        fib.write("10.%d.0.0/16, %d\n" % (pod, pod))

    def generate_topology(self):
        with open(os.path.join(self.directory, "topology.txt"), 'w') as edges:

            # tor-leaf connections
            for pod in range(1, self.r * 2 + 1):
                for tor in range(1, self.r + 1):
                    torRouterName = "TorP%dT%d" % (pod, tor)
                    for set in range(1, self.r + 1):
                        leafRouterName = "LeafP%dS%d" % (pod, set)
                        edges.write("%s,%s,%s,%d\n" % (torRouterName, set + self.r, leafRouterName, tor))
            edges.write("\n")

            # leaf-core connections
            for set in range(1, self.r + 1):
                for pod in range(1, self.r * 2 + 1):
                    leafRouterName = "LeafP%dS%d" % (pod, set)
                    for redendency in range(1, self.r + 1):
                        coreRouterName = "CoreS%dR%d" % (set, redendency)
                        edges.write("%s,%s,%s,%d\n" % (leafRouterName, redendency + self.r, coreRouterName, pod))
            edges.write("\n")
    
    def generate_code(self):
        self.generate_tor_router()
        self.generate_leaf_router()
        self.generate_core_router()
        self.generate_topology()
                        


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generates config for a fat-tree architecture')
    parser.add_argument('-d', dest='directory', required=True, help='select config directory of the network')
    parser.add_argument('-r', dest='redundency', type=int, required=True, help='redundency of nodes')

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        os.mkdir(args.directory)

    g = NetworkGenerator(args.directory, args.redundency)
    g.generate_code()

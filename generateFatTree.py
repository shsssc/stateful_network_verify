import argparse
import os


class FatTreeGenerator:
    def __init__(self, directory: str, r: int, lb_prefix: str):
        self.r = r
        self.directory = directory
        self.lb_prefix = lb_prefix

    def generate_tor_router(self):
        for pod in range(1, self.r * 2 + 1):
            for tor in range(1, self.r + 1):
                routerName = self.lb_prefix + ("TorP%dT%d" % (pod, tor))
                with open(os.path.join(self.directory, "%s.fib" % routerName), 'w') as fib:
                    for server in range(1, self.r + 1):
                        pass # fib.write("10.%d.%d.%d/32, %d\n" % (pod, tor, server, server))
                    fib.write("10.%d.%d.0/24, -1\n" % (pod, tor))
                    fib.write("0.0.0.0/0," + ",".join(map(str, range(self.r, self.r * 2))) + "\n")
    
    def generate_leaf_router(self):
        for pod in range(1, self.r * 2 + 1):
            for set in range(1, self.r + 1):
                routerName = self.lb_prefix + ("LeafP%dS%d" % (pod, set))
                with open(os.path.join(self.directory, "%s.fib" % routerName), 'w') as fib:
                    for tor in range(1, 1 + self.r):
                        fib.write("10.%d.%d.0/24, %d\n" % (pod, tor, tor - 1))
                    fib.write("10.%d.0.0/16, -1\n" % (pod))
                    fib.write("0.0.0.0/0," + ",".join(map(str, range(self.r, self.r * 2))) + "\n")
    
    def generate_core_router(self):
        for set in range(1, self.r + 1):
            for redendency in range(1, self.r + 1):
                routerName = "CoreS%dR%d" % (set, redendency)
                with open(os.path.join(self.directory, "%s.fib" % routerName), 'w') as fib:
                    for pod in range(1, self.r * 2 + 1):
                        fib.write("10.%d.0.0/16, %d\n" % (pod, pod - 1))

    def generate_topology(self):
        with open(os.path.join(self.directory, "topology.txt"), 'w') as edges:

            # tor-leaf connections
            for pod in range(1, self.r * 2 + 1):
                for tor in range(1, self.r + 1):
                    torRouterName = self.lb_prefix + ("TorP%dT%d" % (pod, tor))
                    for set in range(1, self.r + 1):
                        leafRouterName = self.lb_prefix + ("LeafP%dS%d" % (pod, set))
                        edges.write("%s,%s,%s,%d\n" % (torRouterName, set + self.r - 1, leafRouterName, tor - 1))
            edges.write("\n")

            # leaf-core connections
            for set in range(1, self.r + 1):
                for pod in range(1, self.r * 2 + 1):
                    leafRouterName = self.lb_prefix + ("LeafP%dS%d" % (pod, set))
                    for redendency in range(1, self.r + 1):
                        coreRouterName = "CoreS%dR%d" % (set, redendency)
                        edges.write("%s,%s,%s,%d\n" % (leafRouterName, redendency + self.r - 1, coreRouterName, pod - 1))
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
    parser.add_argument('-l', dest='load_balance_prefix', default='Ecmp', help="Load balancing model used")

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        os.mkdir(args.directory)

    g = FatTreeGenerator(args.directory, args.redundency, args.load_balance_prefix)
    g.generate_code()

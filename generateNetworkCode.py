from generateTopology import TopologyGenerator
from generateRouterHeader import RouterGenerator
import argparse
import os

class NetworkGenerator:
    def __init__(self, directory: str):
        self.directory = directory
        self.topologyCode = TopologyGenerator(hop=16)
        self.topologyCode.add_forwarding_table(os.path.join(directory, "topology.txt"))
        self.routerCodes = []
        for item in os.scandir(directory):
            if item.is_file() and item.name != "topology.txt" and item.name.endswith(".txt"):
                a = RouterGenerator(item.name[:item.name.rindex(".txt")])
                a.add_forwarding_table(os.path.join(directory, item.name))
                self.routerCodes.append(a)


    def generate_code(self):
        with open(os.path.join(self.directory, "topology.h"), 'w') as f:
            f.write(self.topologyCode.generate_code())
        for e in self.routerCodes:
            with open(os.path.join(self.directory, e.name + ".h"), 'w') as routerFile:
                routerFile.write(e.generate_code())
        os.system('cp templates/Makefile "%s"' % self.directory)
        os.system('cp templates/common.h "%s"' % self.directory)
        os.system('cp templates/test-driver.cpp "%s"' % self.directory)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generates C++ model code for a network')
    parser.add_argument('-d', dest='directory', help='select config directory of the network')

    args = parser.parse_args()

    g = NetworkGenerator(args.directory)
    g.generate_code()
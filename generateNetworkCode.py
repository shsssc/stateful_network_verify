from generateTopology import TopologyGenerator
from generateRouterHeader import RouterGenerator
from generateSrcReachabilityTestDriver import SrcReachabilityDriverGenerator
import argparse
import os


class NetworkGenerator:
    def __init__(self, directory: str, src: str, port: int):
        self.directory = directory
        self.topologyCode = TopologyGenerator(hop=16)
        self.topologyCode.add_forwarding_table(os.path.join(directory, "topology.txt"))
        self.driverCode = SrcReachabilityDriverGenerator(src, port)
        self.driverCode.add_node_name_to_id_map(self.topologyCode.nodes)
        self.routerCodes = []
        for item in os.scandir(directory):
            if item.is_file() and item.name != "topology.txt" and item.name.endswith(".txt"):
                class_name = item.name[:item.name.rindex(".txt")]
                a = RouterGenerator(class_name.capitalize())
                a.add_forwarding_table(os.path.join(directory, item.name))
                self.routerCodes.append(a)

    def generate_code(self):
        with open(os.path.join(self.directory, "topology.h"), 'w') as f:
            f.write(self.topologyCode.generate_code())
        with open(os.path.join(self.directory, "test-driver.cpp"), 'w') as f:
            f.write(self.driverCode.generate_code())
        for e in self.routerCodes:
            with open(os.path.join(self.directory, e.name.lower() + ".h"), 'w') as routerFile:
                routerFile.write(e.generate_code())
        os.system('cp templates/Makefile "%s"' % self.directory)
        os.system('cp templates/common.h "%s"' % self.directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generates C++ model code for a network')
    parser.add_argument('-d', dest='directory', help='select config directory of the network')
    parser.add_argument('-s', dest='src', help='src node')
    parser.add_argument('-p', dest='port', default="0", help='src port')

    args = parser.parse_args()

    g = NetworkGenerator(args.directory, args.src, int(args.port))
    g.generate_code()

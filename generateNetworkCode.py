import sys

from generateACLHeader import ACLGenerator
from generateTopology import TopologyGenerator
from generateRouterHeader import RouterGenerator
from generateSrcReachabilityTestDriver import SrcReachabilityDriverGenerator
from util.snakeCase import snake_case
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
        self.aclCodes = []
        for item in os.scandir(directory):
            if item.is_file() and item.name.endswith(".txt"):
                if item.name == "topology.txt":
                    pass
                elif str(item.name).lower().startswith("acl"):
                    class_name = item.name[:item.name.rindex(".txt")]
                    a = ACLGenerator(class_name)
                    a.add_acl_table(os.path.join(directory, item.name))
                    self.aclCodes.append(a)
                else:
                    class_name = item.name[:item.name.rindex(".txt")]
                    a = RouterGenerator(class_name)
                    a.add_forwarding_table(os.path.join(directory, item.name))
                    self.routerCodes.append(a)

    def generate_code(self):
        with open(os.path.join(self.directory, "topology.h"), 'w') as f:
            f.write(self.topologyCode.generate_code())
        with open(os.path.join(self.directory, "test-driver.cpp"), 'w') as f:
            f.write(self.driverCode.generate_code())
        for e in self.routerCodes:
            with open(os.path.join(self.directory, snake_case(e.name) + ".h"), 'w') as routerFile:
                routerFile.write(e.generate_code())
        for e in self.aclCodes:
            with open(os.path.join(self.directory, snake_case(e.name) + ".h"), 'w') as aclFile:
                aclFile.write(e.generate_code())
        os.system('cp templates/Makefile "%s"' % self.directory)
        os.system('cp templates/common.h "%s"' % self.directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generates C++ model code for a network')
    parser.add_argument('-d', dest='directory', required=True, help='select config directory of the network')
    parser.add_argument('-s', dest='src', required=True, help='src node')
    parser.add_argument('-p', dest='port', type=int, default=0, help='src port')

    args = parser.parse_args()

    g = NetworkGenerator(args.directory, args.src, args.port)
    g.generate_code()

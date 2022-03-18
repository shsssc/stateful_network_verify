from generateEcmpRouterHeader import EcmpRouterGenerator
from generateRoundRobinRouterHeader import RoundRobinRouterGenerator
from generateDynamicNatRouterHeader import DynamicNatGenerator
from generateTopology import TopologyGenerator
from generateRouterHeader import RouterGenerator
from generateSrcReachabilityTestDriver import SrcReachabilityDriverGenerator
from util.snakeCase import snake_case
import argparse
import os
from generateOptimizedRouterHeader import OptimizedRouterHeaderGenerator
from typing import Set, Dict


class NetworkGenerator:
    def __init__(self, directory: str, use_ec_opt=False):
        self.directory = directory
        self.useEcs = use_ec_opt
        self.routerToEcCode: Dict[str, OptimizedRouterHeaderGenerator] = dict()
        self.topologyCode = TopologyGenerator()
        self.topologyCode.add_forwarding_table(os.path.join(directory, "topology.txt"))
        self.routerCodes = {}
        self.scanDir(directory)

    def addRouterInstance(self, class_name: str):
        if class_name not in self.routerCodes:
            if class_name.lower().startswith('ecmp'):
                self.routerCodes[class_name] = EcmpRouterGenerator(class_name)
            elif class_name.lower().startswith('rr'):
                self.routerCodes[class_name] = RoundRobinRouterGenerator(class_name)
            elif class_name.lower().startswith('nat'):
                self.routerCodes[class_name] = DynamicNatGenerator(class_name)
            else:
                self.routerCodes[class_name] = RouterGenerator(class_name)

    def scanDir(self, directory: str):
        for item in os.scandir(directory):
            if item.is_file():
                if item.name == "topology.txt":
                    pass
                elif item.name.endswith(".acl"):
                    class_name = item.name[:-4]
                    self.addRouterInstance(class_name)
                    self.routerCodes[class_name].add_acl_table(os.path.join(directory, item.name))
                elif item.name.endswith(".fib"):
                    class_name = item.name[:-4]
                    self.addRouterInstance(class_name)
                    self.routerCodes[class_name].add_forwarding_table(os.path.join(directory, item.name))
                elif self.useEcs and item.name.endswith("ecs.csv"):
                    ecs = OptimizedRouterHeaderGenerator(os.path.join(directory, item.name))
                    for r in ecs.sorted_disjoint_intervals:
                        self.routerToEcCode[r] = ecs

    def generate_code(self):
        with open(os.path.join(self.directory, "topology.h"), 'w') as f:
            f.write(self.topologyCode.generate_code())
        for e in self.routerCodes.values():
            with open(os.path.join(self.directory, snake_case(e.name) + ".h"), 'w') as routerFile:
                routerFile.write(e.generate_code())
        if self.useEcs:
            for r, v in self.routerToEcCode.items():
                with open(os.path.join(self.directory, snake_case(r) + ".h"), 'w') as routerFile:
                    routerFile.write(v.generate_code(r))


class ReachabilityCodeGenerator(NetworkGenerator):
    def __init__(self, directory: str, src: str, port: int, use_ec_opt=False, stateful_main=False):
        super().__init__(directory, use_ec_opt)
        self.driverCode = SrcReachabilityDriverGenerator(src, port,
                                                         hop=self.topologyCode.diameter() * 3, stateful=stateful_main)  # TTL = diameter * 3 as best effort loop detection
        self.driverCode.add_node_name_to_id_map(self.topologyCode.nodes)

    def generate_code(self):
        super().generate_code()
        with open(os.path.join(self.directory, "test-driver.cpp"), 'w') as f:
            f.write(self.driverCode.generate_code())
        os.system('cp templates/Makefile "%s"' % self.directory)
        os.system('cp templates/common.h "%s"' % self.directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generates C++ model code for a network')
    parser.add_argument('-d', dest='directory', required=True, help='select config directory of the network')
    parser.add_argument('-s', dest='src', required=True, help='src node')
    parser.add_argument('-p', dest='port', type=int, default=0, help='src port')
    parser.add_argument('-o', dest='optimize', type=bool, default=False,
                        help='search for csv files that treat network boxes as components to save computation')
    parser.add_argument('--stateful', action='store_true', dest='stateful', default=False, help='check for stateful reachability')
    args = parser.parse_args()

    g = ReachabilityCodeGenerator(args.directory, args.src, args.port, args.optimize, stateful_main=args.stateful)
    g.generate_code()

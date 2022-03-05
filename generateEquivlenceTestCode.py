from generateNetworkCode import NetworkGenerator
from generatePathEquivlenceTestDriver import PathEquivlenceDriverGenerator
import argparse
import os

class EquivlenceCodeGenerator(NetworkGenerator):
    def __init__(self, directory: str, src: str, port: int, nodesRegex: str):
        super().__init__(directory)
        self.driverCode = PathEquivlenceDriverGenerator(src, port, hop=self.topologyCode.diameter() * 3, nodesRegex=nodesRegex) # TTL = diameter * 3 as best effort loop detection
        self.driverCode.add_node_name_to_id_map(self.topologyCode.nodes)

    def generate_code(self):
        super().generate_code()
        with open(os.path.join(self.directory, "test-driver.cpp"), 'w') as f:
            f.write(self.driverCode.generate_code())
        os.system('cp templates/Makefile-equivlence "%s/Makefile"' % self.directory)
        os.system('cp templates/common.h "%s"' % self.directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generates C++ model code for a network')
    parser.add_argument('-d', dest='directory', required=True, help='select config directory of the network')
    parser.add_argument('-s', dest='src', required=True, help='src node')
    parser.add_argument('-p', dest='port', type=int, default=0, help='src port')
    parser.add_argument('-e', dest='nodesRegex', required=True, help='regex to select equivlent nodes')

    args = parser.parse_args()

    g = EquivlenceCodeGenerator(args.directory, args.src, args.port, args.nodesRegex)
    g.generate_code()

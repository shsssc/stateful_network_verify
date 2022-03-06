import argparse
from generateNetworkCode import NetworkGenerator
from generateLoopTestDriver import LoopDetectionDriverGenerator
import os

class LoopDetectionCodeGenerator(NetworkGenerator):
    def __init__(self, directory: str):
        super().__init__(directory)
        self.driverCode = LoopDetectionDriverGenerator(
            hop=self.topologyCode.diameter() * 3)  # TTL = diameter * 3 as best effort loop detection

    def generate_code(self):
        super().generate_code()
        with open(os.path.join(self.directory, "test-driver.cpp"), 'w') as f:
            f.write(self.driverCode.generate_code())
        os.system('cp templates/Makefile "%s"' % self.directory)
        os.system('cp templates/common.h "%s"' % self.directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generates C++ model code for a network')
    parser.add_argument('-d', dest='directory', required=True, help='select config directory of the network')

    args = parser.parse_args()

    g = LoopDetectionCodeGenerator(args.directory)
    g.generate_code()

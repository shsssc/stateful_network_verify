import string, csv, sys, socket, struct
import argparse
from util.jinjaEnv import jinja_env


class LoopDetectionDriverGenerator:
    def __init__(self, hop: int):
        self.hop = hop
        self.node_name_to_id = dict()

    def generate_code(self) -> str:
        template = jinja_env.get_template("templates/test-driver-loop.cpp")
        return template.render(hop=self.hop)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generates a main function for reachability from a node')
    parser.add_argument('-o', dest='output', default="-", help='file name of output code')
    parser.add_argument('-p', dest='hop', type=int, default=16, help='simulation hop limit')

    args = parser.parse_args()

    a = SrcReachabilityDriverGenerator(args.hop)

    if args.output == "-":
        print(a.generate_code())
    else:
        with open(args.output, 'w') as f:
            f.write(a.generate_code())

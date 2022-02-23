import string, csv, sys, socket, struct
import argparse
from util.jinjaEnv import jinja_env

class SrcReachabilityDriverGenerator:
    def __init__(self, src: str, port: int):
        self.src = src
        self.port = port
        self.node_name_to_id = dict()

    def add_node_name_to_id_map(self, m: dict):
        self.node_name_to_id = m

    def generate_code(self) -> str:
        template = jinja_env.get_template("templates/test-driver.cpp")
        return template.render(src=self.node_name_to_id[self.src], port=self.port)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generates a main function for reachability from a node')
    parser.add_argument('-s', dest='src', required=True, help='source node ID')
    parser.add_argument('-p', dest='port', type=int, default=0, help='source port ID')
    parser.add_argument('-o', dest='output', default="-", help='file name of output code')
    parser.add_argument('-m', dest='map', default="", help='read router name to id map from csv')

    args = parser.parse_args()

    a = SrcReachabilityDriverGenerator(args.src, int(args.port))

    with open(args.map, 'r') as f:
        name_to_id = dict()
        tsv = csv.reader(f)
        for row in tsv:
            name_to_id[row[0]] = row[1]
        a.add_node_name_to_id_map(name_to_id)

    if args.output == "-":
        print(a.generate_code())
    else:
        with open(args.output, 'w') as f:
            f.write(a.generate_code())

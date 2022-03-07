import re, csv, argparse
from util.jinjaEnv import jinja_env

class BalanceDriverGenerator:
    def __init__(self, src: str, port: int, hop: int, nodesRegex: str):
        self.src = src
        self.port = port
        self.hop = hop
        self.node_name_to_id = dict()
        self.nodesRegex = nodesRegex

    def add_node_name_to_id_map(self, m: dict):
        self.node_name_to_id = m

    def generate_code(self) -> str:
        template = jinja_env.get_template("templates/test-driver-balance.cpp")
        node_ids = list(map(lambda n : self.node_name_to_id[n], 
            filter(lambda e: re.match(self.nodesRegex, e), self.node_name_to_id.keys())))
        node_ids.sort()
        return template.render(src=self.node_name_to_id[self.src], port=self.port, hop=self.hop, 
        equivlent_nodes=node_ids, equivlent_nodes_max=node_ids[-1])


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generates a main function for reachability from a node')
    parser.add_argument('-s', dest='src', required=True, help='source node ID')
    parser.add_argument('-p', dest='port', type=int, default=0, help='source port ID')
    parser.add_argument('-o', dest='output', default="-", help='file name of output code')
    parser.add_argument('-m', dest='map', default="", help='read router name to id map from csv')
    parser.add_argument('-p', dest='hop', type=int, default=16, help='simulation hop limit')
    parser.add_argument('-e', dest='nodesRegex', required=True, help='regex to select equivlent nodes')

    args = parser.parse_args()

    a = BalanceDriverGenerator(args.src, int(args.port), args.hop, args.nodesRegex)

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

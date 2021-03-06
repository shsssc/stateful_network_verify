import string, csv, sys, socket, struct
import argparse
from util.jinjaEnv import jinja_env
from util.snakeCase import snake_case
import networkx as nx


class TopologyGenerator:
    def __init__(self):
        self.links = []
        self.nodes = dict()
        self.G = nx.Graph()

    def __get_node_id(self, nodeName: str, nodes: dict):
        if nodeName in nodes:
            return nodes.get(nodeName)
        result = len(nodes)
        nodes[nodeName] = result
        return result

    def add_forwarding_table(self, file: str):
        links = []
        nodes = dict()
        with open(file, 'r') as f:
            tsv = csv.reader(f)
            for row in tsv:
                if len(row) == 0: continue
                node1 = self.__get_node_id(row[0], nodes)
                self.G.add_node(node1)
                port1 = row[1]
                node2 = self.__get_node_id(row[2], nodes)
                self.G.add_node(node1)
                port2 = row[3]
                links.append({'n_from': node1, 'p_from': port1, 'n_to': node2, 'p_to': port2})
                links.append({'n_from': node2, 'p_from': port2, 'n_to': node1, 'p_to': port1})
                self.G.add_edge(node1, node2)

        self.links = links
        self.nodes = nodes

    def diameter(self):
        return nx.diameter(self.G)

    def generate_code(self) -> str:
        template = jinja_env.get_template("templates/topology.h")
        return template.render(nodes=self.nodes, links=self.links, snake_case=snake_case)

    def generate_name_2_node_map(self) -> str:
        return '\n'.join([f"{k},{v}" for k, v in self.nodes.items()])


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generates C++ model code for network topology')
    parser.add_argument('-t', dest='table', required=True, help='file name of topology table')
    parser.add_argument('-o', dest='output', default="-", help='file name of output code')
    parser.add_argument('-m', dest='map', default="", help='save router to id map to csv')

    args = parser.parse_args()

    a = TopologyGenerator()
    a.add_forwarding_table(args.table)
    if args.output == "-":
        print(a.generate_code())
    else:
        with open(args.output, 'w') as f:
            f.write(a.generate_code())
    if args.map == "-":
        print("// node name to node id map:")
        print("// " + a.generate_name_2_node_map().replace("\n", "\n// "))
    elif args.map == "":
        pass
    else:
        with open(args.map, 'w') as f:
            f.write(a.generate_name_2_node_map())

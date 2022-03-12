from typing import Set, Dict
import os
from util.trie import Trie
from util.IPPrefixDecode import decode_ip_prefix
import csv
import sys
import ipaddress
from generateNetworkCode import NetworkGenerator
from util.jinjaEnv import jinja_env
import argparse
import re


class APGenerator(NetworkGenerator):
    def __init__(self, directory: str, nodes_regx: re, out_file: str = 'ecs.csv'):
        super().__init__(directory)
        self.trie = Trie()
        self.ecs = []
        self.directory = directory
        self.nodes = self.re_to_nodes(nodes_regx)
        self.build_trie()
        self.ecs = self.all_concrete_ec()
        self.driverCode = APDriverGenerator(nodes=self.nodes, hop=self.topologyCode.diameter() + 2, ecs=self.ecs)
        self.out_file = out_file

    def all_ec(self):
        return self.trie.all_ec()

    def all_concrete_ec(self):
        result = []
        ecs = self.all_ec()
        for ec in ecs:
            ec_norm = ec + '0' * (32 - len(ec))
            ip = int(ec_norm, 2)
            result.append({'prefix': ec, 'concrete': ip})
            # ip = ipaddress.ip_address(ip)
            # print(ip)
        return result

    def build_trie(self):
        for n in self.nodes:
            file = os.path.join(self.directory, n + '.fib')
            with open(file, 'r') as f:
                tsv = csv.reader(f)
                for row in tsv:
                    if len(row) == 0: continue
                    try:
                        prefix = decode_ip_prefix(row[0])
                        ip = '{:032b}'.format(int(prefix['hex_address'], 0))
                        bin_prefix = ip[0:prefix['prefix_len']]
                        self.trie.add(bin_prefix)
                    except RuntimeError as ex:
                        sys.stderr.write("Bad forwarding table line %s\n" % row)
                        sys.stderr.write(ex.args[0] + "\n")
                        sys.exit(1)

    def generate_code(self):
        super().generate_code()
        with open(os.path.join(self.directory, "test-driver.cpp"), 'w') as f:
            f.write(self.driverCode.generate_code())
        os.system('cp templates/Makefile "%s"' % self.directory)
        os.system('cp templates/common.h "%s"' % self.directory)

    def execute_model(self):
        # XXX: not using makefile
        os.system(f'cd "%s" && c++ test-driver.cpp && ./a.out > "{self.out_file}"' % self.directory)
        os.remove(os.path.join(self.directory, 'a.out'))

    def re_to_nodes(self, regex: str):
        result: list = list()
        for item in os.scandir(self.directory):
            if item.name.endswith(".fib"):
                class_name = item.name[:-4]
                if re.match(regex, class_name):
                    result.append(class_name)
        #print(result)
        #exit(0)
        return result


class APDriverGenerator:
    def __init__(self, nodes: Set[str], hop: int, ecs: list):
        self.nodes = nodes
        self.hop = hop
        self.ecs = ecs

    def generate_code(self) -> str:
        template = jinja_env.get_template("templates/ecgen-driver.cpp")
        return template.render(nodes=self.nodes, hop=self.hop, ecs=self.ecs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generates C++ model code for a network')
    parser.add_argument('-d', dest='directory', required=True, help='select config directory of the network')
    parser.add_argument('-e', dest='nodesRegex', required=True, help='regex to select node names to run optimization')
    parser.add_argument('-o', dest='output', default='ecs.csv', required=False, help='output file name')

    args = parser.parse_args()

    g = APGenerator(args.directory, args.nodesRegex, args.output)
    g.generate_code()
    g.execute_model()

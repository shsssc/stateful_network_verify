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


class APGenerator(NetworkGenerator):
    def __init__(self, directory: str, nodes: Set[str], out_file: str = 'ecs.csv'):
        super().__init__(directory)
        self.nodes = nodes
        self.trie = Trie()
        self.ecs = []
        self.directory = directory
        self.build_trie()
        self.ecs = self.all_concrete_ec()
        self.driverCode = APDriverGenerator(nodes=nodes, hop=self.topologyCode.diameter() + 2, ecs=self.ecs)
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


class APDriverGenerator:
    def __init__(self, nodes: Set[str], hop: int, ecs: list):
        self.nodes = nodes
        self.hop = hop
        self.ecs = ecs

    def generate_code(self) -> str:
        template = jinja_env.get_template("templates/ecgen-driver.cpp")
        return template.render(nodes=self.nodes, hop=self.hop, ecs=self.ecs)


class ECToCode:
    def __init__(self, file: str):
        self.file = file
        self.sorted_disjoint_intervals: Dict[str, list] = dict()

        records: Dict[str, list] = dict()
        with open(file, 'r') as f:
            tsv = csv.reader(f)
            for row in tsv:
                node = row[0]
                prefix = row[1]
                out_node = int(row[2])
                out_port = int(row[3])
                if node not in records:
                    records[node] = []
                records[node].append((prefix, (out_node, out_port)))
        for node, l in records.items():
            # intervals are already disjoint thanks to trie
            l.sort(key=lambda x: int(x[0] + '0' * (32 - len(x[0])), 2))  # sort with interval start
            merged_intervals = self.__merge_intervals(l)

            self.sorted_disjoint_intervals[node] = merged_intervals

    def __merge_intervals(self, intervals: list):
        result = []
        if len(intervals) == 0:
            return
        l = 0
        r = l
        while l < len(intervals):
            while r < len(intervals) and intervals[r][1] == intervals[l][1]:
                r += 1
            start = int(intervals[l][0] + '0' * (32 - len(intervals[l][0])), 2)
            end = int(intervals[r - 1][0] + '1' * (32 - len(intervals[r - 1][0])), 2)
            result.append((start, end, intervals[l][1]))
            l = r
        return result

    def generate_code(self, node: str):
        return self.__generate_code(self.sorted_disjoint_intervals[node], 0,
                                    len(self.sorted_disjoint_intervals[node]) - 1, 0)

    def __generate_code(self, intervals: list, l: int, r: int, level: int):
        if r < l:
            return ''
        if r == l:
            interval = intervals[r]
            node = interval[2][0]
            port = interval[2][1]
            return f"{' ' * 4 * level}return {{header, {node}, {port}}};"
        m = (r + l) // 2
        interval = intervals[m]
        node = interval[2][0]
        port = interval[2][1]
        start = interval[0]
        end = interval[1]
        return f"{' ' * 4 * level}if (header.dst_address >= {hex(start)} && header.dst_address <= {hex(end)})" \
               f" return {{header, {node}, {port}}};\n" \
               f"{' ' * 4 * level}else if (header.dst_address < {hex(start)}) {{\n" \
               f"{self.__generate_code(intervals, l, m - 1, level + 1)}\n" \
               f"{' ' * 4 * level}}} else {{\n" \
               f"{self.__generate_code(intervals, m + 1, r, level + 1)}\n" \
               f"{' ' * 4 * level}}}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generates C++ model code for a network')
    parser.add_argument('-d', dest='directory', required=True, help='select config directory of the network')
    parser.add_argument('-c', dest='component', required=True, help=', seperated node names to run optimization')

    args = parser.parse_args()

    component = set()
    for c in args.component.split(','):
        component.add(c)

    g = APGenerator(args.directory, component)
    g.generate_code()
    g.execute_model()

    i = ECToCode('Example 3/ecs.csv')
    print(i.generate_code('Router1'))

from typing import Dict
import csv
import csv, sys, argparse
from util.jinjaEnv import jinja_env
from util.snakeCase import snake_case


class OptimizedRouterHeaderGenerator:
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
        template = jinja_env.get_template("templates/optrouter.h")
        code = self.__generate_code(self.sorted_disjoint_intervals[node], 0,
                                    len(self.sorted_disjoint_intervals[node]) - 1, 2)
        return template.render(name=node, code=code,
                               name_snake=snake_case(node))

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
        return f"{' ' * 4 * level}if (header.dst_address >= {hex(start)} && header.dst_address <= {hex(end)})\n" \
               f"{' ' * (4 * level + 4)}return {{header, {node}, {port}}};\n" \
               f"{' ' * 4 * level}else if (header.dst_address < {hex(start)}) {{\n" \
               f"{self.__generate_code(intervals, l, m - 1, level + 1)}\n" \
               f"{' ' * 4 * level}}} else {{\n" \
               f"{self.__generate_code(intervals, m + 1, r, level + 1)}\n" \
               f"{' ' * 4 * level}}}"

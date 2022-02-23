from typing import Dict, Set
import sys
import argparse
import os


def read_coverage_from_file(file: str) -> Dict[str, Set[int]]:
    f = open(file, 'r')
    function_file: str = "N/A"
    lines = f.readlines()

    file_to_coverage: Dict[str, Set[int]] = dict()
    for l in lines:
        if l[0:3] == 'fl=':
            file_name = l[l.find("=") + 1:-1]
            function_file = file_name
        if l.find('=') == -1 and l.find(':') == -1 and len(l) > 5:
            line_number = int(l.split(' ')[1])
            if line_number == 0:
                continue
            if function_file in file_to_coverage:
                file_to_coverage[function_file].add(line_number)
            else:
                file_to_coverage[function_file] = set()
                file_to_coverage[function_file].add(line_number)
    f.close()
    return file_to_coverage


def read_generated_comments(cov: Dict[str, Set[int]], src_dir: str):
    result = []
    for f_name, line_set in cov.items():
        if f_name[0:2] != './' and f_name.find('/') > 0:
            continue
        with open(os.path.join(src_dir, f_name), 'r') as f:
            lines = f.readlines()
            for x in line_set:
                line = lines[x - 1]
                if line.find('//generated-comment') >= 0:
                    result.append(line[line.find('//generated-comment') + len('//generated-comment: '):].strip())
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Read all generated comments from klee-out')
    parser.add_argument('-d', dest='directory', required=True, help='klee-out director')
    parser.add_argument('-s', dest='src', required=True, help='source file directory')

    args = parser.parse_args()

    file_to_coverage = read_coverage_from_file(os.path.join(args.directory, 'run.istats'))

    result = read_generated_comments(file_to_coverage, args.src)
    for r in result:
        print(r)

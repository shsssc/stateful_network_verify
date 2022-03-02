from typing import Dict, Set
import sys
import argparse
import os


def read_coverage_from_file(file: str) -> Dict[str, Set[int]]:
    f = open(file, 'r')
    lines = f.readlines()

    file_to_coverage: Dict[str, Set[int]] = dict()
    for l in lines:
        file_name, line_number = l.split(":")
        line_number = int(line_number)
        if file_name in file_to_coverage:
            file_to_coverage[file_name].add(line_number)
        else:
            file_to_coverage[file_name] = set()
            file_to_coverage[file_name].add(line_number)
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
    parser.add_argument('-c', dest='coverage', required=True, help='coverage map file')
    parser.add_argument('-s', dest='src', required=True, help='source file directory')

    args = parser.parse_args()

    file_to_coverage = read_coverage_from_file(args.coverage)
    result = read_generated_comments(file_to_coverage, args.src)
    for r in result:
        print(r)

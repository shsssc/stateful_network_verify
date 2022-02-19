from typing import Dict, Set

f = open('../Example 3/klee-out-0/run.istats', 'r')
currentFile: str = "N/A"
lines = f.readlines()

file_to_coverage: Dict[str, Set[int]] = dict()
for l in lines:
    if l[0:3] == 'fl=' or l[0:4] == 'fl=':
        file_name = l[l.find("=") + 1:-1]
        currentFile = file_name
    if l.find('=') == -1 and l.find(':') == -1 and len(l) > 5:
        line_number = int(l.split(' ')[1])
        if currentFile in file_to_coverage:
            file_to_coverage[currentFile].add(line_number)
        else:
            file_to_coverage[currentFile] = set()
            file_to_coverage[currentFile].add(line_number)
for k,v in file_to_coverage.items():
    print(f"{k}: line {v}")
f.close()

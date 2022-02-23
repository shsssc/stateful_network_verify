import csv, sys, argparse
from util.jinjaEnv import jinja_env
from util.snakeCase import snake_case
from util.IPPrefixDecode import decode_ip_prefix

class RouterGenerator:
    def __init__(self, name: str):
        self.name = name
        self.table = [] # dict: str_address, prefix_len, port, hex_address

    def add_forwarding_table(self, file: str):
        self.table = []
        with open(file, 'r') as f:
            tsv = csv.reader(f)
            for row in tsv:
                try:
                    prefix = decode_ip_prefix(row[0])
                    self.table.append({**prefix, 'port': int(row[1])})
                except RuntimeError as ex:
                    sys.stderr.write("Bad forwarding table line %s\n" % row)
                    sys.stderr.write(ex.args[0] + "\n")
                    sys.exit(1)
        self.table.sort(key=lambda e: e['prefix_len'], reverse=True)

    def generate_code(self) -> str:
        template = jinja_env.get_template("templates/router.h")
        return template.render(name=self.name, table=self.table, name_snake=snake_case(self.name))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generates C++ model code for a router')
    parser.add_argument('-n', dest='name', required=True, help='select name of router')
    parser.add_argument('-t', dest='table', required=True, help='file name of forwarding table')
    parser.add_argument('-o', dest='output', default="-", help='file name of output code')

    args = parser.parse_args()

    a = RouterGenerator(args.name)
    a.add_forwarding_table(args.table)
    if args.output == "-":
        print(a.generate_code())
    else:
        with open(args.output, 'w') as f:
            f.write(a.generate_code())
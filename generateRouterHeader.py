import string, csv, sys, socket, struct
import argparse
from util.jinjaEnv import jinja_env
from util.snakeCase import snake_case

class RouterGenerator:
    def __init__(self, name: str):
        self.name = name
        self.table = [] # dict: str_address, prefix_len, port, hex_address

    def add_forwarding_table(self, file: str):
        self.table = []
        with open(file, 'r') as f:
            tsv = csv.reader(f)
            for row in tsv:
                prefix = row[0].split("/")
                if len(prefix) != 2:
                    sys.stderr.write("Bad forwarding table line %s\n" % row)
                packed_ip = socket.inet_aton(prefix[0])
                hex_ip = hex(struct.unpack("!L", packed_ip)[0])
                self.table.append({'str_address': prefix[0], 'prefix_len': int(prefix[1]),
                              'port': int(row[1]), 'hex_address': hex_ip})
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
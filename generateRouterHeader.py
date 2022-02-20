import string, csv, sys, socket, struct
from jinja2 import Environment, FileSystemLoader, select_autoescape
import argparse

jinja_env = Environment(
    loader=FileSystemLoader("."),
    autoescape=select_autoescape()
)
jinja_env.trim_blocks = True
jinja_env.lstrip_blocks = True

class RouterGenerator:
    def __init__(self, name: str):
        self.name = name
        self.table = [] # dict: str_address, prefix_len, port, hex_address

    def add_forwarding_table(self, file: str):
        table = []
        with open(file, 'r') as f:
            tsv = csv.reader(f)
            for row in tsv:
                prefix = row[0].split("/")
                if len(prefix) != 2:
                    sys.stderr.write("Bad forwarding table line %s\n" % row)
                packed_ip = socket.inet_aton(prefix[0])
                hex_ip = hex(struct.unpack("!L", packed_ip)[0])
                table.append({'str_address': prefix[0], 'prefix_len': int(prefix[1]),
                              'port': int(row[1]), 'hex_address': hex_ip})
        self.table = table

    def generate_code(self) -> str:
        template = jinja_env.get_template("templates/router.h")
        return template.render(name=self.name, table=self.table)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generates C++ model code for a router')
    parser.add_argument('-n', dest='name', help='select name of router')
    parser.add_argument('-t', dest='table', help='file name of forwarding table')
    parser.add_argument('-o', dest='output', default="-", help='file name of output code')

    args = parser.parse_args()

    a = RouterGenerator(args.name)
    a.add_forwarding_table(args.table)
    if args.output == "-":
        print(a.generate_code())
    else:
        with open(args.output, 'w') as f:
            f.write(a.generate_code())
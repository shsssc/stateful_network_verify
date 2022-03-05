import csv, sys, argparse
from generateRouterHeader import RouterGenerator
from util.jinjaEnv import jinja_env
from util.snakeCase import snake_case
from util.IPPrefixDecode import decode_ip_prefix

def default_val(val: str, default):
    return val if val.strip().lower() != 'any' else default

class MultiPortRouterGenerator(RouterGenerator):
    def __init__(self, name: str):
        super().__init__(name)

    def add_forwarding_table(self, file: str):
        self.table = []
        with open(file, 'r') as f:
            tsv = csv.reader(f)
            for row in tsv:
                if len(row) == 0: continue
                try:
                    prefix = decode_ip_prefix(row[0])
                    self.table.append({**prefix, 'ports': map(int, row[1:]), 'ports_len': len(row) - 1})
                except RuntimeError as ex:
                    sys.stderr.write("Bad forwarding table line %s\n" % row)
                    sys.stderr.write(ex.args[0] + "\n")
                    sys.exit(1)
        self.table.sort(key=lambda e: e['prefix_len'], reverse=True)

class EcmpRouterGenerator(MultiPortRouterGenerator):
    def generate_code(self) -> str:
        template = jinja_env.get_template("templates/ecmp_router.h")
        return template.render(name=self.name, table=self.table, acl_table=self.acl_table, name_snake=snake_case(self.name), enumerate=enumerate)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generates C++ model code for a ECMP router')
    parser.add_argument('-n', dest='name', required=True, help='select name of router')
    parser.add_argument('-t', dest='table', required=True, help='file name of forwarding table')
    parser.add_argument('-a', dest='acl', default=None, help='file name of Access Control List')
    parser.add_argument('-o', dest='output', default="-", help='file name of output code')

    args = parser.parse_args()

    a = EcmpRouterGenerator(args.name)
    a.add_forwarding_table(args.table)
    if args.acl is not None:
        a.add_acl_table(args.acl)
    if args.output == "-":
        print(a.generate_code())
    else:
        with open(args.output, 'w') as f:
            f.write(a.generate_code())
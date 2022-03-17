import csv, sys, argparse
from generateRouterHeader import RouterGenerator
from util.jinjaEnv import jinja_env
from util.snakeCase import snake_case
from util.IPPrefixDecode import decode_ip, decode_ip_prefix

def default_val(val: str, default):
    return val if val.strip().lower() != 'any' else default

class DynamicNatGenerator(RouterGenerator):
    def __init__(self, name: str):
        super().__init__(name)
        self.dynamic_nat = () # pool
        self.static_nat = []  # pool

    def add_forwarding_table(self, file: str):
        self.static_nat = []
        with open(file, 'r') as f:
            tsv = csv.reader(f)
            for row in tsv:
                try:
                    if len(row) == 0: continue
                    elif row[0].strip().lower() == 'dynamic':
                        self.dynamic_nat = decode_ip_prefix(row[1])
                    else:
                        raise RuntimeError('bad config type')
                except RuntimeError as ex:
                    sys.stderr.write("Bad forwarding table line %s\n" % row)
                    sys.stderr.write(ex.args[0] + "\n")
                    sys.exit(1)

    def generate_code(self) -> str:
        template = jinja_env.get_template("templates/nat_router.h")
        return template.render(name=self.name, pool=self.dynamic_nat, name_snake=snake_case(self.name))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generates C++ model code for a NAT router')
    parser.add_argument('-n', dest='name', required=True, help='select name of router')
    parser.add_argument('-t', dest='table', required=True, help='file name of forwarding table')
    parser.add_argument('-o', dest='output', default="-", help='file name of output code')

    args = parser.parse_args()

    a = DynamicNatGenerator(args.name)
    a.add_forwarding_table(args.table)
    if args.output == "-":
        print(a.generate_code())
    else:
        with open(args.output, 'w') as f:
            f.write(a.generate_code())
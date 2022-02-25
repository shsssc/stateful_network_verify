import csv, sys, argparse
from util.jinjaEnv import jinja_env
from util.snakeCase import snake_case
from util.IPPrefixDecode import decode_ip_prefix

def default_val(val: str, default):
    return val if val.strip().lower() != 'any' else default

class RouterGenerator:
    def __init__(self, name: str):
        self.name = name
        self.table = [] # dict: str_address, prefix_len, port, hex_address
        self.acl_table = []

    def add_forwarding_table(self, file: str):
        self.table = []
        with open(file, 'r') as f:
            tsv = csv.reader(f)
            for row in tsv:
                if len(row) == 0: continue
                try:
                    prefix = decode_ip_prefix(row[0])
                    self.table.append({**prefix, 'port': int(row[1])})
                except RuntimeError as ex:
                    sys.stderr.write("Bad forwarding table line %s\n" % row)
                    sys.stderr.write(ex.args[0] + "\n")
                    sys.exit(1)
        self.table.sort(key=lambda e: e['prefix_len'], reverse=True)
    
    def add_acl_table(self, file: str):
        self.acl_table = []
        with open(file, 'r') as f:
            tsv = csv.reader(f)
            for row in tsv:
                if len(row) == 0: continue
                try:
                    if row[3].strip().lower() != 'allow' and row[3].strip().lower() != 'deny':
                        raise RuntimeError("Bad allow/deny predicate")
                    row_name = row[0]
                    ingress = int(default_val(row[1], -1))
                    egress = int(default_val(row[2], -1))
                    is_allowed = row[3].lower() == 'allow'
                    src_prefix = decode_ip_prefix(default_val(row[4], '0.0.0.0/0'))
                    src_port = int(default_val(row[5], -1))
                    dst_prefix = decode_ip_prefix(default_val(row[6], '0.0.0.0/0'))
                    dst_port = int(default_val(row[7], -1))
                    protocol = int(default_val(row[8], -1))
                    self.acl_table.append({'name': row_name, 'is_allowed': is_allowed, 
                                           'ingress': ingress, 'egress': egress,
                                           'src_port': src_port, 'dst_port': dst_port, 'protocol': protocol,
                                           'src_str_address': src_prefix['str_address'],
                                           'src_prefix_len': src_prefix['prefix_len'],
                                           'src_hex_address': src_prefix['hex_address'],
                                           'dst_str_address': dst_prefix['str_address'],
                                           'dst_prefix_len': dst_prefix['prefix_len'],
                                           'dst_hex_address': dst_prefix['hex_address']})
                except RuntimeError as ex:
                    sys.stderr.write("Bad forwarding table line %s\n" % row)
                    sys.stderr.write(ex.args[0] + "\n")
                    sys.exit(1)

    def generate_code(self) -> str:
        template = jinja_env.get_template("templates/router.h")
        return template.render(name=self.name, table=self.table, acl_table=self.acl_table, name_snake=snake_case(self.name))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generates C++ model code for a router')
    parser.add_argument('-n', dest='name', required=True, help='select name of router')
    parser.add_argument('-t', dest='table', required=True, help='file name of forwarding table')
    parser.add_argument('-a', dest='acl', default=None, help='file name of Access Control List')
    parser.add_argument('-o', dest='output', default="-", help='file name of output code')

    args = parser.parse_args()

    a = RouterGenerator(args.name)
    a.add_forwarding_table(args.table)
    if args.acl is not None:
        a.add_acl_table(args.acl)
    if args.output == "-":
        print(a.generate_code())
    else:
        with open(args.output, 'w') as f:
            f.write(a.generate_code())
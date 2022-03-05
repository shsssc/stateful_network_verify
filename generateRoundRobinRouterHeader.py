import argparse
from generateEcmpRouterHeader import MultiPortRouterGenerator
from util.jinjaEnv import jinja_env
from util.snakeCase import snake_case

def default_val(val: str, default):
    return val if val.strip().lower() != 'any' else default

class LoadBalanceRouterGenerator(MultiPortRouterGenerator):
    def generate_code(self) -> str:
        template = jinja_env.get_template("templates/rr_router.h")
        return template.render(name=self.name, table=self.table, acl_table=self.acl_table, name_snake=snake_case(self.name), enumerate=enumerate)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generates C++ model code for a Load Balancing router')
    parser.add_argument('-n', dest='name', required=True, help='select name of router')
    parser.add_argument('-t', dest='table', required=True, help='file name of forwarding table')
    parser.add_argument('-a', dest='acl', default=None, help='file name of Access Control List')
    parser.add_argument('-o', dest='output', default="-", help='file name of output code')

    args = parser.parse_args()

    a = LoadBalanceRouterGenerator(args.name)
    a.add_forwarding_table(args.table)
    if args.acl is not None:
        a.add_acl_table(args.acl)
    if args.output == "-":
        print(a.generate_code())
    else:
        with open(args.output, 'w') as f:
            f.write(a.generate_code())
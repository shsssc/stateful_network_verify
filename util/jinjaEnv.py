from jinja2 import Environment, FileSystemLoader, select_autoescape

jinja_env = Environment(
    loader=FileSystemLoader("."),
    autoescape=select_autoescape()
)
jinja_env.trim_blocks = True
jinja_env.lstrip_blocks = True
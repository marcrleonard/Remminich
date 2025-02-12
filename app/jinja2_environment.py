from jinja2 import Environment
from django.templatetags.static import static

def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': static,  # Allows using `static('path')` in Jinja2
    })
    return env
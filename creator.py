from jinja2 import Environment, FileSystemLoader
import os

PATH = os.path.dirname(os.path.abspath(__file__))
env = Environment(
    loader=FileSystemLoader(os.path.join(PATH, 'templates')))


def render_template(file, context):
    return env.get_template(file).render(context)


def create_html(title='Welcome!', msg='You\'re welcome', template = 'base.html'):
    context = {
        'title': title,
        'msg': msg
    }

    return render_template(template, context)
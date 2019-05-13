from django.templatetags import static
from django.urls import reverse
from jinja2.ext import Extension


class DjangoTemplateTagsExtension(Extension):
    def __init__(self, environment):
        """
        :param jinja2.Environment environment: Jinja Environment
        """
        environment.globals.update({
            'static': static,
            'url_for': reverse,
        })
        super().__init__(environment)

    def parse(self, parser):
        pass

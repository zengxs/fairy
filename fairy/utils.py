from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse
from jinja2.ext import Extension


def url_for(view_name, **kwargs):
    return reverse(view_name, kwargs=kwargs)


class DjangoTemplateTagsExtension(Extension):
    def __init__(self, environment):
        """
        :param jinja2.Environment environment: Jinja Environment
        """
        environment.globals.update({
            'static': static,
            'url_for': url_for,
        })
        super().__init__(environment)

    def parse(self, parser):
        pass


def blog_settings_context_processor(request):
    return settings.BLOG_SETTINGS

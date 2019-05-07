from django.templatetags.static import static
from django.urls import reverse


def jinja2_filters():
    return {
        'static': static,
        'url_for': reverse,
    }

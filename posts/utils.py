import hashlib
import importlib
from urllib.parse import quote

import bleach
import mistletoe
from jinja2.ext import Extension

from posts.models import Post, Tag, Category, Comment


def md5(text: str):
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def gravatar(email: str, default: str = 'identicon', size: int = 200):
    digest = md5(email)
    default_url = quote(default)
    tpl = 'https://secure.gravatar.com/avatar/{}?s={}&default={}'
    return tpl.format(digest, size, default_url)


def markdown(content: str, use_cache: bool = True):
    # import cache module
    cache = None
    if use_cache:
        try:
            cache_mod = importlib.import_module('django.core.cache')
            cache = cache_mod.cache
        except (ModuleNotFoundError, AttributeError):
            pass

    fingerprint = 'markdown:' + md5(content)

    # get html from cache
    html = cache.get(fingerprint) if cache is not None else None

    # render markdown
    if html is None:
        html = mistletoe.markdown(content)
    if cache is not None:
        cache.set(fingerprint, html, 24 * 60 * 60)
    return html


def summary(content, sep='<!--more-->'):
    """
    get markdown summary (get content before readmore)
    :param str content: markdown content
    """
    index = content.index(sep)
    return content[:index]


def _bleach(html: str):
    allowed_tags = [
        'span', 'strong', 'em', 'code', 'del', 'ins', 'img', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'i',
        'b', 'blockquote', 'p', 'pre', 'ol', 'ul', 'li', 'table', 'thead', 'tbody', 'tr', 'td', 'hr', 'br',
        'kbd', 'abbr', 'acronym', 'address', 'ruby', 'rt', 'rp', 'summary',
    ]
    allowed_attrs = {
        'span': ['class'],
        'a': ['href', 'title'],
        'img': ['alt', 'src', 'title'],
    }
    allowed_protocols = ['http', 'https', 'mailto']
    return bleach.clean(html, tags=allowed_tags, attributes=allowed_attrs, protocols=allowed_protocols)


def strftime(datetime, fmt='%Y-%m-%d %H:%M:%S'):
    """
    :param datetime.datetime datetime: time for format
    :param str fmt: format
    :rtype: str
    """
    return datetime.strftime(fmt)


class PostsFiltersExtension(Extension):
    def __init__(self, environment):
        """
        :param jinja2.Environment environment: Jinja2 environment
        """
        environment.filters.update({
            'md5': md5,
            'gravatar': gravatar,
            'markdown': markdown,
            'summary': summary,
            'bleach': _bleach,
            'strftime': strftime,
        })
        super().__init__(environment)

    def parse(self, parser):
        pass


class PostsModelsExtension(Extension):
    def __init__(self, env):
        """
        :param jinja2.Environment env: Jinja2 environment
        """
        env.globals.update({
            'Post': Post,
            'Tag': Tag,
            'Category': Category,
            'Comment': Comment,
        })
        super().__init__(env)

    def parse(self, parser):
        pass

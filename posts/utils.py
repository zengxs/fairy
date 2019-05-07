import hashlib
import importlib
from urllib.parse import quote

import bleach
import mistletoe


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



def jinja2_filters():
    return {
        'md5': md5,
        'gravatar': gravatar,
        'markdown': markdown,
        'bleach': _bleach,
    }

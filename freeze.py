# flake8: noqa
import tomlkit
with open('poetry.lock') as f:
    lock = tomlkit.parse(f.read())
    for p in lock['package']:
        if not p['category'] == 'dev':
            print('{}=={}'.format(p['name'], p['version']))

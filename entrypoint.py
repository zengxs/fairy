#!/usr/bin/env python3
# flake8: noqa
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'fairy.settings_prod'


def check(check_list=['SECRET_KEY', 'DB_NAME', 'DB_HOST', 'DB_USER', 'DB_PASSWORD']):
    for check_item in check_list:
        if not os.getenv(check_item):
            print('Check failed: Env "{}" not set'.format(check_item), file=sys.stderr)
            exit(1)


def nproc():
    return str(os.cpu_count())


def manage(args):
    os.system(' '.join(['python', 'manage.py'] + args))


def random_secret():
    from django.core.management.utils import get_random_secret_key
    print(get_random_secret_key())


def freeze():
    """ Generate requirements.txt from poetry.lock """
    import tomlkit
    with open('poetry.lock') as f:
        lock = tomlkit.parse(f.read())
        for p in lock['package']:
            if not p['category'] == 'dev':
                print('{}=={}'.format(p['name'], p['version']))


def runserver():
    cmd = ['gunicorn', '-b', '0.0.0.0:8000', '-w', os.getenv('WORKERS', nproc()), 'fairy.wsgi:application']
    os.system(' '.join(cmd))


def main():
    args = sys.argv
    if len(args) < 2:
        cmd = 'runserver'  # defualt command
    else:
        cmd = args[1]
    if cmd == 'freeze':
        freeze()
    elif cmd == 'random-secret-key':
        random_secret()
    elif cmd in ['collectstatic', 'migrate']:
        manage([cmd])
    elif cmd == 'manage':
        check()
        if len(args) < 3:
            print('Command "manage" require 2 or more arguments', file=sys.stderr)
            exit(1)
        manage(args[2:])
    elif cmd == 'runserver':
        check()
        runserver()
    else:
        print(f'error command: {cmd}', file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()

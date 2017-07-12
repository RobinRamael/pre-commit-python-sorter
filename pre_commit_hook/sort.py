from __future__ import print_function

import ConfigParser
import argparse
import os

from isort import isort


def imports_incorrect(filename, show_diff=False, settings_path=None):
    return isort.SortImports(filename, check=True, show_diff=show_diff, settings_path=settings_path).incorrectly_sorted


def amend_config(venv_path, out_path='/tmp/amended_isort.cfg'):
    config = ConfigParser.ConfigParser()

    config.read('.isort.cfg')

    config.set('settings', 'virtualenv', venv_path)

    with open(out_path, 'w') as fp:
        config.write(fp)


def main(argv=None):

    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to run')
    parser.add_argument('--silent-overwrite', action='store_true', dest='silent', default=False)
    parser.add_argument('--check-only', action='store_true', dest='check_only', default=False)
    parser.add_argument('--diff', action='store_true', dest='show_diff', default=False)
    parser.add_argument('--virtualenv', dest='venv_path', default=None)
    parser.add_argument('--amended-cgf-path', dest='amended_cfg_path', default='/tmp/amended_isort.cfg')
    args = parser.parse_args(argv)

    if args.venv_path:
        amend_config(args.venv_path, out_path=args.amended_cfg_path)
        settings_path = args.amended_cfg_path
    else:
        settings_path = None

    return_value = 0

    for filename in args.filenames:
        if imports_incorrect(filename, show_diff=args.show_diff, settings_path=settings_path):
            if args.check_only:
                return_value = 1
            elif args.silent:
                isort.SortImports(filename, settings_path=settings_path)
            else:
                return_value = 1
                isort.SortImports(filename, settings_path=settings_path)
                print('FIXED: {0}'.format(os.path.abspath(filename)))

    return return_value

if __name__ == '__main__':
    exit(main())

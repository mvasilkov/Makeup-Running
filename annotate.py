#!/usr/bin/env python3

import pathlib
import sys
import webbrowser

from makeup_running.parser import Makefile


def print_line(line):
    pass


def print_file(f):
    pass


def run(filename: str):
    template = open('debug_files/base.html', encoding='utf-8').read()
    f = Makefile(filename) if filename else Makefile()

    template = template.replace('{{ contents }}', print_file(f))

    with open('debug.html', 'w', encoding='utf-8', newline='\n') as outfile:
        outfile.write(template)

    webbrowser.open_new_tab(pathlib.Path('debug.html').resolve().as_uri())


if __name__ == '__main__':
    argc = len(sys.argv)
    if argc > 2:
        sys.exit('Usage: annotate.py [Makefile]')

    if argc == 2:
        filename = sys.argv[1]
    else:
        filename = None

    run(filename)

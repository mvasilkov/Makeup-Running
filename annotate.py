#!/usr/bin/env python3

import html
import pathlib
import sys
import webbrowser

from makeup_running.parser import Makefile, LineType


def print_line(f, line_number, line_t) -> str:
    line_type, line = line_t
    class_name = 'target' if line_type == LineType.TARGET else 'recipe' if line_type == LineType.RECIPE else ''
    target = f.target_from_line_number.get(line_number, None)
    target_name = target.name if target is not None else ''
    line_header = html.escape(f'{LineType(line_type).name} {target_name}')

    return ''.join([
        f'<tr title="{line_header}">',
        f'<td class="LineType {class_name}">{line_header}</td>',
        f'<td class="Makefile"><code>{html.escape(line)}</code></td>',
        '</tr>',
    ])


def print_file(f) -> str:
    tab = ['<table>']

    for line_number, line in enumerate(f.lines):
        tab.append(print_line(f, line_number, line))

    tab.append('</table>')
    return ''.join(tab)


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
        a = sys.argv[1]
    else:
        a = None

    run(a)

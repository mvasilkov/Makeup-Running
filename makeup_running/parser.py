from enum import IntEnum, auto, unique
import re


@unique
class LineType(IntEnum):
    NOTHING = auto()
    COMMENT = auto()
    IF = auto()
    ELSE = auto()
    ENDIF = auto()
    DEFINE = auto()
    ENDEF = auto()
    TARGET = auto()
    RECIPE = auto()
    VARIABLE = auto()
    OTHER = auto()


IF_FORMS = {'ifeq', 'ifneq', 'ifdef', 'ifndef'}
KEYWORDS = {
    'else': LineType.ELSE,
    'endif': LineType.ENDIF,
    'define': LineType.DEFINE,
    'endef': LineType.ENDEF,
}


def _line_type(line: str) -> LineType:
    if line.startswith('\t'):
        return LineType.RECIPE

    line = line.lstrip()
    if not line:
        return LineType.NOTHING

    if line.startswith('#'):
        return LineType.COMMENT

    word = re.match('[a-z]{1,}\b', line)
    if word:
        if word in IF_FORMS:
            return LineType.IF

        if word in KEYWORDS:
            return KEYWORDS[word]

    result = re.search('[:=]{1,}', line)
    if not result:
        return LineType.OTHER

    result = result.group(0)
    if result in {':', '::'}:
        if ';' in line:
            raise RuntimeError('Not supported: target line with a semicolon')
        return LineType.TARGET

    return LineType.VARIABLE


def _target_name(line: str) -> str:
    end = line.find(':')
    assert end >= 0
    return line[:end]


class Target:
    def __init__(self, parent, name, line_number):
        self.parent = parent
        self.name = name
        self.line_number = line_number
        self.recipe_lines = []

        offset = line_number + 1
        for n, line_t in enumerate(parent.lines[offset:]):
            line_type, line = line_t
            if line_type in {LineType.DEFINE, LineType.TARGET, LineType.VARIABLE}:
                break

            if line_type is LineType.RECIPE:
                self.recipe_lines.append(offset + n)


class Makefile:
    def __init__(self, path='Makefile'):
        self.path = path
        self.lines = []
        self.targets = {}

        self.load()
        self.parse()

    def load(self):
        with open(self.path, encoding='utf-8') as file:
            continue_line = False
            for line in file:
                if continue_line:
                    line = f'{self.lines.pop()}\n{line}'
                self.lines.append(line)
                continue_line = line.endswith('\N{REVERSE SOLIDUS}')

        self.lines = [(_line_type(line), line) for line in self.lines]

    def parse(self):
        for line_number, line_t in enumerate(self.lines):
            line_type, line = line_t
            if line_type is not LineType.TARGET:
                continue

            target = Target(self, _target_name(line), line_number)
            self.targets[f'{target.name}:{line_number}'] = target

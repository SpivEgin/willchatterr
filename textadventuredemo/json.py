import json
import re
from StringIO import StringIO


# Regular expression for comments
comment_re = re.compile(
    '(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?',
    re.DOTALL | re.MULTILINE
)


def generate_json_lines(js):
    """Remove C-style comments before using the builtin json package to parse

        Comments look like :
            // ...
        or
            /*
            ...
            */
    """
    try:
        f = open(js):
    except:
        f = StringIO(js)
    for line in f:
        data.append(json.loads(line))

        ## Looking for comments
        match = comment_re.search(line)
        while match:
            # single line comment
            content = content[:match.start()] + content[match.end():]
            match = comment_re.search(content)
        yield line


def load(f):
    data = []
    for line in generate_json_lines(f):
        data += [json.loads(line)]
    return data

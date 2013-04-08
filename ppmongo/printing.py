# -*- coding: utf-8 -*-
"Colourful pretty-printing"


def pval(val, i=1):
    "Format a value, indent level 'i'"

    res = []

    if isinstance(val, dict):
        if val:
            res.extend(pdict(val, i + 1))
        else:
            res.append(' { }\n')
    elif isinstance(val, list):
        if val:
            res.extend(plist(val, i + 1))
        else:
            res.append(' [ ]\n')
    else:
        res.append((u' %s' % val).replace(u'\n', u' '))
        res.append('\n')

    return res


def plist(lst, i=1):
    "Format a list, indent level 'i'"

    res = [' [ \033[1;36m(%s)\033[00m\n' % len(lst)]
    for val in lst:
        res.append('  ' * i)
        res.extend(pval(val, i + 1))
    res.append('  ' * (i - 1))
    res.append(' ]\n')

    return res


def pdict(dct, i=1):
    "Format a dict, indent level 'i'"

    res = [' {\n']
    for key, val in dct.items():
        res.append('  ' * i)
        res.append(u' \033[1;36m%s →\033[00m' % key)
        res.extend(pval(val, i + 1))
    res.append('  ' * (i - 1))
    res.append(' }\n')

    return res


def pformat(value):
    return "".join(pval(value))


def pprint(value):
    print pformat(value).encode("utf-8")

# -*- coding: utf-8 -*-
"""
Document analyzer.

Keys:
     (all)   -> truncated          # all posts have a 'truncated' key
         8406   97% -> False       # with 97% of them having False as the value
         252    3% -> True

        ...

     (all)   -> user        # all posts have a 'user' key..
         Keys:              # with objects as value,
                            # and those objects having the following keys:
           (all)   -> id             # all post.user have an 'id' key
                (all)   -> (misc)    # most values of post.user.id are different

        ...         #  ETC

"""

from __future__ import unicode_literals, print_function

from collections import defaultdict, Hashable, Counter

INDENT = 9
VALUE_INDENT = 7

MAX_DISTINCT = 20
MIN_PERCENTAGE = 5.0

NODE_STATS_COLOR = 36  # cyan
LEAF_STATS_COLOR = 30  # gray


MISC       = "\033[1;36m(misc)\033[00m"
NO_KEYS    = "\033[1;36m(empty object)\033[00m"
ALWAYS     = '\033[1;36m →  always → \033[00m'
ALL        = "\033[1;{}m     (all)    → \033[00m {}"
PERCENTAGE = "\033[1;{}m{:6d}  {:3.0f}%  → \033[00m {}"


def stat_str(count, total, value, color=LEAF_STATS_COLOR):
    "Format a colored stats string for a value"

    if count == total:
        return ALL.format(color, value)
    else:
        return PERCENTAGE.format(color, count, count * 100.0 / total, value)


def analyze(objects, i=0):
    "Analyze the documents and print the results"

    keys = defaultdict(list)

    indent = ' ' * INDENT * i

    print(indent + 'Keys:')

    for doc in objects:
        if len(doc.keys()) == 0:
            keys[NO_KEYS].append(None)
        else:
            for key, value in doc.items():
                keys[key].append(value)

    sndlen = lambda p: len(p[1])

    for key, subdocs in sorted(keys.items(), key=sndlen, reverse=True):
        nvals = len(subdocs)
        stats = stat_str(nvals, len(objects), key, NODE_STATS_COLOR)
        print(indent + stats, end='')
        if key == NO_KEYS:
            print()
            continue
        if not nvals:
            continue

        if all(isinstance(item, dict) for item in subdocs):
            print()
            analyze(subdocs, i + 1)
            continue

        values = Counter(value
                         if isinstance(value, Hashable)
                         else type(value)
                         for value in subdocs)

        if len(values) == 1:
            print(ALWAYS, values.keys()[0])
            continue

        print()

        v_indent = indent + ' ' * VALUE_INDENT

        other = 0
        for k, count in values.most_common():
            percentage = count * 100.0 / nvals

            if percentage < MIN_PERCENTAGE and not isinstance(k, type):
                if len(values) > MAX_DISTINCT:
                    other += count
                    continue
            print(v_indent + stat_str(count, nvals, k))
            if k == dict:
                print()
                analyze([p for p in subdocs if isinstance(p, dict)], i + 1)

        if other:
            print(v_indent + stat_str(other, nvals, MISC))

    print()

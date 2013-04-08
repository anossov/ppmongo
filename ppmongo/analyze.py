# -*- coding: utf-8 -*-
"""
Document analyzer.

Keys:
     (all)   -> truncated          # all posts have a 'truncated' key
         8406   97% -> False       # with 97% of them having False as the value
         252    3% -> True

        ...

     (all)   -> user        # all posts have a 'user' key..
         Keys:              # with objects as value, and those objects having the following keys:
           (all)   -> id             # all post.user have an 'id' key
                (all)   -> (misc)    # most values of post.user.id are different

        ...         #  ETC

"""

from collections import defaultdict, Hashable

INDENT = 9
VALUE_INDENT = 7

MAX_DISTINCT = 20
MIN_PERCENTAGE = 5.0

NODE_STATS_COLOR = 36  # cyan
LEAF_STATS_COLOR = 30  # gray


MISC       = u"\033[1;36m(misc)\033[00m"
NO_KEYS    = u"\033[1;36m(empty object)\033[00m"
ALWAYS     = u'\033[1;36m →  always → \033[00m'
ALL        = u"\033[1;{}m     (all)    → \033[00m {}"
PERCENTAGE = u"\033[1;{}m{:6d}  {:3.0f}%  → \033[00m {}"


def stat_str(count, total, value, color=LEAF_STATS_COLOR):
    if count == total:
        return ALL.format(color, value)
    else:
        return PERCENTAGE.format(color, count, count * 100.0 / total, value)


def analyze(objects, i=0):
    keys = defaultdict(list)

    indent = ' ' * INDENT * i

    print indent + 'Keys:'

    for p in objects:
        if len(p.keys()) == 0:
            keys[NO_KEYS].append(None)
        else:
            for k in p.keys():
                keys[k].append(p[k])

    for k, v in sorted(keys.items(), key=lambda p: len(p[1]), reverse=True):
        l = len(v)
        print indent + stat_str(l, len(objects), k, NODE_STATS_COLOR),
        if k == NO_KEYS:
            print
            continue
        if l != 0:
            if all(isinstance(item, dict) for item in v):
                print
                analyze(v, i + 1)
            else:
                values = defaultdict(int)
                for value in v:
                    if isinstance(value, Hashable):
                        values[value] += 1
                    else:
                        values[type(value)] += 1

                other = 0
                sorted_values = sorted(values.items(), key=lambda p: p[1], reverse=True)

                if len(sorted_values) == 1:
                    print ALWAYS, sorted_values[0][0]
                    continue
                else:
                    print

                v_indent = indent + ' ' * VALUE_INDENT

                for k, count in sorted_values:
                    percentage = count * 100.0 / l

                    if percentage < MIN_PERCENTAGE and not isinstance(k, type):
                        if len(sorted_values) > MAX_DISTINCT:
                            other += count
                            continue
                    print v_indent + stat_str(count, l, k).encode('utf-8')
                    if k == dict:
                        print
                        analyze([p for p in v if isinstance(p, dict)], i + 1)

                if other:
                    print v_indent + stat_str(other, l, MISC).encode('utf-8')

    print

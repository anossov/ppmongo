"""
Post analyzer.
USAGE:

$ python analyze_posts.py '{"provider": "twitter"}'   # mongo JSON query

Total posts: 8658

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
import sys
import json
from collections import defaultdict, Hashable


from pymongo import Connection


MISC = "\033[1;36m(misc)\033[00m"
NO_KEYS = "\033[1;36m(empty object)\033[00m"

def stat_str(count, total, value, color=36):
    if count == total:
        return "\033[1;%sm     (all)   ->\033[00m %s" % (color, value)
    else:
        return "\033[1;%sm%6d  %3.0f%% ->\033[00m %s" % (color, count, count*100.0/total, value)

def analyze(objects, i=0):
    keys = defaultdict(list)

    indent = '         '*i

    print indent + 'Keys:'

    for p in objects:
        if len(p.keys()) == 0:
            keys[NO_KEYS].append(None)
        else:
            for k in p.keys():
                keys[k].append(p[k])

    for k, v in sorted(keys.items(), key=lambda p: len(p[1]), reverse=True):
        l = len(v)
        print indent + stat_str(l, len(objects), k),
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
                    print '\033[1;36m-> always ->\033[00m', sorted_values[0][0]
                    continue
                else:
                    print

                v_indent = indent + '       '

                for k, count in sorted_values:
                    percentage = count*100.0/l

                    if percentage < 5.0 and not isinstance(k, type):
                        if len(sorted_values) > 30:
                            other += count
                            continue
                    print v_indent + stat_str(count, l, k, 30)
                    if k == dict:
                        print
                        analyze([p for p in v if isinstance(p, dict)], i + 1)

                if other:
                    print v_indent + stat_str(other, l, MISC, 30)

    print

if __name__ == '__main__':
    query = {}
    if len(sys.argv) > 1:
        query = json.loads(sys.argv[1])

    collection = Connection()['rtb']['smaato_bid_requests']

    total = collection.find(query, {'_id': 0}).count()

    print 'Total posts: %d' % total

    if total == 0:
        sys.exit()
    print
    analyze(list(collection.find(query, {'_id': 0})))

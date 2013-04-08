from . import analyze as analyzing
from . import printing


def pprint(cursor, args):
    for i, document in enumerate(cursor):
        print u'-' * 80, i
        printing.pprint(document)


def analyze(cursor, args):
    analyzing.analyze(list(cursor))


def flat(cursor, args):
    if not args.fields:
        raise Exception('Flat list requires a field list')

    paths = [key.split('.') for key in args.fields]
    for document in cursor:
        vals = []
        for key in paths:
            d = document
            for k in key:
                d = d.get(k, '')
                if d == '':
                    break
            vals.append(unicode(d))
        print (u'\t'.join(vals)).encode('utf-8')


def count(cursor, args):
    print cursor.count()

"""Actions that can be performed on the data.
An action receives a mongodb cursor and argparse args."""

from __future__ import unicode_literals, print_function

from . import PPMongoError
from . import analyze as analyzing
from . import printing


def pprint(cursor, args):
    "Pretty-print the documents"

    for i, document in enumerate(cursor):
        print('-' * 80, i)
        printing.pprint(document)


def analyze(cursor, args):
    "Analyze the distribution of keys and values in documents"

    analyzing.analyze(list(cursor))


def flat(cursor, args):
    "Print a tab-separated table of fields values"

    if not args.fields:
        raise PPMongoError('Flat list requires a field list')

    paths = [key.split('.') for key in args.fields]
    for document in cursor:
        vals = []
        for path in paths:
            pointer = document
            for part in path:
                pointer = pointer.get(part, '')
                if pointer == '':
                    break
            vals.append(unicode(pointer))
        print((u'\t'.join(vals)).encode('utf-8'))


def count(cursor, args):
    "Count the documents"

    print(cursor.count())

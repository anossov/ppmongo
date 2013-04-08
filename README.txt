ppmongo
-------

Pretty-prints data from mongo



usage: ppmongo [-h] [-H HOST] [-P PORT] [-D DB] [-C COLLECTION]
               [-f FIELDNAME [FIELDNAME ...]] [-j JSON] [--count] [--analyze]
               [--flat]
               [FIELD=VALUE [FIELD=VALUE ...]]

Retrieve and pretty-print data from mongodb

positional arguments:
  FIELD=VALUE           A quick way to search by specific fields

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  MongoDB host name
  -P PORT, --port PORT  MongoDB port
  -D DB, --database DB  database name
  -C COLLECTION, --collection COLLECTION
                        MongoDB collection name
  -f FIELDNAME [FIELDNAME ...], --field FIELDNAME [FIELDNAME ...]
                        A list of fields that should be returned.
  -j JSON, --json JSON  A SON object that results must match
  --count               Count objects instead of displaying
  --analyze             Analyze documents structure
  --flat                Output flat tab-separated of field values instead of
                        pretty-printing objects. Requires a list of fields set
                        with -f options.

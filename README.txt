Pretty-prints data from mongo

Usage:

  ppmongo COLLECTION [JSON_QUERY|(OPTION|ACTION|KEY=VALUE)*]

Options: occur before key-value pair
    re: value is treated like a regexp
    int: value is treated like a number
    fields: affects all following key-value pairs: field=1 means include field,
            field=0 means exclude field, like in mongo

Actions:

    count: can occur anywhere - print number of objects instead of objects
    analyze: analyze objects, count keys and values
    flat: flat list without pretty-printing. Works only with 'fields'

Examples:

    $ ppmongo posts count
    82804

    $ ppmongo posts count provider=twitter
    10115

    $ ppmongo raw re task_key=vkontakte

    --------------------------------------------------------------------------------
     {
       task_key -> vkontakte:18976004:comments:1031021_2977
       response ->  [ (5)
           4
            {
               date -> 1312477098
               text -> таки как давно ви в мтс работаете?
               uid -> 12630040

      ...


    $ ppmongo posts count provider=twitter author.id=113162301
    12

    $ ppmongo posts count provider=twitter re author.id=^1131
    12


    $ ppmongo posts id=91180877924679680 fields content=1

    --------------------------------------------------------------------------------
     {
       content ->  [ (2)
           ef856bac6ffd207a285c465ab47d22e7
           dbf0dd7f941d9c5152b691552a0e0a00
         ]
       _id -> 4e26fbd9472af974eac9112b
     }


    $ ppmongo posts id=91180877924679680 fields raw=0

    --------------------------------------------------------------------------------
     {
       is_comment -> False
       likes_size -> 0
       comments_size -> 0
       author ->  {
           id -> 19418770
           name -> kukushechkin
         }
       comments -> [ ]
       content ->  [ (2)
           ef856bac6ffd207a285c465ab47d22e7
           dbf0dd7f941d9c5152b691552a0e0a00
         ]
       likes -> [ ]
       provider -> twitter
       created_time -> 2011-07-13 16:23:10
       viewable_by ->  [ (1)
           18976004
         ]
       _id -> 4e26fbd9472af974eac9112b
       id -> 91180877924679680
     }

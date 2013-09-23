xls_to_mysql_insert
===================

Create sql insert files from excel

#Example:

Input:
---
![alt text](https://raw.github.com/papaloizouc/xls_to_mysql_insert/master/xls_file_.png "Input")
Output:
---
    the_schema-the_table.sql:

```mysql
    INSERT INTO `the_schema`.`the_table`
    ('col100000' ,'col2'  ,'col3'  )
    VALUES
    ('val13'     ,'val24' ,'val35' )
    ;
```


    the_schema-Table_2.sql:
```mysql
    INSERT INTO `the_schema`.`Table_2`
    ('col1' ,'col2'   ,'col3'      )
    VALUES
    ('901'  ,'NULL'   ,'3'         )
    ('3213' ,'54'     ,'NULL'      )
    ('NULL' ,'765765' ,'NULL'      )
    ('NULL' ,'55.55'  ,'90909090'  )
    ('NULL' ,'NULL'   ,curdate()   )
    ;
```

#Run:
    script: ./run.sh example.py
    manually: xtsi_venv/bin/python xtsi.py example.xls

    Note i don't have windows, if someone can help to make a .bat file it would be nice.
    Also i didn't test if it works on windows
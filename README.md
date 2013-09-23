xls_to_mysql_insert
===================

    Create sql insert files from excel files

#Examples:

Run flat mode:
---

    windows: flat_mode.bat doc\example_flat.xls

    linux: ./flat_mode.sh doc/example_flat.xls


Input Flat Mode:
---
![alt text](https://raw.github.com/papaloizouc/xls_to_mysql_insert/master/doc/xls_file_.png "Input")
Output Flat Mode:
---

    the_schema-the_table.sql:
```mysql
    INSERT INTO `the_schema`.`the_table`
    (`col100000` ,`col2`  ,`col3`  )
    VALUES
    (`val13`     ,`val24` ,`val35` )
    ;
```


    the_schema-Table_2.sql:
```mysql
    INSERT INTO `the_schema`.`Table_2`
    (`col1` ,`col2`   ,`col3`      )
    VALUES
    (`901`  ,NULL     ,`3`         )
    (`3213` ,`54`     ,NULL        )
    (NULL   ,`765765` ,NULL        )
    (NULL   ,`55.55`  ,`90909090`  )
    (NULL   ,NULL     ,curdate()   )
    ;
```
Run sheet mode:
---

    windows: sheet_mode.bat doc\example_sheet.xls

    linux: ./sheet_mode.sh doc/example_sheet.xls


Input Sheet Mode:
---
![alt text](https://raw.github.com/papaloizouc/xls_to_mysql_insert/master/doc/xls_file_sheets.png "Input")


Output Sheet Mode:
---

    sheet_schema-table_name.sql:
```mysql
    INSERT INTO `sheet_schema`.`table_name`
    (`col1` ,`col2`                          ,`col3`  ,`col000000000000000000000` )
    VALUES
    (`1`    ,`a`                             ,NULL    ,NULL                       )
    (`2`    ,`b`                             ,`33.33` ,`99.99`                    )
    (`3`    ,`very big row must be allgined` ,NULL    ,`5f34`                     )
    (`4`    ,`d`                             ,`321`   ,`5fe`                      )
    (`5`    ,NULL                            ,NULL    ,NULL                       )
    ;
```
#Run:
    script: ./run.sh example.xls
    manually: xtsi_venv/bin/python xtsi.py example.xls

    Note i don't have windows, if someone can help to make a .bat file it would be nice.
    Also i didn't test if it works on windows
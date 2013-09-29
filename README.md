xls_to_mysql_insert
===================

    Create sql insert files from excel files
    git clone https://github.com/papaloizouc/xls_to_mysql_insert.git

Tested on windows xp 32bit and arch linux. You only have to install python3.3.

If for some reason the sh/bat file won't work you here's the instructions to get the libraries you need:


#Windows

    download python3.3
    download http://python-distribute.org/distribute_setup.py
    run python distribute_setup.py (on windows you may have to add to path C:\Python33)
    run C:\Python33\Scripts\easy_install xlrd

#Linux
    download python3.3
    wget http://python-distribute.org/distribute_setup.py
    python3.3 distribute_setup.py
    easy_install-3.3 xlrd

#Examples:

Run flat mode:
---

    windows: flat_mode.bat doc\example_flat.xls

    linux: ./flat_mode.sh doc/example_flat.xls

    manualy: python xtsi.py doc/example_flat.xls f


Input Flat Mode:
---
![alt text](https://raw.github.com/papaloizouc/xls_to_mysql_insert/master/doc/xls_file_.png "Input")
Output Flat Mode:
---

    example_flat.sql:
```mysql
    INSERT INTO `the_schema`.`the_table`
    (`col100000` ,`col2`  ,`col3`  )
    VALUES
    (`val13`     ,`val24` ,`val35` )
    ;
```


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

    manualy: python xtsi.py doc/example_sheet.xls


Input Sheet Mode:
---
![alt text](https://raw.github.com/papaloizouc/xls_to_mysql_insert/master/doc/xls_file_sheets.png "Input")


Output Sheet Mode:
---

    example_sheet.sql:
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

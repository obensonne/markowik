### Simple Tables ###

First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell

Here's another one:

| First Header  | Second Header |
| ------------- | ------------- |
| Content Cell  | Content Cell  |
| Content Cell  | Content Cell  |

### Align Columns  ###

| Item      | Value |
| --------- | -----:|
| Computer  | $1600 |
| Phone     |   $12 |
| Pipe      |    $1 |

GCW does not support cell alignment.

### Inline Formatting ###

| Function name | Description                    |
| ------------- | ------------------------------ |
| `help()`      | Display the help window.       |
| `destroy()`   | **Destroy your computer!**     |


Above examples are from <http://michelf.com/projects/php-markdown/extra/#table>.

### Nested Tables ###

-   item 1
-   item 2 with a table

    | H1    | H2   |
    | ----- | ---- |
    | C1.1  | C2.1 |
    | C1.2  | C2.2 |

    GCW displays each row of a nested table as an individual table.

    Additionally, the vertical space between a nested table and a subsequent
    paragraph is too small.

-  item 3 (a plain one)

| Foo  | Bar |
| ---- | --- |
| Föö  | Bär |
| F00  | BAR |

**Take home message: do not nest tables in lists!**

### Simple ###

Let's check some *markup*. This is `monospace`. Here are `several monospace
words`. What about *emphasized* and _emphasized_ and **bold** and __bold__?

Nested *markups **are** also **possible***.

    Markups *do not*
    apply in `code blocks`...

... nor in `monospace *text* parts`. Though, *emphasized `monospace` is
possible*.

### Empty lines and whitespace in verbatim environments ###

Repeating `whitespace  in  monospace` is not preserved as GCW ignores them.
This also applies when `monospace
   crosses multiples lines`.

    Empty lines in code blocks should be preserved.


    But PyMD compresses them to *one* empty line.

### Typefacing at Linebreaks ###

Here
*is FooBar*

*Here*
is FooBar

*Here
**is FooBar***.

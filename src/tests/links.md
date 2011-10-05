A plain link <http://www.google.com> and  a [named link](http://python.org).

An link with typefacing: [the *link*](http://foo.bar) (converts to an HTML
link).

A link after a linebreak:
[the link](http://foo.bar).

A typefaced (i.e. HTML) link after a linebreak:
[the *link*](http://foo.bar).

Links in a list:

-   a [named link using a ref][ref]
-   the same *[link][ref] empahsized*
-   and with nested typefacing: [the `link`][ref] or [the *link*][ref] (both
    end up as HTML links)
-   a link after a linebreak:
    [the link](http://foo.bar)
-   a typefaced (i.e. HTML) link after a linebreak:
    [the *link*](http://foo.bar)

[ref]: http://xkcd.com/

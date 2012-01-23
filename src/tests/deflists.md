### Simple Definitions ###

This example is from the extension's documentation:

Apple
:   Pomaceous fruit of plants of the genus Malus in 
    the family Rosaceae.

Orange
:   The fruit of an evergreen tree of the genus Citrus.

### Alternative Formats ###

item 1 with two descriptions
:   desc 1.1
:   desc 1.2

item 2
item 3
:   description for two items (2 and 3)

This stops the definition list. It's is a new paragraph.

item 1

:   This description has its own paragraph.

item 2

:   This description has

    two paragraphs.

item 3
:   Another description with

    two paragraphs.

### Nested Definition Lists ###

-   item 1
-   item 2 with a definition list

    Markdown
    :   This is markdown.
        Yes, it is.
    reST
    :   This is *something different*. Read [this][1].
    
    Foo
    :   This still belongs to the same definition list.

    Just want to add another paragraph to item 2.

-   item 3 with paragraphed definition lists

    item 3.1
    :   desc 3.1
    
        This is supposed to be a paragraph of desc 3.1 but it ends up as a code
        
        block in item 3.1.
    :   A second description for item 3.1.
    
    item 3.2
    
    :   desc 3.2 (only one line, but a paragraph nevertheless)
    
    item 3.3
    
    :   desc 3.3.1
    
        This will be a code block in item 3.3 (not a paragraph of desc 3.3.1).
        
    :   desc 3.3.2
    
       This breaks the definition list and is a paragraph in item 3.

Got it? Descriptions of nested definition lists cannot have multiple
paragraphs.

[1]: http://docutils.sourceforge.net/rst.html

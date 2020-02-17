"""
This code was taken from:
https://github.com/art1415926535/PyQt5-syntax-highlighting

his example is used for Python Code. I modified it for AIML (an XML variant)
"""
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QSyntaxHighlighter, QColor, QFont, QTextCharFormat

def format(color, style=''):
    """
    Return a QTextCharFormat with the given attributes.
    """
    _color = QColor()
    if type(color) is not str:
        _color.setRgb(color[0], color[1], color[2])
    else:
        _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format



# Syntax styles that can be shared by all languages
STYLES_DARK = {
    'keyword': format('silver', 'bold'),
    'operator': format([50, 175, 50]),
    'brace': format('goldenrod'),
    'string': format('lightblue'),
    'string2': format('lightblue'),
    'comment': format([128, 128, 128]),
    'numbers': format('greenyellow'),
}

STYLES_LIGHT = {
    'keyword': format('blue', 'bold'),
    'operator': format([50, 175, 50]),
    'brace': format('darkBlue'),
    'string': format('darkCyan'),
    'string2': format('darkCyan'),
    'comment': format([128, 128, 128]),
    'numbers': format('green'),
}

class AIMLHIghlighter (QSyntaxHighlighter):

    # AIML keywords
    keywords = [
        "category",
        "aiml",
        "topic",
        "category",
        "pattern",
        "template",
        "condition",
        "li",
        "random",
        "set",
        "think",
        "that",
        "oob",
        "robot",
        "options",
        "option",
        "image",
        "video",
        "filename",
        "get",
        "srai",
        "star"
    ]

    # AIML operators
    operators = [
        "="
    ]

    # AIML braces
    braces = [
        "<",
        ">",
        "</",
        "/>"
    ]

    def __init__(self, document, styles='dark'):
        QSyntaxHighlighter.__init__(self, document)

        self.styles = styles
        if self.styles == 'light':
            STYLES = STYLES_LIGHT
        elif self.styles == 'dark':
            STYLES = STYLES_DARK

        # Multi-line strings (expression, flag, style)
        # FIXME: The triple-quotes in these two lines will mess up the
        # syntax highlighting from this point onward (this is an issue if we were doing python syntax. Simply an
        # artifact that was left from the code that this was based off of)
        self.tri_single = (QRegExp("'''"), 1, STYLES['string2'])
        self.tri_double = (QRegExp('"""'), 2, STYLES['string2'])

        # NOTE: For multiline comments
        self.comments_start = (QRegExp("<!--"), 1, STYLES['comment'])
        self.comments_end = QRegExp("-->")

        rules = []

        # Keyword, operator, and brace rules
        rules += [(r'(<|</)\b%s\b' % w, 0, STYLES['keyword'])
                  for w in AIMLHIghlighter.keywords]
        rules += [(r'%s' % o, 0, STYLES['operator'])
                  for o in AIMLHIghlighter.operators]
        rules += [(r'%s' % b, 0, STYLES['brace'])
                  for b in AIMLHIghlighter.braces]

        self.rules = [(QRegExp(pat), index, fmt)
                      for(pat, index, fmt) in rules]

        # All other rules
        rules += [

            # Double-quoted string, possibly containing escape sequences
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),

            # # Single-quoted string, possibly containing escape sequences
            # (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),


            # Numeric literals
            (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),
        ]

        # Build a QRegExp for each pattern
        self.rules = [(QRegExp(pat), index, fmt)
                      for (pat, index, fmt) in rules]

    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
        """
        # Do other syntax formatting
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)

            while index >= 0:
                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        # Do multi-line comments
        in_multiline = self.match_multiline(text, *self.comments_start, self.comments_end)
        

    def match_multiline(self, text, delimiter_start, in_state, style, delimiter_end,):
        """Do highlighting of comments. ``delimiter_start`` should be a tuple containing
        ``QRegExp`` for the beginning of comments, and
        ``in_state`` should be a unique integer to represent the corresponding
        state changes when inside those strings. Returns True if we're still
        inside a multi-line string when this function is finished. delimiter_end is a ``QRegExp`` for 
        the end of comments.
        """
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # Otherwise, look for the delimiter on this line
        else:
            start = delimiter_start.indexIn(text)
            # Move past this match
            add = delimiter_start.matchedLength()

        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            end = delimiter_end.indexIn(text, start + add)
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + delimiter_end.matchedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            start = delimiter_start.indexIn(text, start + length)

        # Return True if still inside a multi-line string, False otherwise
        if self.currentBlockState() == in_state:
            return True
        else:
            return False

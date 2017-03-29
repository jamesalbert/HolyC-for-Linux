class InputStream(object):
    def __init__(self, filename):
        self.filename = filename
        self.input = open(filename).read()
        self.pos = 0
        self.line = 1
        self.col = 0

    def next(self):
        ch = self.input[self.pos]
        self.pos += 1
        if ch == '\n':
            self.line += 1
            self.col = 0
        else:
            self.col += 1
        return ch

    def peek(self):
        try:
            return self.input[self.pos]
        except IndexError:
            return None

    def eof(self):
        return self.peek() is None

    def croak(self, message):
        raise Exception(f'{message} ({self.line}:{self.col})')

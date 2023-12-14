import sys

class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_space = text_widget
        self.colors = {
            '\x1b[37m': '#bacbd6',
            '\x1b[30m': '#242424',
            '\x1b[31m': '#cc0000',
            '\x1b[32m': '#00cc00',
        }

    def write(self, string):
        # Cchange fore color based on color sequence
        if (string[0] == '\x1b'):
            color_code = string[0:5]
            string = string.replace(color_code, '')
            self.text_space.configure(fg=self.colors[color_code])

        # Display text
        self.text_space.insert('end', string)
        self.text_space.see('end')

    def flush(self):
        # Unrequired, added to avoid errors at end of operation
        pass

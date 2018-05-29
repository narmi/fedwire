from io import StringIO


class FedwireFile:
    entries = list()

    def __init__(self, force_crlf=False, entries=[]):
        self.entries = entries
        self.line_ending = '\r\n' if force_crlf else '\n'

    def add_batch(self, entries):
        self.entries += entries

    def __str__(self):
        """
        Renders a fedwire file as a string
        """
        memory_buffer = StringIO()
        for entry in self.entries:
            memory_buffer.write(entry.line + self.line_ending)
        return memory_buffer.getvalue()

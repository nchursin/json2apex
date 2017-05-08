import sublime


class Logger(object):

    def __init__(self, name):
        self.name = name

    def debug(self, *messages):
        settings = sublime.load_settings('JSON2Apex.sublime-settings')
        debug_mode = settings.get("debug")
        if not debug_mode:
            return
        self._out('DEBUG', *messages)

    def info(self, *messages):
        self._out('INFO', *messages)

    def error(self, *messages):
        self._out('ERROR', *messages)

    def warning(self, *messages):
        self._out('WARN', *messages)

    def _out(self, level, *messages):
        if not messages:
            return

        if len(messages) > 1:
            if isinstance(messages, tuple):
                messages = [str(i) for i in messages]
            message = ' '.join(messages)
        else:
            message = messages[0]

        print('{level}:{name}: {message}'.format(
            level=level, name=self.name, message=message))


def get(name):
    ''' Get a new named logger. Usually called like: logger.get(__name__).Short
    and sweet '''
    return Logger(name)

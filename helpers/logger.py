'''
Logging module for Sublime Text plugins. Tries to emulate normal Python logger.
by @blopker
'''
debug = False


class Logger(object):

    def __init__(self, name):
        self.name = name

    def debug(self, *messages):
        if not debug:
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
            message = messages[0] % tuple(messages[1:])
        else:
            message = messages[0]

        print('{level}:{name}: {message}'.format(
            level=level, name=self.name, message=message))


def get(name):
    ''' Get a new named logger. Usually called like: logger.get(__name__).Short
    and sweet '''
    return Logger(name)

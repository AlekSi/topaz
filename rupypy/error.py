import os


class RubyError(Exception):
    def __init__(self, w_value):
        self.w_value = w_value

    def __str__(self):
        return "<RubyError: %s>" % self.w_value


def format_traceback(space, exc):
    last_instr_idx = 0
    frame = exc.frame
    yield "%s:%d:in `%s': %s (%s)\n" % (
        frame.get_filename(),
        frame.get_lineno(exc.last_instructions, last_instr_idx),
        frame.get_code_name(),
        exc.msg,
        space.getclass(exc).name,
    )
    last_instr_idx += 1
    frame = frame.backref()
    while frame is not None and frame.has_contents():
        yield "\tfrom %s:%d:in `%s'\n" % (
            frame.get_filename(),
            frame.get_lineno(exc.last_instructions, last_instr_idx),
            frame.get_code_name(),
        )
        last_instr_idx += 1
        frame = frame.backref()


def print_traceback(space, w_exc):
    for line in format_traceback(space, w_exc):
        os.write(2, line)


def error_for_oserror(space, exc):
    assert isinstance(exc, OSError)
    return space.error(
        space.w_SystemCallError,
        os.strerror(exc.errno),
        [space.newint(exc.errno)]
    )

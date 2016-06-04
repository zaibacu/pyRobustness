import signal
from contextlib import contextmanager


def alarm_create(timeout, callback):
    signal.signal(signal.SIGALRM, callback)
    signal.alarm(timeout)

    def reset():
        return signal.alarm(0)

    return reset


@contextmanager
def alarm_context(*args, **kwargs):
    reset = alarm_create(*args, **kwargs)
    yield
    reset()

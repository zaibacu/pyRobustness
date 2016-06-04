import signal
import threading
from contextlib import contextmanager


def _signal_timer(timeout, callback):
    def wrapper(*args):
        return callback()

    signal.signal(signal.SIGALRM, wrapper)
    signal.alarm(timeout)

    def reset():
        return signal.alarm(0)

    return reset


def _threading_timer(timeout, callback):
    timer = threading.Timer(timeout, callback)
    timer.start()

    def reset():
        return timer.cancel()

    return reset


def alarm_create(timeout, callback, use_signal=True):
    import platform
    if use_signal and platform.system() != "Windows":  # SIGALRM does not work on Windows
        return _signal_timer(timeout, callback)
    else:
        return _threading_timer(timeout, callback)


@contextmanager
def alarm_context(*args, **kwargs):
    reset = alarm_create(*args, **kwargs)
    yield
    reset()

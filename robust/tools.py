from functools import wraps
from exception import ContinuousFailureException, TimeoutException


def _fail(ex, on_fail=None):
    if on_fail:
        on_fail()
    else:
        raise ex


def retry(limit, on_fail=None):
    """
    Retries same function N times, goes to fail callback if unable to succeed
    """
    def injector(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for _ in range(0, limit):
                try:
                    return fn(*args, **kwargs)
                except:
                    continue

            # If you're here - you deserved it
            _fail(ContinuousFailureException, on_fail)

        return wrapper
    return injector


def timeout(limit, on_fail=None):
    """
    Waits for function to respond N seconds
    """
    def injector(fn):
        import signal

        def timeout_handler(signum, frame):
            return _fail(TimeoutException, on_fail)

        @wraps(fn)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(limit)

            try:
                return fn(*args, **kwargs)
            finally:
                signal.alarm(0)

        return wrapper
    return injector

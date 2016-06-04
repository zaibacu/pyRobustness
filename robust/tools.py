from functools import wraps
from robust.exception import (ContinuousFailureException,
                              TimeoutException,
                              ConnectionCutException)


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
                except Exception:
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
        from robust.alarm import alarm_context

        def timeout_handler():
            return _fail(TimeoutException, on_fail)

        @wraps(fn)
        def wrapper(*args, **kwargs):
            with alarm_context(limit, timeout_handler):
                return fn(*args, **kwargs)

        return wrapper
    return injector


def breaker(limit, revive, on_fail=None):
    """
    Allows :limit: failures, after which it cuts connection.
    After :revive: seconds it allows one connection to pass.
    If it succeeds - counter is reset, if doesn't - we wait another :revive: seconds
    """

    def injector(fn):
        from robust.alarm import alarm_create
        counter = 0
        reset_fn = None

        def revive_handler():
            nonlocal counter
            counter -= 1

        @wraps(fn)
        def wrapper(*args, **kwargs):
            nonlocal counter
            nonlocal reset_fn
            if counter >= limit:
                return _fail(ConnectionCutException, on_fail)

            result = None
            try:
                result = fn(*args, **kwargs)
            except Exception:
                counter += 1
                if counter >= limit:
                    reset_fn = alarm_create(revive, revive_handler)
                raise
            else:
                if reset_fn:
                    reset_fn()
                counter = 0
                return result

        return wrapper

    return injector

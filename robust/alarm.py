import signal


def alarm_create(timeout, callback):
    signal.signal(signal.SIGALRM, callback)
    signal.alarm(timeout)

    def reset():
        return signal.alarm(0)

    return reset

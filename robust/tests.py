from pytest import raises
from robust.tools import retry, timeout, breaker
from robust.exception import (ContinuousFailureException,
                              TimeoutException,
                              ConnectionCutException)


class TestRetryCase(object):

    def test_happy_case(self):
        @retry(5)
        def dummy():
            return 42

        assert 42 == dummy()

    def test_fail_case(self):
        @retry(5)
        def fail():
            raise RuntimeError("Don't know what to do")

        with raises(ContinuousFailureException):
            fail()

    def test_callback(self):
        passed = False

        def do_pass():
            nonlocal passed
            passed = True

        @retry(5, do_pass)
        def fail():
            raise RuntimeError("Don't know what to do")

        do_pass()
        assert passed


class TestTimeoutCase(object):

    def test_happy_case(self):
        @timeout(1)
        def dummy():
            return 42

        assert 42 == dummy()

    def test_failure_case(self):
        @timeout(1)
        def fail():
            while True:
                pass

        with raises(TimeoutException):
            fail()

    def test_callback(self):
        passed = False

        def do_pass():
            nonlocal passed
            passed = True

        @timeout(1, do_pass)
        def fail():
            while True:
                pass

        do_pass()
        assert passed


class TestBreakerPattern(object):

    def test_cut_after_5_failures(self):

        @breaker(limit=5, revive=30)
        def fail():
            raise RuntimeError("Just failing for no good reason")

        with raises(ConnectionCutException):
            counter = 0
            while True:
                try:
                    fail()
                except RuntimeError:
                    pass
                counter += 1

        assert counter == 5

    def test_revive_after_1_second(self):
        import time

        @breaker(limit=2, revive=1)
        def fail():
            raise RuntimeError("Failing and failing")

        while True:
            try:
                fail()
            except RuntimeError:
                pass
            except ConnectionCutException:
                break

        with raises(ConnectionCutException):
            fail()

        time.sleep(1)

        with raises(RuntimeError):
            fail()

        with raises(ConnectionCutException):
            fail()

    def test_revive_with_timeout(self):
        import time

        @breaker(limit=1, revive=2)
        @timeout(1)
        def fail():
            time.sleep(2)

        with raises(TimeoutException):
            fail()

        with raises(ConnectionCutException):
            fail()

        time.sleep(2)

        with raises(TimeoutException):
            fail()


class TestTimers(object):

    def test_signal_timer(self):
        import time
        from robust.alarm import _signal_timer
        reached = False

        def callback():
            nonlocal reached
            reached = True

        _signal_timer(1, callback)
        time.sleep(2)
        assert reached

    def test_threading_timer(self):
        import time
        from robust.alarm import _threading_timer
        reached = False

        def callback():
            nonlocal reached
            reached = True

        _threading_timer(1, callback)
        time.sleep(2)
        assert reached

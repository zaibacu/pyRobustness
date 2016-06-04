from pytest import raises
from robust.tools import retry, timeout
from robust.exception import ContinuousFailureException, TimeoutException


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

        @breaker(fail_count=5, check=30)
        def fail():
            raise RuntimeError("Just failing for no good reason")

        with raises(ConnectionCutException):
            counter = 0
            for i in range(0, 5):
                fail()
                counter += 1

        assert counter == 5

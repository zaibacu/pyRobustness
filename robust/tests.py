import unittest
from tools import retry, timeout
from exception import ContinuousFailureException, TimeoutException


class RetryCase(unittest.TestCase):
    def test_happy_case(self):
        @retry(5)
        def dummy():
            return 42

        self.assertEqual(42, dummy())

    def test_fail_case(self):
        @retry(5)
        def fail():
            raise RuntimeError("Don't know what to do")

        self.assertRaises(ContinuousFailureException, fail)

    def test_callback(self):
        passed = False

        def do_pass():
            nonlocal passed
            passed = True

        @retry(5, do_pass)
        def fail():
            raise RuntimeError("Don't know what to do")

        do_pass()
        self.assertEqual(True, passed)


class TimeoutCase(unittest.TestCase):
    def test_happy_case(self):
        @timeout(1)
        def dummy():
            return 42

        self.assertEqual(42, dummy())

    def test_failure_case(self):
        @timeout(1)
        def fail():
            while True:
                pass

        self.assertRaises(TimeoutException, fail)

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
        self.assertEqual(True, passed)



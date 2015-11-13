[![Build Status](https://travis-ci.org/zaibacu/pyRobustness.svg?branch=master)](https://travis-ci.org/zaibacu/pyRobustness)
About
=====
A simple util library for creating applications which needs to keep running, despite abnormalities

Installing
==========
`pip install pyrobustness`

Usage
=====

Timeout example:
```python
from robust.tools import timeout


@timeout(5)
def very_long_job():
    import time
    while True:
      print("Zzz")
      time.sleep(1)
    
very_long_job()
```

Retry example:
```python
from robust.tools import retry

@retry(5)
def very_broken_method():
    print(".")
    raise RuntimeError("Something is broken...")
    
very_broken_method()

```

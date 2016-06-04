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

while True:
    very_broken_method()

```

Circuit Breaker example:

```python
import time
from robust.tools import breaker

counter = 0

@breaker(limit=5, revive=5)
def very_broken_method():
    nonlocal counter
    if counter <= 5:
        counter += 1
    	raise RuntimeError("Something is broken...")
    else:
        print("We've made it!")


while True:
    try:
    	very_broken_method()
    except RuntimeError:
        pass
    except Exception:
        break

time.sleep(5)
very_broken_method()
```


Version History
===============
- 1.1: 
     - Additional type for alarm - threading to support Windows OS, or certain cases when signal is not working as supposed
     - CircuitBreaker pattern, inspired by speech by Daniel Martins @Pycon 2016
- 1.0: Initial version

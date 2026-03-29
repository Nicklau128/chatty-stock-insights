# integrations/retry.py

import time
import random
from typing import Callable, TypeVar

T = TypeVar("T")


def retry_with_backoff(
    func: Callable[[], T],
    retries: int = 3,
    base_delay: float = 1.0,
) -> T:
    """
    Generic exponential backoff retry.
    """

    for attempt in range(retries):
        try:
            return func()

        except Exception as e:
            if attempt == retries - 1:
                raise

            delay = base_delay * (2 ** attempt)
            jitter = random.uniform(0, 0.5)
            time.sleep(delay + jitter)

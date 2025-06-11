# modules/decorators.py

import traceback
import sys
import functools

def exception_logger(logger):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                tb = traceback.extract_tb(sys.exc_info()[2])[-1]  # Dernière ligne active
                filename = tb.filename
                lineno = tb.lineno
                name = tb.name
                line = tb.line.strip() if tb.line else "???" 

                print(
                    f"Exception in {name}() [{filename}:{lineno}] → {type(e).__name__}: « {line} »"
                )
                print(f"Full traceback:\n{traceback.format_exc()}")
                raise
        return wrapper
    return decorator

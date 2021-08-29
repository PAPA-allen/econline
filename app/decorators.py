from threading import Thread
from functools import wraps

def async_call(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper

#decorator design pattern
def pre_printer(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        print("Pre `printer")
        return func(*args, **kwargs)
    return decorator


#example of a decoratorated design function
@pre_printer
def printer1():
    print("allen aryee")

ala = printer1()
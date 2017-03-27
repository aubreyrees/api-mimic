__all__ = ['signature']


try:
    import inspect
    signature = inspect.signature
except:
    import funcsigs
    signature = funcsigs.signature

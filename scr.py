def benchmark(func):
    import time

    def wrapper(*args, **kwargs):
        start = time.time()
        return_value = func(*args, **kwargs)
        end = time.time()
        print(f'  --- {func.__name__} - successful! - {round(end - start, 2)} sec.')
        return return_value
    return wrapper

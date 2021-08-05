from concurrent.futures import ThreadPoolExecutor

pool = ThreadPoolExecutor(128)

def exec(func):
    pool.submit()
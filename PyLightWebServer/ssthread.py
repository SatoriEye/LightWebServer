

import concurrent.futures

def func(x):
    # Do something with x
    return x * x

# Create a thread pool with 4 threads
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    # Submit tasks to the thread pool
    results = [executor.submit(func, i) for i in range(10)]

    # Wait for all tasks to complete
    concurrent.futures.wait(results)

    # Print the results
    for future in results:
        print(future.result())

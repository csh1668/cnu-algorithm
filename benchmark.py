import platform
import time
from functools import wraps
import inspect

_results = []

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
RESET = '\033[0m'

class BenchmarkResult:
    def __init__(self, name, elapsed, mean, std, error):
        self.name = name
        self.elapsed = elapsed
        self.mean = mean
        self.std = std
        self.error = error

def measure(repeat=1):
    def _measure(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            sig = inspect.signature(func)
            params = list(sig.parameters.keys())
            is_class_method = params and params[0] == 'self'

            res = None

            def run():
                nonlocal res
                b = time.time()
                res = func(*args, **kwargs)
                a = time.time()
                return a - b

            elapsed = run()
            mean, std, error = 0, 0, 0
            if repeat > 1:
                times = [elapsed]
                for _ in range(1, repeat):
                    times.append(run())
                mean = sum(times) / repeat
                std = (sum((t - mean) ** 2 for t in times) / repeat) ** 0.5
                error = std / (repeat ** 0.5)
                elapsed += sum(times[1:])

            args_str = ', '.join(repr(arg) for arg in (args[1:] if is_class_method else args))
            kwargs_str = ', '.join(f"{k}={v!r}" for k, v in kwargs.items())
            all_args = ', '.join(filter(None, [args_str, kwargs_str]))
            _results.append(BenchmarkResult(f'{func.__name__}({all_args})', elapsed, mean, std, error))
            return res

        return wrapper
    return _measure

def _float2str(f): return f'{f:.4f}s'

def _cur_runtime():
    return platform.python_implementation() + ' ' + platform.python_version()

def print_results(title=None):
    if title is not None: print(f"{BLUE}{title}{RESET} ({_cur_runtime()})")

    columns = ['Name', 'Elapsed Time', 'Mean', 'Std', 'Error']
    table = [columns, *[[res.name, _float2str(res.elapsed), _float2str(res.mean), _float2str(res.std), _float2str(res.error)] for res in _results]]
    max_lens = [max([len(str(seg[i])) for seg in table]) for i in range(len(columns))]

    max_elapsed, min_elapsed = max([res.elapsed for res in _results]), min([res.elapsed for res in _results])
    max_mean, min_mean = max([res.mean for res in _results]), min([res.mean for res in _results])
    max_std, min_std = max([res.std for res in _results]), min([res.std for res in _results])
    max_error, min_error = max([res.error for res in _results]), min([res.error for res in _results])

    max_vars = list(map(_float2str, [max_elapsed, max_mean, max_std, max_error]))
    min_vars = list(map(_float2str, [min_elapsed, min_mean, min_std, min_error]))

    for i in range(len(table)):
        for j in range(len(columns)):
            if i == 0: print(f"{table[i][j]:^{max_lens[j]}}", end=' ')
            else:
                if columns[j] != 'Name':
                    color = GREEN if table[i][j] == min_vars[j - 1] else (RED if table[i][j] == max_vars[j - 1] else YELLOW)
                    print(f"{color}{table[i][j]:^{max_lens[j]}}{RESET}", end=' ')
                else:
                    print(f"{table[i][j]:^{max_lens[j]}}", end=' ')
        print()
    # max_name_len = max([len(name) for (name, *_), _ in result] + [len('Name')])
    # print(f"{'Method':<{max_name_len}}: Elapsed Time")
    # for i in range(len(result)):
    #     name, elapsed = result[i][0]
    #     color = GREEN if i == 0 else (YELLOW if i != len(result) - 1 else RED)
    #     result[i].append(f"{color}{name:<{max_name_len}}: {elapsed:.4f}s{RESET}")
    # for _, _, line in sorted(result, key=lambda x: x[1]): print(line)
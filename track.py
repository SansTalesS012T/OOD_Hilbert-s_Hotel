import os
import psutil

def get_process_memory() -> int:
    process = psutil.Process(os.getpid())
    return process.memory_info().rss
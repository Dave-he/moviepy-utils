import logging
import os
from contextlib import redirect_stdout

# 禁用 Python 标准输出（针对 print 语句）
def suppress_output(func):
    def wrapper(*args, **kwargs):
        with open(os.devnull, 'w') as f, redirect_stdout(f):
            return func(*args, **kwargs)
    return wrapper


# 设置 moviepy 的日志级别为 ERROR，只在出现错误时打印日志
logging.getLogger("moviepy").setLevel(logging.ERROR)
logging.getLogger("imageio").setLevel(logging.ERROR)
# 全局禁止 FFmpeg 日志（在脚本开头添加）
os.environ["IMAGEIO_FFMPEG_LOG_LEVEL"] = "error"  # 可选值：'debug', 'info', 'warn', 'error', 'quiet'

from loguru import logger
import sys

# 配置Loguru日志器
# 将日志输出到控制台，设置日志级别为DEBUG
logger.add(sys.stdout, format="{time} {level} {message}", level="INFO")

# 将日志输出到文件，每天轮转一次，保留7天的日志文件
logger.add(
    "logs/explorer_{time}.log", rotation="1 day", retention="7 days", level="DEBUG"
)

# Export logger
loguru_looger = logger


"""
# 示例日志记录
logger.debug("这是一条调试信息")
logger.info("这是一条普通信息")
logger.warning("这是一条警告信息")
logger.error("这是一条错误信息")
logger.critical("这是一条严重错误信息")

# 如果你需要捕获并记录未处理的异常，可以使用以下方法
try:
    1 / 0
except ZeroDivisionError:
    logger.exception("捕获到未处理的异常：")
"""

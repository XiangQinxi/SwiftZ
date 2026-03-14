""""""
"""
错误日志模块
提供统一的错误日志记录和查看功能
"""

import io
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler

# 日志目录
LOG_DIR = Path("./logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 日志文件路径
ERROR_LOG_FILE = LOG_DIR / "errors.log"
ACCESS_LOG_FILE = LOG_DIR / "access.log"
DEBUG_LOG_FILE = LOG_DIR / "debug.log"

# 日志格式
ERROR_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# 最大日志文件大小（5MB）
MAX_LOG_SIZE = 5 * 1024 * 1024
# 保留的日志文件数量
BACKUP_COUNT = 3


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    获取一个配置好的 logger
    
    Args:
        name: logger 名称
        level: 日志级别
    
    Returns:
        配置好的 Logger 对象
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 避免重复添加 handler
    if logger.handlers:
        return logger
    
    # 控制台 handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_formatter = logging.Formatter(ERROR_FORMAT, DATE_FORMAT)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # 文件 handler（按日期分割）
    try:
        file_handler = RotatingFileHandler(
            ERROR_LOG_FILE,
            maxBytes=MAX_LOG_SIZE,
            backupCount=BACKUP_COUNT,
            encoding="utf-8"
        )
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(ERROR_FORMAT, DATE_FORMAT)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    except Exception:
        pass  # 如果无法写入文件，只使用控制台
    
    return logger


# 创建常用 logger
error_logger = get_logger("swiftz.error", logging.ERROR)
access_logger = get_logger("swiftz.access", logging.INFO)
debug_logger = get_logger("swiftz.debug", logging.DEBUG)


def log_error(module: str, error: Exception, context: str = None, user_id: int = None):
    """
    记录错误日志
    
    Args:
        module: 发生错误的模块名
        error: 异常对象
        context: 额外上下文信息
        user_id: 发生错误的用户 ID
    """
    context_str = f" | Context: {context}" if context else ""
    user_str = f" | User: {user_id}" if user_id else ""
    
    error_logger.error(
        f"{module} | {type(error).__name__}: {str(error)}{context_str}{user_str}",
        exc_info=True
    )


def log_access(action: str, user_id: int = None, package_id: str = None, details: str = None):
    """
    记录访问/操作日志
    
    Args:
        action: 操作类型（login, logout, upload, download, delete 等）
        user_id: 用户 ID
        package_id: 文件包 ID
        details: 额外详情
    """
    user_str = f"User: {user_id}" if user_id else "Anonymous"
    package_str = f"Package: {package_id}" if package_id else ""
    details_str = f"Details: {details}" if details else ""
    
    access_logger.info(f"{action} | {user_str} | {package_str} | {details_str}")


def log_debug(message: str, details: dict = None):
    """
    记录调试日志
    
    Args:
        message: 日志消息
        details: 额外详情字典
    """
    details_str = f" | {details}" if details else ""
    debug_logger.debug(f"{message}{details_str}")


def get_recent_errors(lines: int = 100) -> list:
    """
    获取最近的错误日志
    
    Args:
        lines: 返回的行数
    
    Returns:
        日志行列表
    """
    if not ERROR_LOG_FILE.exists():
        return []
    
    try:
        with open(ERROR_LOG_FILE, "r", encoding="utf-8") as f:
            all_lines = f.readlines()
            return all_lines[-lines:]
    except Exception:
        return []


def get_error_count() -> dict:
    """
    获取错误统计
    
    Returns:
        包含错误计数的字典
    """
    if not ERROR_LOG_FILE.exists():
        return {"total": 0, "today": 0, "this_week": 0}
    
    try:
        with open(ERROR_LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        total = len(lines)
        
        today = datetime.now().strftime("%Y-%m-%d")
        this_week = (datetime.now().date().isoformat())
        
        today_count = sum(1 for line in lines if line.startswith(today))
        
        # 计算本周（最近7天）
        from datetime import timedelta
        week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        week_count = sum(1 for line in lines if line[:10] >= week_ago)
        
        return {
            "total": total,
            "today": today_count,
            "this_week": min(week_count, total),
            "last_error": lines[-1].strip() if lines else None
        }
    except Exception:
        return {"total": 0, "today": 0, "this_week": 0}


def clear_old_logs(days: int = 7):
    """
    清理旧的日志文件
    
    Args:
        days: 保留最近多少天的日志
    """
    cutoff = time.time() - (days * 24 * 60 * 60)
    
    for log_file in [ERROR_LOG_FILE, ACCESS_LOG_FILE, DEBUG_LOG_FILE]:
        if log_file.exists():
            try:
                if log_file.stat().st_mtime < cutoff:
                    log_file.unlink()
            except Exception:
                pass


# Streamlit 错误处理器
class StreamlitErrorHandler:
    """
    Streamlit 全局错误处理器
    可以捕获 Streamlit 应用中的未处理异常
    """
    
    def __init__(self):
        self.logger = error_logger
    
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        """
        处理未捕获的异常
        """
        if issubclass(exc_type, KeyboardInterrupt):
            # 不记录键盘中断
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        self.logger.error(
            f"Uncaught exception: {exc_type.__name__}: {exc_value}",
            exc_info=(exc_type, exc_value, exc_traceback)
        )


# 安装全局错误处理器
def install_error_handler():
    """
    安装全局错误处理器
    """
    sys.excepthook = StreamlitErrorHandler().handle_exception
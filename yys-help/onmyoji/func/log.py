import logging
import sys
import os
from datetime import datetime
from config import CONFIG

def setup_logging():
    """设置日志系统"""
    # 创建logs文件夹（如果不存在）
    log_config = CONFIG['LOGGING']
    if not os.path.exists(log_config['FILE_PATH']):
        os.makedirs(log_config['FILE_PATH'])
    
    # 生成日志文件名
    log_filename = os.path.join(
        log_config['FILE_PATH'],
        datetime.now().strftime(log_config['FILE_NAME_FORMAT'])
    )
    
    # 配置日志格式，只使用文件处理器
    logging.basicConfig(
        level=getattr(logging, log_config['LEVEL']),
        format=log_config['FORMAT'],
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8')
            # 移除 logging.StreamHandler(sys.stdout)
        ]
    )
    
    logging.info("日志系统初始化完成")

# 初始化日志系统
setup_logging()
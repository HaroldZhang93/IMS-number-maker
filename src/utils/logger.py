#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
日志管理模块
"""

import os
import logging
from logging.handlers import RotatingFileHandler

class Logger:
    """日志管理类，用于记录应用程序日志"""
    
    _instance = None
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """初始化日志管理器"""
        if self._initialized:
            return
        
        # 日志目录
        self.log_dir = os.path.expanduser("~/Documents/IMS-number-maker/logs")
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir, exist_ok=True)
        
        # 日志文件路径
        self.log_file = os.path.join(self.log_dir, "app.log")
        
        # 创建日志记录器
        self.logger = logging.getLogger("IMS-number-maker")
        self.logger.setLevel(logging.DEBUG)
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 创建文件处理器
        file_handler = RotatingFileHandler(
            self.log_file, maxBytes=1024*1024*5, backupCount=5, encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        
        # 创建格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        # 添加处理器
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        
        self._initialized = True
    
    def get_logger(self):
        """获取日志记录器
        
        Returns:
            logging.Logger: 日志记录器
        """
        return self.logger
    
    def debug(self, message):
        """记录调试日志
        
        Args:
            message: 日志消息
        """
        self.logger.debug(message)
    
    def info(self, message):
        """记录信息日志
        
        Args:
            message: 日志消息
        """
        self.logger.info(message)
    
    def warning(self, message):
        """记录警告日志
        
        Args:
            message: 日志消息
        """
        self.logger.warning(message)
    
    def error(self, message):
        """记录错误日志
        
        Args:
            message: 日志消息
        """
        self.logger.error(message)
    
    def critical(self, message):
        """记录严重错误日志
        
        Args:
            message: 日志消息
        """
        self.logger.critical(message) 
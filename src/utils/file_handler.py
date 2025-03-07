#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
文件处理工具模块
"""

import os
import datetime

class FileHandler:
    """文件处理类，用于保存和加载脚本文件"""
    
    @staticmethod
    def save_script(script_content, file_path=None):
        """保存脚本内容到文件
        
        Args:
            script_content: 脚本内容
            file_path: 文件路径，如果为None则自动生成
            
        Returns:
            tuple: (是否成功, 文件路径或错误消息)
        """
        try:
            # 如果未指定路径，则自动生成
            if not file_path:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                file_path = f"ims_script_{timestamp}.txt"
            
            # 确保目录存在
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            return True, file_path
        
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def load_script(file_path):
        """从文件加载脚本内容
        
        Args:
            file_path: 文件路径
            
        Returns:
            tuple: (是否成功, 脚本内容或错误消息)
        """
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                return False, f"文件不存在: {file_path}"
            
            # 读取文件
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return True, content
        
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def get_default_save_directory():
        """获取默认保存目录
        
        Returns:
            str: 默认保存目录路径
        """
        # 获取用户文档目录
        documents_dir = os.path.expanduser("~/Documents")
        
        # 创建应用专用目录
        app_dir = os.path.join(documents_dir, "IMS-number-maker")
        
        # 确保目录存在
        if not os.path.exists(app_dir):
            os.makedirs(app_dir)
        
        return app_dir 
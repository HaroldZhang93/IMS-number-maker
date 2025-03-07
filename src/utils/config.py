#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
配置管理模块
"""

import os
import json

class ConfigManager:
    """配置管理类，用于保存和加载用户配置"""
    
    def __init__(self):
        """初始化配置管理器"""
        # 配置文件路径
        self.config_dir = os.path.expanduser("~/Documents/IMS-number-maker")
        self.config_file = os.path.join(self.config_dir, "config.json")
        
        # 默认配置
        self.default_config = {
            "domain": "dra.ims.sdt",
            "cfn": "cg.dra.ims.sdt",
            "password": "123456",
            "sifc_id": "100",
            "scscf": "scscfpool01",
            "cc": "86",
            "lata": "10",
            "last_start_number": "+861088889001",
            "last_count": "10",
            "last_save_dir": self._get_default_save_dir()
        }
        
        # 当前配置
        self.config = self.load_config()
    
    def _get_default_save_dir(self):
        """获取默认保存目录"""
        save_dir = os.path.join(self.config_dir, "scripts")
        if not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)
        return save_dir
    
    def load_config(self):
        """加载配置
        
        Returns:
            dict: 配置字典
        """
        # 确保配置目录存在
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir, exist_ok=True)
        
        # 如果配置文件不存在，创建默认配置
        if not os.path.exists(self.config_file):
            return self.save_config(self.default_config)
        
        # 读取配置文件
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 确保所有默认配置项都存在
            for key, value in self.default_config.items():
                if key not in config:
                    config[key] = value
            
            return config
        
        except Exception:
            # 如果读取失败，返回默认配置
            return self.default_config
    
    def save_config(self, config):
        """保存配置
        
        Args:
            config: 配置字典
            
        Returns:
            dict: 保存的配置字典
        """
        # 确保配置目录存在
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir, exist_ok=True)
        
        # 写入配置文件
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
            
            return config
        
        except Exception:
            # 如果保存失败，返回当前配置
            return self.config
    
    def get_config(self, key=None, default=None):
        """获取配置项
        
        Args:
            key: 配置项键名，如果为None则返回整个配置
            default: 默认值，如果配置项不存在则返回此值
            
        Returns:
            配置项值或整个配置字典
        """
        if key is None:
            return self.config
        
        return self.config.get(key, default)
    
    def set_config(self, key, value):
        """设置配置项
        
        Args:
            key: 配置项键名
            value: 配置项值
            
        Returns:
            bool: 是否成功
        """
        self.config[key] = value
        self.save_config(self.config)
        return True
    
    def update_config(self, config_dict):
        """更新多个配置项
        
        Args:
            config_dict: 配置字典
            
        Returns:
            bool: 是否成功
        """
        self.config.update(config_dict)
        self.save_config(self.config)
        return True 
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
输入验证器模块
"""

import re

class InputValidator:
    """输入验证器类，用于验证用户输入的参数"""
    
    @staticmethod
    def validate_phone_number(phone):
        """验证电话号码格式
        
        Args:
            phone: 电话号码，如 +861088889001
            
        Returns:
            bool: 是否有效
        """
        # 验证格式：可选的+号，后跟8-15位数字
        pattern = r'^\+?\d{8,15}$'
        return bool(re.match(pattern, phone))
    
    @staticmethod
    def validate_domain(domain):
        """验证域名格式
        
        Args:
            domain: 域名，如 dra.ims.sdt
            
        Returns:
            bool: 是否有效
        """
        # 简单域名验证：字母、数字、点、连字符
        pattern = r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, domain))
    
    @staticmethod
    def validate_count(count_str):
        """验证号码数量
        
        Args:
            count_str: 号码数量字符串
            
        Returns:
            bool: 是否有效
        """
        try:
            count = int(count_str)
            return 1 <= count <= 10000  # 限制合理范围
        except ValueError:
            return False
    
    @staticmethod
    def validate_params(params):
        """验证参数字典
        
        Args:
            params: 参数字典
            
        Returns:
            tuple: (是否有效, 错误消息)
        """
        required_fields = ['domain', 'cfn', 'password', 'sifc_id', 'scscf', 'cc', 'lata']
        
        # 检查必填字段
        for field in required_fields:
            if field not in params or not params[field]:
                return False, f"缺少必填参数: {field}"
        
        # 验证域名
        if not InputValidator.validate_domain(params['domain']):
            return False, "域名格式无效"
        
        # 验证数字字段
        try:
            int(params['sifc_id'])
            int(params['cc'])
            int(params['lata'])
        except ValueError:
            return False, "数字参数格式无效"
        
        return True, "" 
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
主窗口模块
"""

import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QMessageBox, QTabWidget, QFileDialog,
    QLabel, QStatusBar, QAction, QMenu, QToolBar
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont

from src.ui.widgets import LabeledInput, NumberInput, ScriptPreview, ParameterForm
from src.core.generator import ScriptGenerator
from src.core.validator import InputValidator
from src.utils.config import ConfigManager
from src.utils.file_handler import FileHandler
from src.utils.logger import Logger

class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        """初始化主窗口"""
        super().__init__()
        
        # 初始化日志
        self.logger = Logger()
        self.logger.info("应用程序启动")
        
        # 初始化配置
        self.config_manager = ConfigManager()
        
        # 初始化生成器
        self.generator = ScriptGenerator()
        
        # 初始化验证器
        self.validator = InputValidator()
        
        # 设置窗口属性
        self.setWindowTitle("IMS号码生成器 by ZHN")
        self.setMinimumSize(800, 600)
        
        # 创建中心控件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 创建主布局
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # 创建UI
        self._create_ui()
        
        # 加载配置
        self._load_config()
    
    def _create_ui(self):
        """创建UI"""
        # 创建标题
        title_label = QLabel("IMS号码生成器")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.main_layout.addWidget(title_label)
        
        # 创建内容布局
        content_layout = QHBoxLayout()
        
        # 创建左侧布局
        left_layout = QVBoxLayout()
        
        # 创建参数表单
        self.param_form = ParameterForm("网元参数设置")
        self.param_form.add_input("domain", "域名", "dra.ims.sdt")
        self.param_form.add_input("cfn", "CFN", "cg.dra.ims.sdt")
        self.param_form.add_input("password", "密码", "123456")
        self.param_form.add_input("sifc_id", "SIFC ID", "100")
        self.param_form.add_input("scscf", "SCSCF", "scscfpool01")
        self.param_form.add_input("cc", "国家码", "86")
        self.param_form.add_input("lata", "LATA", "10")
        
        # 创建号码设置
        self.number_form = ParameterForm("号码设置")
        self.number_form.add_input("start_number", "起始号码", "+861088889001")
        self.number_form.add_number_input("count", "号码数量", 10, 1, 1000)
        
        # 创建生成按钮
        self.generate_button = QPushButton("生成脚本")
        self.generate_button.setMinimumHeight(40)
        self.generate_button.clicked.connect(self.generate_script)
        
        # 添加到左侧布局
        left_layout.addWidget(self.param_form)
        left_layout.addWidget(self.number_form)
        left_layout.addWidget(self.generate_button)
        
        # 创建右侧布局
        right_layout = QVBoxLayout()
        
        # 创建脚本预览
        self.script_preview = ScriptPreview()
        
        # 添加到右侧布局
        right_layout.addWidget(self.script_preview)
        
        # 添加到内容布局
        content_layout.addLayout(left_layout, 1)
        content_layout.addLayout(right_layout, 2)
        
        # 添加到主布局
        self.main_layout.addLayout(content_layout)
        
        # 创建状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")
        
        # 创建菜单栏
        self._create_menu()
    
    def _create_menu(self):
        """创建菜单栏"""
        # 创建菜单栏
        menu_bar = self.menuBar()
        
        # 创建文件菜单
        file_menu = menu_bar.addMenu("文件")
        
        # 创建新建操作
        new_action = QAction("新建", self)
        new_action.triggered.connect(self.new_script)
        file_menu.addAction(new_action)
        
        # 创建保存操作
        save_action = QAction("保存", self)
        save_action.triggered.connect(self.save_script)
        file_menu.addAction(save_action)
        
        # 添加分隔符
        file_menu.addSeparator()
        
        # 创建退出操作
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 创建帮助菜单
        help_menu = menu_bar.addMenu("帮助")
        
        # 创建关于操作
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def _load_config(self):
        """加载配置"""
        # 获取配置
        config = self.config_manager.get_config()
        
        # 设置参数表单值
        param_values = {
            "domain": config.get("domain", "dra.ims.sdt"),
            "cfn": config.get("cfn", "cg.dra.ims.sdt"),
            "password": config.get("password", "123456"),
            "sifc_id": config.get("sifc_id", "100"),
            "scscf": config.get("scscf", "scscfpool01"),
            "cc": config.get("cc", "86"),
            "lata": config.get("lata", "10")
        }
        self.param_form.set_values(param_values)
        
        # 设置号码表单值
        number_values = {
            "start_number": config.get("last_start_number", "+861088889001"),
            "count": int(config.get("last_count", "10"))
        }
        self.number_form.set_values(number_values)
    
    def _save_config(self):
        """保存配置"""
        # 获取参数表单值
        param_values = self.param_form.get_values()
        
        # 获取号码表单值
        number_values = self.number_form.get_values()
        
        # 更新配置
        config = {
            "domain": param_values["domain"],
            "cfn": param_values["cfn"],
            "password": param_values["password"],
            "sifc_id": param_values["sifc_id"],
            "scscf": param_values["scscf"],
            "cc": param_values["cc"],
            "lata": param_values["lata"],
            "last_start_number": number_values["start_number"],
            "last_count": str(number_values["count"])
        }
        
        # 保存配置
        self.config_manager.update_config(config)
    
    def generate_script(self):
        """生成脚本"""
        try:
            # 获取参数
            params = self.param_form.get_values()
            
            # 获取号码设置
            start_number = self.number_form.get_values()["start_number"]
            count = self.number_form.get_values()["count"]
            
            # 验证参数
            valid, error_msg = self.validator.validate_params(params)
            if not valid:
                QMessageBox.warning(self, "参数错误", error_msg)
                return
            
            # 验证号码
            if not self.validator.validate_phone_number(start_number):
                QMessageBox.warning(self, "号码错误", "起始号码格式无效")
                return
            
            # 验证数量
            if not self.validator.validate_count(str(count)):
                QMessageBox.warning(self, "数量错误", "号码数量必须在1-10000之间")
                return
            
            # 生成脚本
            script = self.generator.generate_full_script(start_number, count, params)
            
            # 显示脚本
            self.script_preview.set_text(script)
            
            # 更新状态栏
            self.status_bar.showMessage(f"已生成 {count} 个号码的脚本")
            
            # 保存配置
            self._save_config()
            
            # 记录日志
            self.logger.info(f"生成脚本: 起始号码={start_number}, 数量={count}")
        
        except Exception as e:
            # 显示错误
            QMessageBox.critical(self, "生成错误", str(e))
            
            # 记录日志
            self.logger.error(f"生成脚本错误: {str(e)}")
    
    def new_script(self):
        """新建脚本"""
        # 清空脚本预览
        self.script_preview.set_text("")
        
        # 更新状态栏
        self.status_bar.showMessage("已新建脚本")
    
    def save_script(self):
        """保存脚本"""
        # 获取脚本内容
        script = self.script_preview.get_text()
        
        # 检查是否为空
        if not script:
            QMessageBox.warning(self, "保存错误", "没有可保存的脚本内容")
            return
        
        # 获取保存路径
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存脚本", "", "文本文件 (*.txt);;所有文件 (*)"
        )
        
        if not file_path:
            return
        
        try:
            # 保存脚本
            success, result = FileHandler.save_script(script, file_path)
            
            if success:
                # 显示提示
                QMessageBox.information(self, "保存成功", f"脚本已保存到: {result}")
                
                # 更新状态栏
                self.status_bar.showMessage(f"脚本已保存到: {result}")
                
                # 记录日志
                self.logger.info(f"保存脚本: {result}")
            else:
                # 显示错误
                QMessageBox.critical(self, "保存错误", result)
                
                # 记录日志
                self.logger.error(f"保存脚本错误: {result}")
        
        except Exception as e:
            # 显示错误
            QMessageBox.critical(self, "保存错误", str(e))
            
            # 记录日志
            self.logger.error(f"保存脚本错误: {str(e)}")
    
    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(
            self,
            "关于 IMS号码生成器 by ZHN",
            "IMS号码生成器 v1.0\n\n"
            "这是一个用于IMS服务器的SIP号码生成工具，可以根据特定规则生成放号脚本。\n\n"
            "© 2025 All Rights Reserved"
        )
    
    def closeEvent(self, event):
        """关闭事件处理
        
        Args:
            event: 关闭事件
        """
        # 保存配置
        self._save_config()
        
        # 记录日志
        self.logger.info("应用程序关闭")
        
        # 接受关闭事件
        event.accept() 
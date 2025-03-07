#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
自定义控件模块
"""

from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QSpinBox, QComboBox,
    QHBoxLayout, QVBoxLayout, QFormLayout, QGroupBox,
    QPushButton, QTextEdit, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

class LabeledInput(QWidget):
    """带标签的输入框控件"""
    
    def __init__(self, label_text, default_value="", parent=None):
        """初始化控件
        
        Args:
            label_text: 标签文本
            default_value: 默认值
            parent: 父控件
        """
        super().__init__(parent)
        
        # 创建布局
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建标签
        self.label = QLabel(label_text)
        self.label.setMinimumWidth(100)
        
        # 创建输入框
        self.input = QLineEdit(default_value)
        
        # 添加到布局
        layout.addWidget(self.label)
        layout.addWidget(self.input)
    
    def get_value(self):
        """获取输入值
        
        Returns:
            str: 输入值
        """
        return self.input.text()
    
    def set_value(self, value):
        """设置输入值
        
        Args:
            value: 输入值
        """
        self.input.setText(str(value))

class NumberInput(QWidget):
    """数字输入控件"""
    
    def __init__(self, label_text, default_value=0, min_value=0, max_value=10000, parent=None):
        """初始化控件
        
        Args:
            label_text: 标签文本
            default_value: 默认值
            min_value: 最小值
            max_value: 最大值
            parent: 父控件
        """
        super().__init__(parent)
        
        # 创建布局
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建标签
        self.label = QLabel(label_text)
        self.label.setMinimumWidth(100)
        
        # 创建输入框
        self.input = QSpinBox()
        self.input.setMinimum(min_value)
        self.input.setMaximum(max_value)
        self.input.setValue(default_value)
        
        # 添加到布局
        layout.addWidget(self.label)
        layout.addWidget(self.input)
    
    def get_value(self):
        """获取输入值
        
        Returns:
            int: 输入值
        """
        return self.input.value()
    
    def set_value(self, value):
        """设置输入值
        
        Args:
            value: 输入值
        """
        self.input.setValue(int(value))

class ScriptPreview(QWidget):
    """脚本预览控件"""
    
    def __init__(self, parent=None):
        """初始化控件
        
        Args:
            parent: 父控件
        """
        super().__init__(parent)
        
        # 创建布局
        layout = QVBoxLayout(self)
        
        # 创建标题
        title = QLabel("脚本预览")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 12, QFont.Bold))
        
        # 创建文本编辑器
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setFont(QFont("Courier New", 10))
        
        # 创建按钮布局
        button_layout = QHBoxLayout()
        
        # 创建复制按钮
        self.copy_button = QPushButton("复制到剪贴板")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        
        # 创建保存按钮
        self.save_button = QPushButton("保存到文件")
        self.save_button.clicked.connect(self.save_to_file)
        
        # 添加按钮到布局
        button_layout.addWidget(self.copy_button)
        button_layout.addWidget(self.save_button)
        
        # 添加控件到布局
        layout.addWidget(title)
        layout.addWidget(self.text_edit)
        layout.addLayout(button_layout)
    
    def set_text(self, text):
        """设置文本内容
        
        Args:
            text: 文本内容
        """
        self.text_edit.setPlainText(text)
    
    def get_text(self):
        """获取文本内容
        
        Returns:
            str: 文本内容
        """
        return self.text_edit.toPlainText()
    
    def copy_to_clipboard(self):
        """复制内容到剪贴板"""
        self.text_edit.selectAll()
        self.text_edit.copy()
        
        # 显示提示
        QMessageBox.information(self, "提示", "已复制到剪贴板")
    
    def save_to_file(self):
        """保存内容到文件"""
        # 获取保存路径
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存脚本", "", "文本文件 (*.txt);;所有文件 (*)"
        )
        
        if not file_path:
            return
        
        try:
            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.get_text())
            
            # 显示提示
            QMessageBox.information(self, "提示", f"已保存到文件: {file_path}")
        
        except Exception as e:
            # 显示错误
            QMessageBox.critical(self, "错误", f"保存失败: {str(e)}")

class ParameterForm(QGroupBox):
    """参数表单控件"""
    
    def __init__(self, title="参数设置", parent=None):
        """初始化控件
        
        Args:
            title: 分组框标题
            parent: 父控件
        """
        super().__init__(title, parent)
        
        # 创建布局
        self.form_layout = QFormLayout(self)
        
        # 创建输入控件
        self.inputs = {}
    
    def add_input(self, name, label, default_value=""):
        """添加输入控件
        
        Args:
            name: 控件名称
            label: 标签文本
            default_value: 默认值
        """
        input_widget = LabeledInput(label, default_value)
        self.form_layout.addRow(input_widget)
        self.inputs[name] = input_widget
    
    def add_number_input(self, name, label, default_value=0, min_value=0, max_value=10000):
        """添加数字输入控件
        
        Args:
            name: 控件名称
            label: 标签文本
            default_value: 默认值
            min_value: 最小值
            max_value: 最大值
        """
        input_widget = NumberInput(label, default_value, min_value, max_value)
        self.form_layout.addRow(input_widget)
        self.inputs[name] = input_widget
    
    def get_values(self):
        """获取所有输入值
        
        Returns:
            dict: 输入值字典
        """
        values = {}
        for name, widget in self.inputs.items():
            values[name] = widget.get_value()
        return values
    
    def set_values(self, values):
        """设置输入值
        
        Args:
            values: 输入值字典
        """
        for name, value in values.items():
            if name in self.inputs:
                self.inputs[name].set_value(value) 
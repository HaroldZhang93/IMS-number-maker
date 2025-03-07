#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
IMS号码生成器主程序入口
"""

import sys
from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow

def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setApplicationName("IMS号码生成器 by ZHN")
    
    # 创建并显示主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 
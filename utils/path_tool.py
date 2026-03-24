"""
为整个工程提供路径相关的工具函数
"""

import os

def get_project_root() -> str:
    """
    获取项目根目录的绝对路径
    """
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_abs_path(relative_path: str) -> str:
    """
    将相对路径转换为绝对路径
    :param relative_path: 相对于项目根目录的路径
    :return: 绝对路径
    """
    project_root = get_project_root()
    return os.path.join(project_root, relative_path)
"""
yaml
key: value
"""
import yaml
from utils.path_tool import get_abs_path

def load_rag_config(config_path: str=get_abs_path('config/rag.yml'),encoding: str='utf-8') -> dict:
    """
    加载RAG配置文件
    :param config_path: 配置文件的相对路径
    :return: 配置字典
    """
    with open(config_path, 'r', encoding=encoding) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config

def load_chroma_config(config_path: str=get_abs_path('config/chroma.yml'),encoding: str='utf-8') -> dict:
    """
    加载Chroma配置文件
    :param config_path: 配置文件的相对路径
    :return: 配置字典
    """
    with open(config_path, 'r', encoding=encoding) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config

def load_prompts_config(config_path: str=get_abs_path('config/prompts.yml'),encoding: str='utf-8') -> dict:
    """
    加载Prompts配置文件
    :param config_path: 配置文件的相对路径
    :return: 配置字典
    """
    with open(config_path, 'r', encoding=encoding) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config

def load_agent_config(config_path: str=get_abs_path('config/agent.yml'),encoding: str='utf-8') -> dict:
    """
    加载Agent配置文件
    :param config_path: 配置文件的相对路径
    :return: 配置字典
    """
    with open(config_path, 'r', encoding=encoding) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config

# 设置全局配置变量
rag_conf = load_rag_config()
chroma_conf = load_chroma_config()
prompts_conf = load_prompts_config()
agent_conf = load_agent_config()
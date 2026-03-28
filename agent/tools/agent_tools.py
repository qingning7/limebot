"""Agent tools definitions."""

from __future__ import annotations

import os
import random
from typing import Optional

from langchain_core.tools import tool

from rag.rag_service import RagSummarizeService
from utils.config_handler import agent_conf
from utils.logger_handler import logger
from utils.path_tool import get_abs_path


_rag_service: Optional[RagSummarizeService] = None
user_ids = ["1001", "1002", "1003", "1004", "1005", "1006"]
month_arr = ["2026-01", "2026-02", "2026-03"]
external_data: dict[str, dict[str, dict[str, str]]] = {}


def get_rag_service() -> RagSummarizeService:
    global _rag_service
    if _rag_service is None:
        _rag_service = RagSummarizeService()
    return _rag_service


@tool(description="从向量存储中检索参考资料")
def rag_summarize(query: str) -> str:
    return get_rag_service().rag_summarize(query)


@tool(description="获取指定城市天气")
def get_weather(city: str) -> str:
    return (
        f"城市{city}天气为晴天，气温26摄氏度，空气湿度50%，南风3级，"
        "最近3小时降雨概率极低"
    )


@tool(description="获取用户所在城市")
def get_user_location() -> str:
    return random.choice(["深圳", "合肥", "杭州"])


@tool(description="获取用户ID")
def get_user_id() -> str:
    return random.choice(user_ids)


@tool(description="获取当前月份")
def get_current_month() -> str:
    return random.choice(month_arr)


def generate_external_data():
    if not external_data:
        external_data_path = get_abs_path(agent_conf["external_data_path"])

        if not os.path.exists(external_data_path):
            raise FileNotFoundError(f"外部数据文件不存在: {external_data_path}")

        with open(external_data_path, "r", encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                arr: list[str] = line.strip().split(",")
                if len(arr) < 6:
                    continue

                user_id: str = arr[0].replace('"', "")
                feature: str = arr[1].replace('"', "")
                efficiency: str = arr[2].replace('"', "")
                consumables: str = arr[3].replace('"', "")
                comparison: str = arr[4].replace('"', "")
                time: str = arr[5].replace('"', "")

                if user_id not in external_data:
                    external_data[user_id] = {}

                external_data[user_id][time] = {
                    "特征": feature,
                    "效率": efficiency,
                    "耗材": consumables,
                    "对比": comparison,
                }


@tool(description="查询指定用户在指定月份的使用记录")
def fetch_external_data(user_id: str, month: str) -> str:
    generate_external_data()

    try:
        return str(external_data[user_id][month])
    except KeyError:
        logger.warning(f"[fetch_external_data]未找到 user_id={user_id}, month={month} 的记录")
        return ""


@tool(description="报告场景上下文注入工具")
def fill_context_for_report():
    return "fill_context_for_report已调用"

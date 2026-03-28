from typing import Callable

from langchain.agents.middleware import (
    AgentState,
    ModelRequest,
    before_model,
    dynamic_prompt,
    wrap_tool_call,
)
from langchain.tools.tool_node import ToolCallRequest
from langchain_core.messages import ToolMessage
from langgraph.runtime import Runtime
from langgraph.types import Command

from utils.logger_handler import logger
from utils.prompt_loader import load_report_prompts, load_system_prompts


@wrap_tool_call
def monitor_tool(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage | Command],
) -> ToolMessage | Command:
    logger.info(f"[tool monitor]tool={request.tool_call['name']}")
    logger.info(f"[tool monitor]args={request.tool_call['args']}")

    try:
        result = handler(request)
        logger.info(f"[tool monitor]tool={request.tool_call['name']} success")
        return result
    except Exception as exc:
        logger.info(f"tool={request.tool_call['name']} failed: {exc}")
        raise


@before_model
def log_before_model(
    state: AgentState,
    runtime: Runtime,
):
    logger.info(f"[log_before_model]messages_count={len(state['messages'])}")
    logger.debug(
        f"[log_before_model]{type(state['messages'][-1]).__name__} | {state['messages'][-1].content}"
    )
    return None


@dynamic_prompt
def report_prompt_switch(request: ModelRequest):
    is_report = request.runtime.context.get("report", False)
    if is_report:
        return load_report_prompts()

    return load_system_prompts()

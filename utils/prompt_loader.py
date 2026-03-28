from utils.config_handler import prompts_conf
from utils.path_tool import get_abs_path
from utils.logger_handler import logger


def _load_prompt(config_key: str, loader_name: str) -> str:
    prompt_relative_path = prompts_conf.get(config_key)
    if not prompt_relative_path:
        logger.error(f"[{loader_name}]missing config key: {config_key}")
        return ""

    prompt_abs_path = get_abs_path(prompt_relative_path)
    try:
        with open(prompt_abs_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as exc:
        logger.error(f"[{loader_name}]failed to read prompt: {exc}")
        return ""


def load_system_prompts() -> str:
    return _load_prompt("main_prompt_path", "load_system_prompts")


def load_rag_prompts() -> str:
    return _load_prompt("rag_summarize_prompt_path", "load_rag_prompts")


def load_report_prompts() -> str:
    return _load_prompt("report_prompt_path", "load_report_prompts")

"""Normalize zh|en and request-scoped locale."""
from __future__ import annotations

from contextvars import ContextVar

_locale: ContextVar[str] = ContextVar("atkbrain_locale", default="zh")
_report_lang: ContextVar[str] = ContextVar("atkbrain_report_lang", default="zh")


def normalize_locale(raw: object) -> str:
    s = str(raw or "").strip().lower().replace("_", "-")
    if s.startswith("en"):
        return "en"
    return "zh"


def set_locale(raw: object) -> str:
    lang = normalize_locale(raw)
    _locale.set(lang)
    return lang


def get_locale() -> str:
    return normalize_locale(_locale.get())


def set_report_lang(raw: object) -> str:
    lang = normalize_locale(raw)
    _report_lang.set(lang)
    return lang


def get_report_lang() -> str:
    return normalize_locale(_report_lang.get())


def config_output_lang(cfg: object) -> str:
    """猎面输出锁定中文。配置里的 en 不再生效。"""
    _ = cfg
    return "zh"


def locale_from_request(request) -> str:
    """界面语言锁定中文，不跟 Accept-Language 或 X-Locale 走。"""
    _ = request
    return "zh"

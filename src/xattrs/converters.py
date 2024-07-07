# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

import re

from xattrs.typing import CaseConvention, _ConverterType


def to_lower(value: str) -> str:
    return value.lower()


def to_upper(value: str) -> str:
    return value.upper()


def to_capital(value: str) -> str:
    return value.capitalize()


def to_camel(value: str) -> str:
    pascal = to_pascal(value)
    if len(pascal) <= 1:
        return pascal.lower()
    return pascal[0].lower() + pascal[1:]


def to_pascal(value: str) -> str:
    if "-" in value:
        value = value.replace("-", "_")

    expr = re.compile(r"(?:^|_)(.)")
    return expr.sub(lambda m: m.group(1).lower().title(), value)


def to_snake(value: str) -> str:
    if "-" in value:
        value = "".join(
            w.lower().capitalize() for w in value.replace("_", "-").split("-")
        )

    expr0 = re.compile(r"(.)([A-Z][a-z]+)")
    expr1 = re.compile(r"([a-z0-9])([A-Z])")
    repl = r"\1_\2"
    return expr1.sub(repl, expr0.sub(repl, value)).lower()


def to_kebab(value: str) -> str:
    return to_snake(value).replace("_", "-")


def to_secret(value: str, marker: str = "*", length: int | None = 6) -> str:
    length = int(length or len(value))
    return "".join(str(marker) for _ in range(length))


def to_const(value: str) -> str:
    return to_snake(value).upper()


_CASE_CONVERTER_MAPPING: dict[CaseConvention, _ConverterType] = {
    "lowercase": to_lower,
    "uppercase": to_upper,
    "UPPERCASE": to_upper,
    "capitalcase": to_capital,
    "Capitalcase": to_capital,
    "snake_case": to_snake,
    "camelCase": to_camel,
    "kebab-case": to_kebab,
    "CONST_CASE": to_upper,
    "PascalCase": to_pascal,
}

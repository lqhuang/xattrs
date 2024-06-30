from __future__ import annotations

META_PREFIX = "xattrs"


## Configuration

### Case Convention

LOWER_CASE = "lowercase"
UPPER_CASE = "uppercase"
CAPITALIZE = "capitalize"

PASCAL_CASE = "PascalCase"
CAMEL_CASE = "camelCase"

SNAKE_CASE = "snake_case"
CONST_CASE = "CONST_CASE"
ADA_CASE = "Ada_Case"

KEBAB_CASE = "kebab-case"
COBOL_CASE = "COBOL-CASE"
TRAIN_CASE = "Train-Case"

## Global specific configuration

deny_unknown_fields = "deny_unknown_fields"

### New type (as new type)
NEW_TYPE = "new_type"

## Field specific configuration

ALIAS = "alias"

SKIP = "skip"
SKIP_DE = "skip_de"
SKIP_SE = "skip_ser"
SKIP_IF = "skip_if"
SKIP_UNLESS = "skip_unless"
SKIP_IF_EMPTY = "skip_if_empty"


SER_NAME = "ser_alias"
DE_NAME = "de_alias"

"""
Duplicate of the original field, may be repeated to specify multiple aliases
"""
ALIASES = "aliases"

# SPDX-License-Identifier: BSD-3-Clause

from enum import Enum


class DeconstructStrategy(Enum):
    """`attrs`/`dataclass` classes deconstructing strategies."""

    AS_DICT = "as_dict"
    AS_TUPLE = "as_tuple"

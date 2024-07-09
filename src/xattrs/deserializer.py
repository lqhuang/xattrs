# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from xattrs._typing import T_interm, T_proto
from xattrs.base import BaseDeserializer


class Deserializer(BaseDeserializer[T_proto, T_interm]): ...

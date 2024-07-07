# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from xattrs.base import BaseDeserializer
from xattrs.typing import T_interm, T_proto


class Deserializer(BaseDeserializer[T_proto, T_interm]): ...

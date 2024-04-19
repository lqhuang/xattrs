# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from xattrs.base import BaseSerializer
from xattrs.typing import T_interm, T_proto


class Serializer(BaseSerializer[T_interm, T_proto]): ...

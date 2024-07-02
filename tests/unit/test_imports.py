# isort:skip_file
from xattrs import dataclass, define, frozen, field
from xattrs import asdict, astuple, astree
from xattrs import derive

from xattrs.preconf.json import (
    JsonDeserializer,
    JsonSerializer,
    default_json_deserializer,
)

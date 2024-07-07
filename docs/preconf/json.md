```python
import json


T = TypeVar('T')

@json_serde(
    encoder=Encoder,
    decoder=Decoder,
    json=json,
    generic=T,
    generic1=T1,
    generic2=T2,
    ....
)
@dataclass
class Model:
    a: int

    @codec
    def a(self) -> int:
        ...

    @override_decoder
    def a(self) -> int:
        ...

    @override_encoder
    def a(self) -> int:
        ...

m = Model()
m.to_json()
m = Model.from_json('{"a": 1, "b": 2}')
```

# Serialization and Deserialization

## Custom Serde

```python
from xattrs.attrs import define

@define
class ComplexStruct:
    a: int
    b: str
    c: float

    def __attrs_flatten__(self):
        return {
            'a': self.a,
            'b': self.b,
            'c': self.c,
        }

    @classmethod
    def __attrs_unflatten__(cls, data, spec):
        return cls(
            a=data['a'],
            b=data['b'],
            c=data['c'],
        )
```

```python
from xattrs.dataclasses import dataclass

@dataclass
class ComplexStruct:
    a: int
    b: str
    c: float

    def __attrs_flatten__(self):
        return {
            'a': self.a,
            'b': self.b,
            'c': self.c,
        }

    @classmethod
    def __attrs_unflatten__(cls, data, spec):
        return cls(
            a=data['a'],
            b=data['b'],
            c=data['c'],
        )
```

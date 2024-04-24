# Expected Behaviors

## Class variable would not be considered as a field

```
@dataclass
class Employee:
    # Field with no specifier
    name: str

    # Field that uses field specifier class instance
    age: Optional[int] = field(default=None, init=False)

    # Field with type annotation and simple initializer to
    # describe default value
    is_paid_hourly: bool = True

    # Not a field (but rather a class variable) because type
    # annotation is not provided.
    office_number = "unassigned"
```

- https://typing.readthedocs.io/en/latest/spec/dataclasses.html#the-dataclass-transform-decorator

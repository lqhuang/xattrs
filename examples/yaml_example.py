from __future__ import annotations

from attrs import define, field

from xattrs import asdict, serde
from xattrs.preconf.json import to_json
from xattrs.preconf.yaml import to_yaml


@serde(rename="kebab-case")
@define
class Person:
    first_name: str
    last_name: str
    age: int

    full_name: str = field(
        init=False, alias="full_name"
    )  # per field conf has higher priority

    def __attrs_post_init__(self):
        self.full_name = f"{self.first_name} {self.last_name}"


if __name__ == "__main__":
    data = {"first_name": "John", "last_name": "Lowe", "age": 25}
    person = Person(**data)
    print(person)
    # Person(first_name='John', last_name='Lowe', age=25, full_name='John Lowe')
    print(asdict(person))
    # {'first-name': 'John', 'last-name': 'Lowe', 'age': 25, 'full-name': 'John Lowe'}
    print(to_yaml(person))
    # age: 25
    # first-name: John
    # full-name: John Lowe
    # last-name: Lowe
    print(to_json(person))
    # {"first-name": "John", "last-name": "Lowe", "age": 25, "full-name": "John Lowe"}

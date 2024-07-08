from __future__ import annotations

from textwrap import dedent

from attrs import define, field

from xattrs import asdict, serde
from xattrs.preconf.yaml import to_yaml


def test_yaml__attrs_example():
    @serde(alias_converter="kebab-case")
    @define
    class Person:
        first_name: str
        last_name: str
        age: int

        full_name: str = field(init=False, alias="full_name")

        def __attrs_post_init__(self):
            self.full_name = f"{self.first_name} {self.last_name}"

    data = {"first_name": "John", "last_name": "Lowe", "age": 25}
    person = Person(**data)

    assert asdict(person) == {
        "first-name": "John",
        "last-name": "Lowe",
        "age": 25,
        "full-name": "John Lowe",
    }

    yaml_string = dedent(
        """
        age: 25
        first-name: John
        full-name: John Lowe
        last-name: Lowe
        """
    )
    assert to_yaml(person).strip() == yaml_string.strip()

from dataclasses import dataclass

from attrs import field, frozen

from xattrs import define, derive, field, serde
from xattrs.preconf.yaml import to_yaml


@serde(alias_converter="kebab-case")
@define
class Person:
    first_name: str
    last_name: str
    age: int

    full_name: str = field(
        init=False, alias="full_name"
    )  # per field conf has higher priority

    def __post_init__(self):
        self.full_name = f"{self.first_name} {self.last_name}"


# Decoding a Person object
person_obj = {"name": "John", "age": 25}
decoded_person = Person(**person_obj)
print(decoded_person)  # Output: Person(name='JOHN', age=25)

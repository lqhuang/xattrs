from dataclasses import dataclass

from xattrs import derive, frozen
from xattrs.preconf.json import default_json_serializer


@default_json_serializer
@frozen
class Person:
    name: str
    age: int


# Decoding a Person object
person_obj = {"name": "John", "age": 25}
decoded_person = Person(**person_obj)
print(decoded_person)  # Output: Person(name='JOHN', age=25)

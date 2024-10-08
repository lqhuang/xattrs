from __future__ import annotations

import json

from xattrs import frozen
from xattrs.preconf.json import to_json


def test_to_json():
    @frozen
    class Person:
        name: str
        age: int

    # Decoding a Person object
    obj = {"name": "John", "age": 25}
    person = Person(**obj)

    assert repr(person) == "Person(name='John', age=25)"

    assert to_json(person) == json.dumps(obj)

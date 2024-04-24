from dataclasses import dataclass

from attrs import asdict, frozen

from xattrs import derive, frozen

# Example usage


@derive(frozen)
class Person:
    name: str
    age: int


# Decoding a Person object
person_obj = {"name": "John", "age": 25}
decoded_person = Person(person_obj)
print(decoded_person)  # Output: Person(name='JOHN', age=25)

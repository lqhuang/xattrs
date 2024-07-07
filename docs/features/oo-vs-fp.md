# Choose your favorite programming paradigms without compromise

Do not argue about which programming paradigm is better anymore. Choose the one
that fits your problem and flavor best. Actually, for _entry level problems_,
they're simply equivalent. (Alright, It's always true for all cases, please
don't troll on this.)

```python
# Object-oriented programming
obj.func(arg1, arg2)

# Functional programming
func(obj, arg1, arg2)
```

It's about how you organize your code. OO and FP can be mixed together and work
well together.

```python
@derive(frozen, AsDict, FromJson, ToJson)
class User:
    name: str
    age: int


user = User('Alice', 25)
user.to_json()
# {'name': 'Alice', 'age': 25}

User.from_json("{'name': 'Bob', 'age': 30}")
# User('Bob', 30)

to_json(user)
# {'name': 'Alice', 'age': 25}

from_json(User, "{'name': 'Bob', 'age': 30}")
# User('Bob', 30)
```

`dataclasses` and `attrs` are two popular libraries in Python for defining
classes with attributes. They are similar in many ways, but they have different
APIs. One of the differences is that `dataclasses` has a built-in function
`asdict` to convert an instance of a dataclass to a dictionary, while `attrs`
does not have such a function. In this article, we will show you how to
implement `asdict` for `attrs` classes.

## `asdict` functions between `dataclasses` and `attrs`

Function signature of `asdict` in `dataclasses`:

```python
# Path: Lib/dataclasses.py
def asdict(obj, *, dict_factory=dict):
    """Return the fields of a dataclass instance as a new dictionary mapping
    field names to field values.
    """
    if not _is_dataclass_instance(obj):
        raise TypeError("asdict() should be called on dataclass instances")
    return _asdict_inner(obj, dict_factory)
```

Function signature of `asdict` in `attrs`:

```python
# Path: src/attr/_funcs.py
def asdict(
    inst,
    recurse=True,
    filter=None,
    dict_factory=dict,
    retain_collection_types=False,
    value_serializer=None,
):
    """
    Return the *attrs* attribute values of *inst* as a dict.

    Optionally recurse into other *attrs*-decorated classes.
    """
    ...
```

xattrs keep `value_serializer`

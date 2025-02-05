# xattrs

[![PyPI - Version](https://img.shields.io/pypi/v/xattrs.svg)](https://pypi.org/project/xattrs)

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/xattrs.svg)](https://pypi.org/project/xattrs)

---

`xattrs` is eXtensible toolkits of your `attrs` and `dataclasses` types with sensible default behaviors.

**Table of Contents**

- [Motivation](#motivation)
- [How to contribute](#how-to-contribute)
- [License](#license)

## Motivation

`pydantic` is a great library to validate and serialize data, but it's not designed to work with `attrs` or `dataclasses` as first class support.

`attrs` is a great library to define classes with declarative and immutable data, but it's not designed to serialize or deserialize instances directly and validate data value by given schema.

`attrs` incubated `dataclasses` define classes without boilerplate in a standard library way. And as a third-party library

> ...
>
> - Data Classes are _intentionally_ less powerful than attrs.
> - ...
> - `dataclasses` can and will be more conservative. We are not bound to any release schedules and we have a clear deprecation policy.
>
> ...
>
> - [attrs Documentaion - Why not ...](https://www.attrs.org/en/stable/why.html)

As I understand, `attrs` is more powerful and flexible, and has better situation than `dataclass` to develop and test bleeding-edge ideas and unstable features. And finally, these could also feedback to `dataclass`.

Unfortunately, while `attrs` itself is widely adopted, its ecosystem is not as prosperous as `pydantic`'s. Very few libraries are designed to enrich validators, filters or converters for attrs. `cattrs` attempted to do so, but it hasn't gained the popularity that was expected.

So `xattrs` is here born to fill the gap between `attrs` and `pydantic`, and (try) to provide a better way to work with `attrs` and `dataclasses` in a more elegant and powerful way.

> [!WARNING]
>
> `xattrs` is still in early stage of development. Please use it with caution and give feedback to help us to improve it. Thanks!
>
> Try `pydantic` first if you're looking for a mature and stable solution.

## Architecture

`xattrs` has layered architecture, which is designed to be extensible and customizable.

- `xattrs` is the fundamental layer, which provides the core functionalities to serialize and deserialize instances of `attrs` and `dataclasses` types.
  - Just use it as `attrs-serde` or `dataclass-serde`.
- `xattrs.schema` is the schema layer, which provides the schema functionalities to validate annotated schema for instances of `attrs` and `dataclasses`.
  - If you're familar with `pydantic`, you could consider it as a better (?) `TypeAdapter` for `attrs` and `dataclass`.
  - If you're familar with `zod` (TypeScript), its API is inspired from `zod`.
  - Try to `import xattrs.schema as xs` and see what you could do with it.

## Project scope

Let dataclasses or attrs just store declaretive and immutable 'data'.

Goals:

- Easy to use, easy to extend, easy to customize.
- Extending upstream project as more as its recommended ways, see also [`attrs` Extending](https://www.attrs.org/en/stable/extending.html).
- Elegant and powerful API for (de)serialization and schema validation

<!-- Non-goals: -->

## Installation

```console
pip install xattrs
```

## How to contribute

The first and the best way to contribute to `xattrs` is to use it in your project and give feedback on your experience about it both good and bad. You could participate our community by submitting [issues](https://github.com/lqhuang/xattrs/issues) or even [pull requests](https://github.com/lqhuang/xattrs/pulls), not limited to bugs, but also proposals, documentation, use cases and best practices.

Then you could also try to help us to improve the project by promoting it to your teams, writing blog posts, or even giving a talk in your local community.

If you have did all above, but still thought you could do more. Consider to sponsor the project for long-term maintenance and development.

The most important thing is the community, and we are looking forward to how people enjoy using `xattrs` and how it could help them to solve their problems.

## Development Guide

### Major upstream dependencies

- `attrs`
- `dataclasses`
- `annotated`

## License

`xattrs` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

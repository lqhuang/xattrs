# xattrs

[![PyPI - Version](https://img.shields.io/pypi/v/xattrs.svg)](https://pypi.org/project/xattrs)

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/xattrs.svg)](https://pypi.org/project/xattrs)

---

Serialize and deserialize instances of your `attrs` and `dataclasses` types with implicit or customized encoding.

🚧 **WIP**

**Table of Contents**

- [Installation](#installation)
- [How to contribute](#how-to-contribute)
- [License](#license)

## Introduction

<!-- "correct by construction" instead of "correct by validation" / "correct by schema" -->

## Project orient

Let dataclasses or attrs just store declaretive and immutable 'data'.

Goals:

- Easy to use, easy to extend, easy to customize.
- Extending upstream project as more as its recommended ways, see also [`attrs` Extending](https://www.attrs.org/en/stable/extending.html).

Non-goals:

## Installation

```console
pip install xattrs
```

## How to contribute

The first and the best way to contribute to `xattrs` is to use it in your project and give feedback on your experience about it both good and bad. You could participate our community by submitting [issues]() or even pull requests, not limited to bugs, but also proposals, documentation, use cases and best practices.

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

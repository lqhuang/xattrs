# Introduction

## Overview of `xattrs` Project

`xattrs` is a serialization and deserialization framework of ADT (Algebraic Data
Types) classes for Python.

Think of `xattrs` as a tool to convert your ADT classes into a general format
that can be stored, transferred, and shared among applications, threads, network
and more.

## Goals

aimed at multiplying developers productivity

1. Convention-over-Configuration
2. sensible defaults
3. opinionated APis.
4. Efficient (probably not most performant but good enough)

## Features

- Support `attrs`, `dataclasses` and `dataclass_transform`
- Batteries included support for common types and protocols
- Highly extensible customization to fit your demands
- Automatic case name transformation (`camelCase`, `snake_case`, `kebab-case`)
- Optional schema validation and conversion
- Flexible configuration with sensible defaults
- Pythonic and typed API design with uncompromising performance

## Why `xattrs`?

## Inpsired from

- [attrs](https://www.attrs.org/en/stable/)
- [Python 3 Documentation `dataclasses`](https://docs.python.org/3/library/dataclasses.html)
- [PEP 681 – Data Class Transforms](https://peps.python.org/pep-0681/)
- [pydantic v2](https://docs.pydantic.dev/)
- [rust - serde](https://serde.rs/)
- ADT from Functioanl programming languages

## Why not?

### Why not `pydantic`

### Why not `cattrs`

`cattrs` is a great library for converting complex data structures to and from,
but it's limited to hook-style customization and not as flexible as `xattrs`

### Why not `msgspec`

## Roadmap

- Support more types and protocols
- Continuously profiling to improve the performance and stability of the library
- Benchmarking versions through time

## Eco systems

- more schema validation fields
  - xattrs-schema
  - annoted
- more serialization formats and protocols
  - xattrs-protobuf
  - xattrs-avro
  - xattrs-thrift
  - xattrs-jax
- command line tool: Declarative CLIs with argparse and xattrs
  - typed-argparse
  - https://github.com/mpkocher/pydantic-cli
  - click
  - fire
- testing
  - [bloomberg/attrs-strict](https://github.com/bloomberg/attrs-strict):
    Provides runtime validation of attributes specified in Python 'attr'-based
    data classes.
  - xattrs-fuzztypes
- Example usage for Large Language Model (LLM)
  - xattrs-llm
- Misc
  - [koxudaxi/datamodel-code-generator](https://github.com/koxudaxi/datamodel-code-generator):
    Pydantic model and dataclasses.dataclass generator for easy conversion of
    JSON, OpenAPI, JSON Schema, and YAML data sources.
    <https://koxudaxi.github.io/datamodel-code-generator/>

We hope more people can contribute to the project and make it better. including
small things like fixing typos, adding comments, or improving the documentation.

## Audit and Security

Try to make the library adapt without 顾虑 as possible by leading audit and
security enhencements.

We are committed to providing a secure and transparent software supply chain.

- Security
  - Signed releases
  - Security advisories
  - Reproducible Builds (https://reproducible-builds.org/)
  - Security policy
  - sigstore

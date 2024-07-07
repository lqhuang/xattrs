# Seperate Data and Operations

Best practices for multi-threading / multi-processing in transformers

- Immutable data (dataclasses, tuples, etc) to avoid race conditions. Probably
  still not thread safe, but it reduces your mind burden.
- Operations for data coulde stateful and thread-unsafe, they only assume work
  well on single thread

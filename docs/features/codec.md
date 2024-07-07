# Codec

## Introduction

The codec is a component that is responsible for encoding and decoding messages.
It is used by the transport layer to encode and decode messages. The codec is
also used by the serialization layer to encode and decode messages.

## Examples

### Encoding and decoding messages

```python
class Decoder:
    def decode(self, data: bytes) -> Message:
        return Message(data)

class Encoder:
    def encode(self, message: Message) -> bytes:
        return message.payload

class Codec(Decoder, Encoder):
    ...
```

### Encoding and decoding messages with a serializer

```python
class Decoder:
    def decode(self, data: bytes) -> Message:
        return Message(data)

class Encoder:
    def encode(self, message: Message) -> bytes:
        return message.payload

class Serializer:
    def serialize(self, message: Message) -> bytes:
        return message.payload

    def deserialize(self, data: bytes) -> Message:
        return Message(data)

class Codec(Decoder, Encoder):
    def __init__(self, serializer: Serializer):
        self.serializer = serializer

    def decode(self, data: bytes) -> Message:
        return self.serializer.deserialize(data)

    def encode(self, message: Message) -> bytes:
        return self.serializer.serialize(message)
```

from typing import Any, Callable, TypeVar

from dataclasses import dataclass

T = TypeVar("T")


def decoder(decoder_func: Callable[[Any], T]) -> Callable[[Any], T]:
    def decorator(cls: T) -> T:
        def decode(obj: Any) -> T:
            # Perform decoding logic here
            # You can use the decoder_func to transform the obj to the desired format
            # For example:
            decoded_obj = decoder_func(obj)
            return cls(**decoded_obj)

        cls.decode = staticmethod(decode)
        return cls

    return decorator

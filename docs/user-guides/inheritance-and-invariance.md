# Inheritance and Class Variance

Inheritance is a fundamental concept in object-oriented programming. It allows
you to define a new class based on an existing class. The new class inherits the
properties and methods of the existing class, and can also add new properties
and methods or override existing ones.

## Inheritance

```py
class Animal:
    ...

class Dog(Animal):
    ...

class Cat(Animal):
    ...
```

In this example, `Dog` and `Cat` are subclasses of `Animal`. They inherit all
...

## References

- [Covariance, Contravariance, and Invariance — The Ultimate Python Guide](https://blog.daftcode.pl/covariance-contravariance-and-invariance-the-ultimate-python-guide-8fabc0c24278)

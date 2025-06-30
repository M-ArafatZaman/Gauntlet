# Gauntlet
A dependency injection framework in python.

# Dependency Injection

## What is Dependency Injection?
Dependency injection is a design pattern where objects _(let's call it a component)_ are provided (injected) with the instances of objects _(its' dependencies)_ it needs instead of the object _(the component)_ instantiating the objects _(dependencies)_ itself.
While it sounds like a highly complicated design pattern, truthfully, it can all be summarized with the following example.

**Before DI**
```python
class Engine:
    def __init__(self):
        ...

class Car:
    def __init__(self):
        self.engine = Engine() # The class `Car` has a dependency on `Engine`
```

**After DI**
```python
class Engine:
    # Remains same ...

class Car:
    def __init__(self, engine: Engine): # `Engine` is injected on the constructor
        self.engine = engine

car = Car(engine = Engine()) # Here we instantiate the Engine and provide it to the car
```
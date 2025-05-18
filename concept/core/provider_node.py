from typing import List, Callable, TypeVar, Tuple
from dataclasses import dataclass
from .dependency_node import DependencyNode

T = TypeVar('T')

@dataclass
class ProviderNode:
    """A node in a dependency injection graph that describes how to provision an instance of type `T`.

    This class serves as a registry entry for dependency injection systems, linking:
    - A type to be provided
    - A factory function that creates instances
    - Dependencies required for construction

    Attributes:
        name: A human-readable identifier for this provider.
        type: The class/type being provided (generic type `T`).
        provider_fn: Factory function that returns instances of `T`.
        dependencies: List of dependencies required by the factory function.

    Example:
        >>> def create_engine(config: Config) -> Engine:
        ...     return Engine(config)
        >>> provider = ProviderNode(
        ...     name="Engine",
        ...     type=Engine,
        ...     provider_fn=create_engine,
        ...     dependencies=[DependencyNode(type=Config, ...)]
        ... )
    """
    name: str
    type: T
    provider_fn: Callable[..., T]
    dependencies: List[DependencyNode]


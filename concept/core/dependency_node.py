from dataclasses import dataclass
from typing import TypeVar

T = TypeVar('T')

@dataclass
class DependencyNode:
    """A node representing a dependency required by a provider in a DI system.

    This class encapsulates metadata about a single dependency needed to construct
    another object, including both type information and contextual naming.

    Attributes:
        type: The class/type of the dependency (generic type `T`).
        name: Human-readable identifier for the dependency (typically the type name).
        parameter_name: The argument name where this dependency will be injected.

    Example:
        >>> node = DependencyNode(
        ...     type=DatabaseConnection,
        ...     name="DatabaseConnection",
        ...     parameter_name="db_conn"
        ... )
        >>> node.type
        <class 'DatabaseConnection'>
    """
    type: T
    name: str
    parameter_name: str
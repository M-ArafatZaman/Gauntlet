import inspect
from typing import List
from core import DependencyNode, ProviderNode

class Provides:
    """A class decorator that registers a provider function in the Gauntlet dependency injection system.

    This decorator analyzes the annotated function signature to:
    1. Validate return and parameter type hints
    2. Build a dependency tree of required components
    3. Register the provider in the owner class's provider registry

    Attributes:
        fn (Callable): The decorated provider function.
        signature (inspect.Signature): Parsed function signature.
    """
     
    def __init__(self, fn):
        """Initializes the decorator with the provider function.

        Args:
            fn: The function to be registered as a provider.
        """
        self.fn = fn

    def __set_name__(self, owner, name):
        """Hook called when the decorated function is assigned to a class.

        Performs signature validation and dependency tree construction before
        attaching the function to the owner class.

        Args:
            owner: The class that owns this provider.
            name: The attribute name under which the function is stored.
        """
        self.signature = inspect.signature(self.fn)
        self.validate_signature()
        self.build_dependency_tree(owner)
        setattr(owner, name, self.fn)

    def build_dependency_tree(self, owner):
        """Constructs and registers the provider's dependency graph.

        Args:
            owner: The class that will contain the provider registration.
        """
        return_type = self.get_return_type()
        dependencies = self.get_dependencies()
        owner.providers[return_type] = ProviderNode(
            name = return_type.__name__,
            type = return_type,
            provider_fn = self.fn,
            dependencies = dependencies,
        )

    def get_return_type(self):
        """Extracts the provider's return type annotation.

        Returns:
            The type that this provider constructs.
        """
        return self.signature.return_annotation
    
    def get_dependencies(self) -> List[DependencyNode]:
        """Generates dependency nodes for all required parameters.

        Returns:
            A list of DependencyNode objects representing each parameter
            (excluding 'self') that the provider requires.

        Example:
            For a provider `fn(db: Database, cache: Redis)`, returns:
            [DependencyNode(Database), DependencyNode(Redis)]
        """
        return [
            DependencyNode(
                type=param.annotation,
                name=param.annotation.__name__,
                parameter_name=param_name,
            )
            for param_name, param in self.signature.parameters.items()
            if param_name != 'self'
        ]

    def validate_signature(self):
        """Validates the provider function's type annotations.

        Raises:
            Exception: If return type or parameter annotations are missing.
        """
        self.validate_return_type()
        self.validate_parameters()

    def validate_return_type(self):
        """Ensures the provider has a return type annotation.

        Raises:
            Exception: If return type annotation is missing.
        """
        return_type = self.signature.return_annotation
        if return_type == inspect._empty:
            raise Exception(
                f"Provider '{self.fn.__name__}' must be annotated with a return type."
            )        

    def validate_parameters(self):
        """Verifies all parameters (except self) have type annotations.

        Raises:
            Exception: If any parameter lacks type annotation.
        """
        for param_name, param in self.signature.parameters.items():
            if param_name == 'self':
                continue
            if param.annotation == inspect._empty:
                raise Exception(
                    f"Parameter '{param_name}' for provider '{self.fn.__name__}' "
                    "must be annotated with a type."
                )


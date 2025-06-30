from abc import ABC
from typing import TypeVar, Type, Dict, Any
from .provider_node import ProviderNode

T = TypeVar("T")

class Provider(ABC):
    """Abstract base class for dependency injection providers.
    
    Maintains a registry of providers and handles dependency resolution through
    recursive injection. Subclasses define concrete providers using the `@Provides` decorator.

    Class Attributes:
        providers: Dictionary mapping types to their ProviderNode configurations.

    Example:
        class CarModule(Provider):
            @Provides
            def provide_engine(self) -> Engine:
                return Engine()

            @Provides
            def provide_car(self, engine: Engine) -> Car:
                return Car(engine)
    """
    providers: Dict[T, ProviderNode] = {}

    def get(self, clazz: Type[T]) -> T:
        """Retrieves an instance of the requested class with all dependencies resolved.
        
        Args:
            clazz: The class type to instantiate (e.g., EngineDao).
            
        Returns:
            A fully constructed instance of the requested type with all dependencies injected.
            
        Raises:
            Exception: If no provider exists for the requested type.
            
        Example:
            >>> module = CarModule()
            >>> car = module.get(Car)  # Auto-injects Engine dependency
        """
        if clazz not in self.providers:
            raise Exception(f"No provider exists for '{clazz.__name__}'.")

        dependency_mp = self.resolve_dependencies(clazz)
        return self.providers[clazz].provider_fn(self, **dependency_mp)
    
    def resolve_dependencies(self, clazz: Type[T]) -> Dict[str, Any]:
        """Recursively resolves all dependencies for a given class.
        
        Args:
            clazz: The class whose dependencies should be resolved.
            
        Returns:
            Dictionary mapping parameter names to resolved instances.
            
        Note:
            Performs depth-first resolution and will detect circular dependencies.
        """
        dependency_mp = {}
        for dependency in self.providers[clazz].dependencies:
            dependency_mp[dependency.parameter_name] = self.get(dependency.type)
        return dependency_mp

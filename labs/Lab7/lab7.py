from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar

T = TypeVar("T")


class LifeStyle(Enum):
	PER_REQUEST = "per_request"
	SCOPED = "scoped"
	SINGLETON = "singleton"


# region interfaces

class ILogger(ABC):
	@abstractmethod
	def log(self, message: str) -> None:
		pass


class IDatabase(ABC):
	@abstractmethod
	def connect(self) -> None:
		pass

	@abstractmethod
	def execute(self, query: str) -> None:
		pass


class IEmailService(ABC):
	@abstractmethod
	def send(self, to: str, subject: str) -> None:
		pass

# endregion


# region classes

class ConsoleLogger(ILogger):
	def __init__(self, prefix: str = "INFO"):
		self.prefix: str = prefix

	def log(self, message: str) -> None:
		print(f"[{self.prefix}] {message}")


class FileLogger(ILogger):
	def __init__(self, filename: str = "app.log"):
		self.filename: str = filename

	def log(self, message: str) -> None:
		with open(self.filename, "a") as f:
			f.write(f"{message}\n")


class SQLiteDatabase(IDatabase):
	def __init__(self, connection_string: str, logger: ILogger):
		self.connection_string: str = connection_string
		self.logger: ILogger = logger

	def connect(self) -> None:
		self.logger.log(f"Connecting to SQLite: {self.connection_string}")

	def execute(self, query: str) -> None:
		self.logger.log(f"Executing query: {query}")


class PostgresDatabase(IDatabase):
	def __init__(self, host: str, port: int, logger: ILogger):
		self.host: str = host
		self.port: int = port
		self.logger: ILogger = logger

	def connect(self) -> None:
		self.logger.log(f"Connecting to PostgreSQL: {self.host}:{self.port}")

	def execute(self, query: str) -> None:
		self.logger.log(f"Executing query: {query}")


class MockEmailService(IEmailService):
	def __init__(self, logger: ILogger):
		self.logger: ILogger = logger
		self.sent_emails: List[Dict[str, str]] = []

	def send(self, to: str, subject: str) -> None:
		self.logger.log(f"Send mail for {to}: {subject}")
		self.sent_emails.append({"to": to, "subject": subject})


class RealEmailService(IEmailService):
	def __init__(self, smtp_server: str, logger: ILogger):
		self.smtp_server: str = smtp_server
		self.logger: ILogger = logger

	def send(self, to: str, subject: str) -> None:
		self.logger.log(f"[RealES] Sending via {self.smtp_server} for {to}: {subject}")

# endregion


# region devided Injector

class DependencyRegistry:
	def __init__(self):
		self.registry: Dict[Any, Dict[str, Any]] = {}

	def register(
		self,
		interface: Type[Any],
		implementation: Optional[Type[Any]] = None,
		lifestyle: LifeStyle = LifeStyle.PER_REQUEST,
		factory: Optional[Callable[[], Any]] = None,
		**params: Any
	) -> None:

		if implementation is None and factory is None:
			raise ValueError("Need implementation or factory")

		self.registry[interface] = {
			"implementation": implementation,
			"factory": factory,
			"lifestyle": lifestyle,
			"params": params,
		}

	def get(self, interface: Type[Any]) -> Dict[str, Any]:
		if interface not in self.registry:
			raise ValueError(f"Not registered: {interface}")
		return self.registry[interface]


class ScopeManager:
	def __init__(self):
		self.scopes: List[Dict[Any, Any]] = []
		self.singletons: Dict[Any, Any] = {}

	def push_scope(self) -> None:
		self.scopes.append({})

	def pop_scope(self) -> None:
		self.scopes.pop()

	def get_current_scope(self) -> Dict[Any, Any]:
		if not self.scopes:
			raise RuntimeError("No active scope")
		return self.scopes[-1]

	def get_singleton(self, key: Any, creator: Callable[[], Any]) -> Any:
		if key not in self.singletons:
			self.singletons[key] = creator()
		return self.singletons[key]

	def get_scoped(self, key: Any, creator: Callable[[], Any]) -> Any:
		scope = self.get_current_scope()
		if key not in scope:
			scope[key] = creator()
		return scope[key]


class InstanceFactory:
	def __init__(self, registry: DependencyRegistry, scopes: ScopeManager):
		self.registry: DependencyRegistry = registry
		self.scopes: ScopeManager = scopes

	def resolve(self, interface: Type[T]) -> T:
		conf = self.registry.get(interface)
		impl: Optional[Type[Any]] = conf["implementation"]
		factory: Optional[Callable[[], Any]] = conf["factory"]
		life: LifeStyle = conf["lifestyle"]
		params: Dict[str, Any] = conf["params"]

		if factory:
			return factory()

		if impl is None:
			raise ValueError(f"No implementation for {interface}")

		if life == LifeStyle.SINGLETON:
			return self.scopes.get_singleton(
				interface, lambda: self._create(impl, params)
			)

		if life == LifeStyle.SCOPED:
			return self.scopes.get_scoped(
				interface, lambda: self._create(impl, params)
			)

		return self._create(impl, params)

	def _create(self, implementation: Type[Any], extra_params: Dict[str, Any]) -> Any:
		import inspect

		constructor_params: Dict[str, Any] = {}
		signature = inspect.signature(implementation.__init__)

		for name, param in list(signature.parameters.items())[1:]:
			if name in extra_params:
				constructor_params[name] = extra_params[name]
			else:
				ann = param.annotation
				if inspect.isclass(ann) and issubclass(ann, ABC):
					constructor_params[name] = self.resolve(ann)

		return implementation(**constructor_params)


class Injector:
	def __init__(self):
		self.registry: DependencyRegistry = DependencyRegistry()
		self.scopes: ScopeManager = ScopeManager()
		self.factory: InstanceFactory = InstanceFactory(self.registry, self.scopes)

	def register(self, *args: Any, **kwargs: Any) -> None:
		self.registry.register(*args, **kwargs)

	def get_instance(self, interface: Type[T]) -> T:
		return self.factory.resolve(interface)

	def __enter__(self) -> "Injector":
		self.scopes.push_scope()
		return self

	def __exit__(self, exc_type, exc_val, exc_tb) -> None:
		self.scopes.pop_scope()

# endregion

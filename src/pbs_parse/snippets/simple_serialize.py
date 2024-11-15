from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Generator, Generic, Iterable, Protocol, TypeVar
from json import dump as json_dump
from json import load as json_load
from dataclasses import asdict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _typeshed import DataclassInstance

try:
    from yaml import safe_load, safe_dump

    YAML = True
except ModuleNotFoundError:
    YAML = False


T = TypeVar("T")
E = TypeVar("E")
F = TypeVar("F", bound=DataclassInstance)
G = TypeVar("G", bound=Dict[str, Any])


class SimpleConverter(Protocol[T, E]):
    @staticmethod
    def to_simple(obj: T) -> E: ...
    @staticmethod
    def from_simple(obj: E, new_obj: T) -> T: ...
    @staticmethod
    def from_simple_gen(obj: Iterable[E], new_obj: T) -> Generator[T, None, None]: ...
    @staticmethod
    def to_simple_gen(obj: Iterable[T]) -> Generator[E, None, None]: ...


class SimpleSerializer(Protocol[T]):
    @staticmethod
    def save_json(path_out: Path, obj: T): ...
    @staticmethod
    def load_json(path_in: Path, new_obj: T) -> T: ...
    @staticmethod
    def save_yaml(path_out: Path, obj: T): ...
    @staticmethod
    def load_yaml(path_in: Path, new_obj: T) -> T: ...


class SimpleSerializerABC(ABC, Generic[T, E]):
    @classmethod
    @abstractmethod
    def to_simple(cls, obj: T) -> E: ...
    @classmethod
    @abstractmethod
    def from_simple(cls, obj: E, new_obj: T) -> T: ...
    @classmethod
    def from_simple_gen(cls, obj: Iterable[E], new_obj: T) -> Generator[T, None, None]:
        for item in obj:
            yield cls.from_simple(item, new_obj)

    @classmethod
    def to_simple_gen(cls, obj: Iterable[T]) -> Generator[E, None, None]:
        for item in obj:
            yield cls.to_simple(item)

    @classmethod
    def save_json(
        cls, path_out: Path, obj: T, indent: int = 1, overwrite: bool = False
    ):
        check_file(path_out=path_out, overwrite=overwrite)
        path_out.parent.mkdir(exist_ok=True, parents=True)
        with open(path_out, "w") as file:
            json_dump(obj=obj, fp=file, default=cls.to_simple, indent=indent)

    @classmethod
    def load_json(cls, path_in: Path, new_obj: T) -> T:
        with open(path_in, "r") as file:
            return cls.from_simple(json_load(file), new_obj)

    @classmethod
    def save_yaml(
        cls, path_out: Path, obj: T, indent: int = 1, overwrite: bool = False
    ):
        if not YAML:
            raise ValueError("PyYaml not found.")
        check_file(path_out=path_out, overwrite=overwrite)
        path_out.parent.mkdir(exist_ok=True, parents=True)
        with open(path_out, "w") as file:
            safe_dump(data=cls.to_simple(obj), stream=file, indent=indent)

    @classmethod
    def load_yaml(cls, path_in: Path, new_obj: T) -> T:
        if not YAML:
            raise ValueError("PyYaml not found.")
        with open(path_in, "r") as file:
            return cls.from_simple(safe_load(file), new_obj)


def check_file(path_out: Path, overwrite: bool = False) -> bool:
    if path_out.exists():
        if path_out.is_dir():
            raise ValueError(f"Output path exists and it is a directory. {path_out}")
        if path_out.is_file():
            if not overwrite:
                raise ValueError(
                    f"Output path exists and overwrite is false. {path_out}"
                )
    return True


class DataclassSerializer(SimpleSerializerABC[F, G]):
    @classmethod
    def to_simple(cls, obj: F) -> G:
        return asdict(obj)  # type: ignore

    @classmethod
    def from_simple(cls, obj: G, new_obj: F) -> F:
        return new_obj(**obj)  # type: ignore

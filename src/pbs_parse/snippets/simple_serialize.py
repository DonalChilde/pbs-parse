from abc import ABC, abstractmethod
from pathlib import Path
from typing import (
    Generator,
    Generic,
    Iterable,
    Protocol,
    Type,
    TypeVar,
)
from json import dump as json_dump
from json import load as json_load
from dataclasses import asdict


try:
    from yaml import safe_load, safe_dump

    YAML = True
except ModuleNotFoundError:
    YAML = False


COMPLEX_OBJ = TypeVar("COMPLEX_OBJ")
SIMPLE_OBJ = TypeVar("SIMPLE_OBJ")


class SimpleConverter(Protocol[COMPLEX_OBJ, SIMPLE_OBJ]):
    @staticmethod
    def to_simple(complex_obj: COMPLEX_OBJ) -> SIMPLE_OBJ: ...
    @staticmethod
    def from_simple(
        simple_obj: SIMPLE_OBJ, complex_obj: Type[COMPLEX_OBJ]
    ) -> COMPLEX_OBJ: ...
    @staticmethod
    def from_simple_gen(
        simple_objs: Iterable[SIMPLE_OBJ], complex_obj: Type[COMPLEX_OBJ]
    ) -> Generator[COMPLEX_OBJ, None, None]: ...
    @staticmethod
    def to_simple_gen(
        complex_objs: Iterable[COMPLEX_OBJ],
    ) -> Generator[SIMPLE_OBJ, None, None]: ...


class SimpleSerializer(Protocol[COMPLEX_OBJ]):
    @staticmethod
    def save_json(path_out: Path, complex_obj: COMPLEX_OBJ): ...
    @staticmethod
    def load_json(path_in: Path, complex_obj: Type[COMPLEX_OBJ]) -> COMPLEX_OBJ: ...
    @staticmethod
    def save_yaml(path_out: Path, complex_obj: COMPLEX_OBJ): ...
    @staticmethod
    def load_yaml(path_in: Path, complex_obj: Type[COMPLEX_OBJ]) -> COMPLEX_OBJ: ...


class SimpleSerializerABC(ABC, Generic[COMPLEX_OBJ, SIMPLE_OBJ]):
    @classmethod
    @abstractmethod
    def to_simple(cls, complex_obj: COMPLEX_OBJ) -> SIMPLE_OBJ:
        pass

    @classmethod
    @abstractmethod
    def from_simple(
        cls, obj: SIMPLE_OBJ, complex_obj: Type[COMPLEX_OBJ]
    ) -> COMPLEX_OBJ:
        pass

    @classmethod
    def from_simple_gen(
        cls, simple_objs: Iterable[SIMPLE_OBJ], complex_obj: Type[COMPLEX_OBJ]
    ) -> Generator[COMPLEX_OBJ, None, None]:
        for item in simple_objs:
            yield cls.from_simple(item, complex_obj)

    @classmethod
    def to_simple_gen(
        cls, complex_obj: Iterable[COMPLEX_OBJ]
    ) -> Generator[SIMPLE_OBJ, None, None]:
        for item in complex_obj:
            yield cls.to_simple(item)

    @classmethod
    def save_json(
        cls,
        path_out: Path,
        complex_obj: COMPLEX_OBJ,
        indent: int = 1,
        overwrite: bool = False,
    ):
        check_file(path_out=path_out, overwrite=overwrite)
        path_out.parent.mkdir(exist_ok=True, parents=True)
        with open(path_out, "w") as file:
            json_dump(obj=complex_obj, fp=file, default=cls.to_simple, indent=indent)

    @classmethod
    def load_json(cls, path_in: Path, complex_obj: Type[COMPLEX_OBJ]) -> COMPLEX_OBJ:
        with open(path_in, "r") as file:
            return cls.from_simple(json_load(file), complex_obj)

    @classmethod
    def save_yaml(
        cls,
        path_out: Path,
        complex_obj: COMPLEX_OBJ,
        indent: int = 1,
        overwrite: bool = False,
    ):
        if not YAML:
            raise ValueError("PyYaml not found.")
        check_file(path_out=path_out, overwrite=overwrite)
        path_out.parent.mkdir(exist_ok=True, parents=True)
        with open(path_out, "w") as file:
            safe_dump(data=cls.to_simple(complex_obj), stream=file, indent=indent)

    @classmethod
    def load_yaml(cls, path_in: Path, complex_obj: Type[COMPLEX_OBJ]) -> COMPLEX_OBJ:
        if not YAML:
            raise ValueError("PyYaml not found.")
        with open(path_in, "r") as file:
            return cls.from_simple(safe_load(file), complex_obj)


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


class DataclassSerializer(SimpleSerializerABC[COMPLEX_OBJ, SIMPLE_OBJ]):
    @classmethod
    def to_simple(cls, complex_obj: COMPLEX_OBJ) -> SIMPLE_OBJ:
        return asdict(complex_obj)  # type: ignore

    @classmethod
    def from_simple(
        cls, simple_obj: SIMPLE_OBJ, complex_obj: Type[COMPLEX_OBJ]
    ) -> COMPLEX_OBJ:
        return complex_obj(**simple_obj)  # type: ignore

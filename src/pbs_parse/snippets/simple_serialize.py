from abc import ABC, abstractmethod
from pathlib import Path
from typing import (
    Callable,
    Generator,
    Generic,
    Iterable,
    Optional,
    Protocol,
    Type,
    TypeVar,
)
from json import dump as json_dump
from json import load as json_load
from dataclasses import asdict, is_dataclass


try:
    from yaml import safe_load, safe_dump

    YAML = True
except ModuleNotFoundError:
    YAML = False


COMPLEX_OBJ = TypeVar("COMPLEX_OBJ")
SIMPLE_OBJ = TypeVar("SIMPLE_OBJ")


class SimpleConverter(Protocol[COMPLEX_OBJ, SIMPLE_OBJ]):

    def to_simple(self, complex_obj: COMPLEX_OBJ) -> SIMPLE_OBJ: ...

    def from_simple(self, simple_obj: SIMPLE_OBJ) -> COMPLEX_OBJ: ...

    def from_simple_gen(
        self, simple_objs: Iterable[SIMPLE_OBJ]
    ) -> Generator[COMPLEX_OBJ, None, None]: ...

    def to_simple_gen(
        self,
        complex_objs: Iterable[COMPLEX_OBJ],
    ) -> Generator[SIMPLE_OBJ, None, None]: ...


class SimpleSerializer(Protocol[COMPLEX_OBJ]):

    def save_json(
        self,
        path_out: Path,
        complex_obj: COMPLEX_OBJ,
        indent: int = 1,
        overwrite: bool = False,
    ): ...

    def load_json(self, path_in: Path) -> COMPLEX_OBJ: ...

    def save_yaml(
        self,
        path_out: Path,
        complex_obj: COMPLEX_OBJ,
        indent: int = 1,
        overwrite: bool = False,
    ): ...

    def load_yaml(self, path_in: Path) -> COMPLEX_OBJ: ...


class SimpleSerializerABC(ABC, Generic[COMPLEX_OBJ, SIMPLE_OBJ]):
    def __init__(
        self,
        complex_cls: Type[COMPLEX_OBJ],
        simple_factory: Optional[Callable[[COMPLEX_OBJ], SIMPLE_OBJ]] = None,
        complex_factory: Optional[Callable[[SIMPLE_OBJ], COMPLEX_OBJ]] = None,
    ) -> None:
        super().__init__()
        self.complex_cls = complex_cls
        self.simple_factory = simple_factory
        self.complex_factory = complex_factory

    @abstractmethod
    def to_simple(self, complex_obj: COMPLEX_OBJ) -> SIMPLE_OBJ:
        pass

    @abstractmethod
    def from_simple(self, obj: SIMPLE_OBJ) -> COMPLEX_OBJ:
        pass

    def from_simple_gen(
        self, simple_objs: Iterable[SIMPLE_OBJ]
    ) -> Generator[COMPLEX_OBJ, None, None]:
        for item in simple_objs:
            yield self.from_simple(item)

    def to_simple_gen(
        self, complex_obj: Iterable[COMPLEX_OBJ]
    ) -> Generator[SIMPLE_OBJ, None, None]:
        for item in complex_obj:
            yield self.to_simple(item)

    def save_json(
        self,
        path_out: Path,
        complex_obj: COMPLEX_OBJ,
        indent: int = 1,
        overwrite: bool = False,
    ):
        check_file(path_out=path_out, overwrite=overwrite)
        path_out.parent.mkdir(exist_ok=True, parents=True)
        with open(path_out, "w") as file:
            json_dump(obj=complex_obj, fp=file, default=self.to_simple, indent=indent)

    def load_json(self, path_in: Path) -> COMPLEX_OBJ:
        with open(path_in, "r") as file:
            return self.from_simple(json_load(file))

    def save_yaml(
        self,
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
            safe_dump(data=self.to_simple(complex_obj), stream=file, indent=indent)

    def load_yaml(self, path_in: Path, complex_obj: Type[COMPLEX_OBJ]) -> COMPLEX_OBJ:
        if not YAML:
            raise ValueError("PyYaml not found.")
        with open(path_in, "r") as file:
            return self.from_simple(safe_load(file))


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
    def __init__(
        self,
        complex_cls: Type[COMPLEX_OBJ],
        simple_factory: Optional[Callable[[COMPLEX_OBJ], SIMPLE_OBJ]] = None,
        complex_factory: Optional[Callable[[SIMPLE_OBJ], COMPLEX_OBJ]] = None,
    ) -> None:
        if simple_factory is None:
            simple_factory = self._to_simple_default
        if complex_factory is None:
            complex_factory = self._from_simple_default
        self.simple_factory = simple_factory
        self.complex_factory = complex_factory
        super().__init__(
            complex_cls=complex_cls,
            simple_factory=simple_factory,
            complex_factory=complex_factory,
        )
        self.complex_cls = complex_cls

    def to_simple(self, complex_obj: COMPLEX_OBJ) -> SIMPLE_OBJ:
        return self.simple_factory(complex_obj)

    def from_simple(self, simple_obj: SIMPLE_OBJ) -> COMPLEX_OBJ:
        return self.complex_factory(simple_obj)

    def _to_simple_default(self, complex_obj: COMPLEX_OBJ) -> SIMPLE_OBJ:
        if is_dataclass(complex_obj):
            return asdict(complex_obj)  # type: ignore
        else:
            raise ValueError(
                f"complex_obj is not a dataclass, its type name is {type(complex_obj).__name__}"
            )

    def _from_simple_default(self, simple_obj: SIMPLE_OBJ) -> COMPLEX_OBJ:
        return self.complex_cls(**simple_obj)

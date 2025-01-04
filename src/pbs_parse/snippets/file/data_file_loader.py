"""FILE: data_file_loader.py."""

from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class FileResource[T]:
    """FileResource."""

    resource: T
    file_path: Path


class DataFileLoader[T](ABC):
    """DataFileLoader."""

    def __init__(self, path_in: Path, glob: str) -> None:
        """Load data files from a directory. Files match the glob.

        Args:
            path_in (Path): Directory to load files from.
            glob (str): The glob to match.

        Examples:
            ```
            loader = DataFileLoader[str](path_in=Path("/projects/tmp"), glob="*.txt")
            for data in loader():
                print(data)
            ```

        """
        if path_in.is_file():
            raise ValueError(
                f"Path in is an existing file, should be a directory. {path_in=}"
            )
        self.path_in = path_in
        self.glob = glob
        self.files: list[Path] = []
        self._build_file_list()

    def __iter__(self) -> Iterable[FileResource[T]]:
        """__iter__.

        Returns:
            Iterable[FileResource[T]]: _description_
        """
        return (
            FileResource(resource=self._translate(obj_path=x), file_path=x)
            for x in self.files
        )

    def __len__(self) -> int:
        """__len__.

        Returns:
            int: _description_
        """
        return len(self.files)

    def __getitem__(self, position: int) -> FileResource[T]:
        """__getitem__.

        Args:
            position (int): _description_

        Returns:
            FileResource[T]: _description_
        """
        file_path = self.files[position]
        return FileResource[T](resource=self._translate(file_path), file_path=file_path)

    # def __call__(self) -> Iterable[FileResource[T]]:
    #     """Get an iterable of the loaded data files.

    #     Returns:
    #         Iterable[T]: _description_

    #     Yields:
    #         Iterator[Iterable[T]]: _description_
    #     """
    #     for path in self.files:
    #         yield FileResource(resource=self._translate(obj_path=path), file_path=path)

    def _build_file_list(self):
        files = list(self.path_in.glob(self.glob))
        files.sort()
        self.files = files

    # @property
    # def file_count(self) -> int:
    #     """The total number of discovered files matching the glob.

    #     This is only populated after the __call__ function is called.
    #     """
    #     return len(self.files)

    @abstractmethod
    def _translate(self, obj_path: Path) -> T: ...

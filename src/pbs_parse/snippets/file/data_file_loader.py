"""FILE: data_file_loader.py."""

from abc import ABC, abstractmethod
from collections.abc import Iterable
from pathlib import Path


class DataFileLoader[T](ABC):
    """DataFileLoader."""

    def __init__(self, path_in: Path, glob: str) -> None:
        """Load data files from a directory. Files match the glob.

        File paths are discovered after calling __call_, and refreshed after
        further calls to __call__.

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

    def __call__(self) -> Iterable[T]:
        """Get an iterable of the loaded data files.

        Returns:
            Iterable[T]: _description_

        Yields:
            Iterator[Iterable[T]]: _description_
        """
        self._build_file_list()
        for path in self.files:
            yield self._translate(obj_path=path)

    def _build_file_list(self):
        files = list(self.path_in.glob(self.glob))
        files.sort()
        self.files = files

    @property
    def file_count(self) -> int:
        """The total number of discovered files matching the glob.

        This is only populated after the __call__ function is called.
        """
        return len(self.files)

    @abstractmethod
    def _translate(self, obj_path: Path) -> T: ...
